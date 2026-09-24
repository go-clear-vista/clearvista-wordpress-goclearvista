#!/usr/bin/env python3
"""Compare a live company page with its local build: python3 company-pages/verify_live.py <slug>...
Checks the rendered Code module text/markup, the form src, raw shortcode leaks, and square brackets."""
import html, re, subprocess, sys, time, os
HERE = os.path.dirname(os.path.abspath(__file__))
def norm(s):
    s = html.unescape(s)
    s = re.sub(r'\s(decoding|fetchpriority)="[^"]*"', "", s)   # added by WordPress on render
    s = re.sub(r'<noscript>.*?</noscript>', "", s, flags=re.S)   # WP Rocket lazyload fallbacks
    s = re.sub(r'src="data:image/svg\+xml[^"]*"(.*?)data-lazy-src=', r'\1src=', s)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"</?p>|<br\s*/?>", "", s)          # wpautop noise
    s = s.replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", "", s)
ok = True
for slug in sys.argv[1:]:
    live = subprocess.run(["curl", "-sL", f"https://www.goclearvista.com/{slug}/?nocache={int(time.time())}"], capture_output=True, text=True).stdout
    local = open(os.path.join(HERE, "build", f"{slug}-code.html")).read().strip()
    div = open(os.path.join(HERE, "build", f"{slug}.divi.txt")).read()
    form = re.search(r"src='([^']+)'></iframe>\[/et_pb_code\]", div).group(1)
    a = live.find("<style>.cvs-hero")
    seg = live[a:] if a >= 0 else ""
    same = bool(seg) and norm(local) in norm(seg)
    leaks = re.findall(r"\[/?et_pb_[a-z_]+", live)
    res = dict(code_found=a >= 0, matches_local=same, form_ok=(form in live or html.escape(form) in live), shortcode_leaks=len(leaks))
    print(slug, res)
    if not same and seg:
        x, y = norm(seg)[:len(norm(local))], norm(local)
        i = next((k for k in range(min(len(x), len(y))) if x[k] != y[k]), min(len(x), len(y)))
        print("   first diff at", i, "live:", x[i-60:i+80], "\n   local:", y[i-60:i+80])
    ok &= same and res["form_ok"] and not leaks
sys.exit(0 if ok else 1)
