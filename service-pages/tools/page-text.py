#!/usr/bin/env python3
"""Print the visible main-content text of a saved goclearvista.com page, one line per text node.

Strips the header, scripts and styles so two saves of the same page can be diffed to confirm
an edit changed only what was intended:

    curl -sL --compressed -A 'Mozilla/5.0' https://www.goclearvista.com/about-us-2/ -o before.html
    # ...make the edit...
    curl -sL --compressed -A 'Mozilla/5.0' "https://www.goclearvista.com/about-us-2/?nc=$RANDOM" -o after.html
    diff <(python3 tools/page-text.py before.html) <(python3 tools/page-text.py after.html)
"""
import html
import re
import sys

s = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
m = re.search(r'<div id="et-main-area"(.*)<footer', s, re.S) or re.search(r"<body(.*)</body>", s, re.S)
b = m.group(1)
b = re.sub(r"<header.*?</header>", "", b, flags=re.S)
b = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", "", b)
t = html.unescape(re.sub(r"<[^>]+>", "\n", b))
print("\n".join(line.strip() for line in t.split("\n") if line.strip()))
