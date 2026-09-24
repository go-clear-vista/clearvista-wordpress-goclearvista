#!/usr/bin/env python3
"""Generate Divi shortcode content + local previews for the service-page redesign drafts.

Design system mirrors the live State of Utah Contract / Services pages (cvs-*, cvu-* classes),
plus a few new components prefixed cvp- (process steps, FAQ, tier table, gallery, visit block).
"""
import html, json, os, re, sys

OUT = os.environ.get("OUT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "build"))
UP = "https://www.goclearvista.com/wp-content/uploads"
FORM_DEMO = "https://forms.goclearvista.com/clearvista/form/RequestaFreeDemoorQuote/formperma/C1BPewDGmP0RHRo3dLbMxoQdXcQZwdbZr9b4uPdOC3I"

# ---------------------------------------------------------------- CSS
CSS_BASE = (
    # hero / buttons / CTA band (identical to live pages)
    ".cvs-hero{position:relative;background:linear-gradient(180deg,rgba(20,22,52,.55),rgba(20,22,52,.88)),url(__HERO__) center/cover;color:#fff}"
    ".cvs-hero-in{max-width:1240px;margin:0 auto;padding:110px 40px 90px}"
    ".cvs-eye{color:#d9a13a;font-weight:800;letter-spacing:.18em;font-size:14px;margin:0 0 12px;padding:0}"
    ".cvs-hero h1{color:#fff;font-size:52px;line-height:1.08em;font-weight:800;margin:0 0 16px;padding:0;text-shadow:0 2px 10px rgba(0,0,0,.35)}"
    ".cvs-hero .cvs-sub{font-size:20px;line-height:1.55em;color:#e3e5f0;max-width:660px;margin:0;padding:0 0 30px}"
    ".cvs-btns{display:flex;gap:14px;flex-wrap:wrap}"
    ".cvs-btn{display:inline-block;padding:14px 26px;border-radius:4px;font-weight:700;font-size:16px}"
    ".cvs-btn.p{background:#d9a13a;color:#161834!important}"
    ".cvs-btn.s{border:2px solid rgba(255,255,255,.6);color:#fff!important}"
    ".cvs-cta{background:#161834;color:#fff;text-align:center;border-top:1px solid rgba(255,255,255,.12)}"
    ".cvs-cta-in{max-width:900px;margin:0 auto;padding:56px 30px 20px}"
    ".cvs-cta h2{color:#fff;font-size:34px;font-weight:800;margin:0 0 10px;padding:0}"
    ".cvs-cta p{color:#c9cbe0;font-size:17px;margin:0;padding:0}"
    ".cvs-cta .cvs-eye{color:#d9a13a;font-size:14px;padding:0 0 10px}"
    # stats bar
    ".cvu-stats{background:#161834}"
    ".cvu-stats-in{max-width:1240px;margin:0 auto;padding:0 40px;display:grid;grid-template-columns:repeat(3,1fr)}"
    ".cvu-stats-in.c4{grid-template-columns:repeat(4,1fr)}"
    ".cvu-stat{padding:26px 20px;border-left:1px solid rgba(255,255,255,.12);text-align:center}"
    ".cvu-stat:first-child{border-left:0}"
    ".cvu-stat b{display:block;color:#d9a13a;font-size:30px;font-weight:800;line-height:1.1em}"
    ".cvu-stat i{display:block;font-style:normal;color:#c9cbe0;font-size:14px;margin-top:6px;line-height:1.35em}"
    # sections / type
    ".cvu-sec{background:#fff}.cvu-sec.alt{background:#f6f7fb}"
    ".cvu-in{max-width:1240px;margin:0 auto;padding:64px 40px}"
    ".cvu-in>h2,.cvu-h{color:#292d5b;font-size:30px;font-weight:800;margin:0 0 10px;padding:0;line-height:1.2em}"
    ".cvu-lead{color:#595959;font-size:17px;line-height:1.6em;margin:0;padding:0 0 28px;max-width:760px}"
    ".cvu-p{color:#3d3f55;font-size:16px;line-height:1.7em;margin:0;padding:0 0 14px}"
    ".cvu-p a,.cvu-small a,.cvp-faq a{color:#292d5b!important;font-weight:700;border-bottom:2px solid #d9a13a}"
    ".cvu-small{color:#595959;font-size:14px;line-height:1.6em;margin:0;padding:6px 0 0}"
    ".cvu-2{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}"
    ".cvp-intro{display:grid;grid-template-columns:1fr 1.15fr;gap:56px;align-items:start}"
    ".cvp-intro h2{color:#292d5b;font-size:34px;line-height:1.15em;font-weight:800;margin:0;padding:0}"
    ".cvp-intro .cvu-p{font-size:17px}"
    # cards
    ".cvu-3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}"
    ".cvu-4{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}"
    ".cvu-c{background:#fff;border:1px solid #e3e5ee;border-top:3px solid #d9a13a;border-radius:6px;padding:26px 24px;box-shadow:0 6px 20px rgba(41,45,91,.07)}"
    ".cvu-c em{font-style:normal;color:#b07d1f;font-weight:800;font-size:13px;letter-spacing:.12em}"
    ".cvu-c strong{display:block;color:#292d5b;font-size:19px;font-weight:800;margin:8px 0 6px;line-height:1.25em}"
    ".cvu-c span{display:block;color:#595959;font-size:15px;line-height:1.55em}"
    # checklist + chips
    ".cvu-ul{list-style:none!important;margin:0!important;padding:0!important}"
    ".cvu-ul li{list-style:none!important;position:relative;margin:0 0 12px!important;padding:0 0 0 30px!important;color:#3d3f55;font-size:16px;line-height:1.5em}"
    ".cvu-ul li:before{content:\"\";position:absolute;left:0;top:3px;width:18px;height:18px;border-radius:50%;background:#d9a13a url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23161834' d='M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z'/%3E%3C/svg%3E\") center/12px no-repeat}"
    ".cvu-chips{display:flex;flex-wrap:wrap;gap:8px}"
    ".cvu-chips span{background:#fff;border:1px solid #e3e5ee;border-left:3px solid #d9a13a;color:#292d5b;font-weight:600;font-size:14px;padding:8px 13px;border-radius:3px}"
    # process steps
    ".cvp-steps{display:grid;grid-template-columns:repeat(var(--n,5),1fr);gap:18px;list-style:none!important;margin:0!important;padding:0!important}"
    ".cvp-steps li{list-style:none!important;position:relative;margin:0!important;padding:0!important}"
    ".cvp-steps li:after{content:\"\";position:absolute;top:23px;left:58px;right:-18px;height:2px;background:#e3d2ae}"
    ".cvp-steps li:last-child:after{display:none}"
    ".cvp-steps b{position:relative;z-index:1;display:flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:50%;background:#161834;color:#d9a13a;font-size:17px;font-weight:800;margin-bottom:16px;box-shadow:0 0 0 5px #f6f7fb}"
    ".cvp-steps strong{display:block;color:#292d5b;font-size:18px;font-weight:800;margin-bottom:6px}"
    ".cvp-steps span{display:block;color:#595959;font-size:15px;line-height:1.55em;padding-right:6px}"
    ".cvp-steps-note{color:#3d3f55;font-size:16px;margin:30px 0 0;padding:16px 20px;background:#fff;border-left:3px solid #d9a13a;border-radius:3px}"
    ".cvp-steps-note a{color:#292d5b!important;font-weight:700;border-bottom:2px solid #d9a13a}"
    # spotlight
    ".cvs-spot{background:#161834;color:#fff}"
    ".cvs-spot-in{max-width:1240px;margin:0 auto;padding:72px 40px;display:grid;grid-template-columns:1.1fr 1fr;gap:56px;align-items:center}"
    ".cvs-spot-ph{position:relative}"
    ".cvs-spot-ph img{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:6px;box-shadow:0 30px 60px rgba(0,0,0,.45)}"
    ".cvs-spot-ph:before{content:\"\";position:absolute;left:-14px;bottom:-14px;width:45%;height:45%;border-left:4px solid #d9a13a;border-bottom:4px solid #d9a13a;border-radius:0 0 0 6px}"
    ".cvs-spot h2{color:#fff;font-size:38px;line-height:1.1em;font-weight:800;margin:0 0 16px;padding:0}"
    ".cvs-spot .cvs-sp{color:#d6d8e6;font-size:17px;line-height:1.65em;margin:0;padding:0 0 26px}"
    ".cvs-stats{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:28px}"
    ".cvs-stat{border-left:3px solid #d9a13a;padding:4px 0 4px 14px}"
    ".cvs-stat b{display:block;color:#d9a13a;font-size:30px;font-weight:800;line-height:1.1em}"
    ".cvs-stat i{display:block;font-style:normal;color:#c9cbe0;font-size:14px;margin-top:4px}"
    # related services
    ".cvp-rel{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}"
    ".cvp-rel a{display:block;text-decoration:none!important;background:#fff;border:1px solid #e3e5ee;border-left:3px solid #d9a13a;border-radius:4px;padding:18px 20px;transition:transform .2s,box-shadow .2s}"
    ".cvp-rel a:hover{transform:translateY(-3px);box-shadow:0 12px 26px rgba(41,45,91,.12)}"
    ".cvp-rel strong{display:block;color:#292d5b;font-size:17px;font-weight:800;margin-bottom:4px}"
    ".cvp-rel span{display:block;color:#595959;font-size:14px;line-height:1.45em}"
    ".cvp-rel em{display:block;font-style:normal;color:#b07d1f;font-weight:700;font-size:13px;letter-spacing:.04em;margin-top:8px}"
    # FAQ
    ".cvp-faq{max-width:900px}"
    ".cvp-faq details{background:#fff;border:1px solid #e3e5ee;border-left:3px solid #d9a13a;border-radius:4px;margin:0 0 12px}"
    ".cvp-faq summary{cursor:pointer;list-style:none;padding:18px 52px 18px 22px;color:#292d5b;font-weight:800;font-size:17px;position:relative}"
    ".cvp-faq summary::-webkit-details-marker{display:none}"
    ".cvp-faq summary:after{content:\"+\";position:absolute;right:22px;top:12px;color:#d9a13a;font-size:28px;font-weight:400}"
    ".cvp-faq details[open] summary:after{content:\"–\"}"
    ".cvp-faq details p{color:#3d3f55;font-size:16px;line-height:1.65em;margin:0;padding:0 22px 20px}"
    ".cvu-form-w .et_pb_row{max-width:900px}"
    # responsive
    "@media (max-width:980px){.cvs-hero-in{padding:80px 28px 64px}.cvs-hero h1{font-size:42px}"
    ".cvu-stats-in,.cvu-stats-in.c4{padding:0 28px}.cvu-stats-in.c4{grid-template-columns:repeat(2,1fr)}.cvu-stats-in.c4 .cvu-stat:nth-child(3){border-left:0}.cvu-stats-in.c4 .cvu-stat:nth-child(n+3){border-top:1px solid rgba(255,255,255,.12)}"
    ".cvu-in{padding:48px 28px}.cvu-3{grid-template-columns:1fr 1fr}.cvu-4{grid-template-columns:1fr 1fr}.cvu-2,.cvp-intro{grid-template-columns:1fr;gap:28px}"
    ".cvp-steps{grid-template-columns:1fr 1fr;gap:26px 22px}.cvp-steps li:after{display:none}"
    ".cvs-spot-in{grid-template-columns:1fr;gap:36px;padding:56px 28px}.cvs-spot h2{font-size:32px}.cvp-rel{grid-template-columns:1fr 1fr}}"
    "@media (max-width:767px){.cvs-hero-in{padding:64px 20px 48px}.cvs-hero h1{font-size:34px}.cvs-hero .cvs-sub{font-size:17px}.cvs-btn{flex:1 1 100%;text-align:center}.cvs-cta h2{font-size:26px}"
    ".cvu-stats-in,.cvu-stats-in.c4{padding:0 12px}.cvu-stat{padding:18px 8px}.cvu-stat b{font-size:22px}.cvu-stat i{font-size:12px}"
    ".cvu-in{padding:36px 20px}.cvu-in>h2,.cvu-h,.cvp-intro h2{font-size:25px}.cvu-lead,.cvp-intro .cvu-p{font-size:16px}"
    ".cvu-3,.cvu-4{grid-template-columns:1fr;gap:12px}.cvu-c{padding:18px 18px}.cvu-c strong{font-size:17px}"
    ".cvp-steps{grid-template-columns:1fr;gap:0}.cvp-steps li{display:grid;grid-template-columns:46px 1fr;column-gap:16px;padding:0 0 22px!important}.cvp-steps li:after{display:block;top:52px;bottom:4px;left:22px;right:auto;width:2px;height:auto}.cvp-steps b{grid-row:span 2;margin:0}"
    ".cvs-spot-in{padding:44px 20px}.cvs-spot h2{font-size:27px}.cvs-spot .cvs-sp{font-size:16px}.cvs-stat b{font-size:24px}.cvs-spot-ph:before{left:-8px;bottom:-8px}"
    ".cvp-rel{grid-template-columns:1fr;gap:10px}.cvp-faq summary{font-size:15px;padding:15px 46px 15px 16px}.cvp-faq details p{font-size:15px;padding:0 16px 16px}}"
)

CSS_TIERS = (
    ".cvp-tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:6px;box-shadow:0 10px 30px rgba(41,45,91,.1)}"
    ".cvp-t{width:100%;min-width:720px;border-collapse:collapse;background:#fff;font-size:15px}"
    ".cvp-t th,.cvp-t td{border:1px solid #e3e5ee;padding:12px 14px;text-align:center;color:#3d3f55}"
    ".cvp-t td:first-child,.cvp-t th:first-child{text-align:left;font-weight:600;color:#292d5b}"
    ".cvp-t thead th,.cvp-t thead th:first-child{background:#161834;color:#fff;font-weight:800;font-size:15px;line-height:1.3em;vertical-align:bottom}"
    ".cvp-t thead th small{display:block;color:#c9cbe0;font-weight:600;font-size:12px;letter-spacing:.08em;margin-top:4px}"
    ".cvp-t thead th.g{background:#d9a13a;color:#161834}.cvp-t thead th.g small{color:#161834}"
    ".cvp-t td.g{background:#fdf7ea}"
    ".cvp-t tbody tr:nth-child(even) td{background-color:#fafbfd}.cvp-t tbody tr:nth-child(even) td.g{background:#fbf1dc}"
    ".cvp-y{display:inline-block;width:20px;height:20px;border-radius:50%;background:#d9a13a url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23161834' d='M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z'/%3E%3C/svg%3E\") center/13px no-repeat;vertical-align:middle}"
    ".cvp-n{color:#c4c6d3}"
    ".cvp-t tbody td.sec{background:#eef0f6!important;color:#292d5b;font-size:12px;font-weight:800;letter-spacing:.14em;text-align:left}"
    ".cvp-tnote{color:#595959;font-size:13px;line-height:1.6em;margin:14px 0 0;padding:0}"
    ".cvp-swipe{display:none;color:#b07d1f;font-weight:700;font-size:13px;letter-spacing:.04em;margin:0 0 10px;padding:0}"
    "@media (max-width:767px){.cvp-swipe{display:block}.cvp-t{font-size:13px;min-width:600px}.cvp-t th,.cvp-t td{padding:10px 8px}"
    ".cvp-t td:first-child,.cvp-t th:first-child{position:sticky;left:0;z-index:1;width:150px;min-width:150px;background:#fff;box-shadow:2px 0 4px rgba(41,45,91,.08)}"
    ".cvp-t thead th:first-child{background:#161834}.cvp-t tbody tr:nth-child(even) td:first-child{background:#fafbfd}.cvp-t tbody td.sec{position:static}}"
)

CSS_EXP = (
    ".cvp-gal{display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:220px 220px;gap:14px}"
    ".cvp-gal img{display:block;width:100%;height:100%;object-fit:cover;border-radius:6px}"
    ".cvp-gal img:first-child{grid-row:span 2}.cvp-gal img:nth-child(2){grid-column:span 2}"
    ".cvp-visit{background:#161834;color:#fff}"
    ".cvp-visit .cvu-in>h2{color:#fff}"
    ".cvp-vg{display:grid;grid-template-columns:1fr 1.3fr;gap:40px;align-items:stretch}"
    ".cvp-info{display:grid;gap:18px;align-content:start}"
    ".cvp-info div{border-left:3px solid #d9a13a;padding:2px 0 2px 16px}"
    ".cvp-info small{display:block;color:#d9a13a;font-weight:800;font-size:12px;letter-spacing:.16em;margin-bottom:4px}"
    ".cvp-info span,.cvp-info a{color:#fff!important;font-size:17px;line-height:1.5em}"
    ".cvp-info a.big{font-size:24px;font-weight:800}"
    ".cvp-map iframe{display:block;width:100%;height:100%;min-height:320px;border:0;border-radius:6px}"
    "@media (max-width:980px){.cvp-vg{grid-template-columns:1fr}.cvp-gal{grid-template-columns:1fr 1fr;grid-template-rows:260px 160px 160px}.cvp-gal img:first-child{grid-column:span 2;grid-row:auto}}"
    "@media (max-width:767px){.cvp-gal{grid-template-rows:200px 120px 120px;gap:8px}}"
)

# ---------------------------------------------------------------- components
def esc(s):
    return s  # copy is authored as HTML-safe text below (entities written explicitly)

def hero(eye, h1, sub, b1, b2_label, b2_href):
    return (f'<div class="cvs-hero"><div class="cvs-hero-in"><p class="cvs-eye">{eye}</p><h1>{h1}</h1>'
            f'<p class="cvs-sub">{sub}</p><div class="cvs-btns"><a class="cvs-btn p" href="#cvs-quote">{b1}</a>'
            f'<a class="cvs-btn s" href="{b2_href}">{b2_label}</a></div></div></div>')

def stats(items):
    c = " c4" if len(items) == 4 else ""
    inner = "".join(f'<div class="cvu-stat"><b>{b}</b><i>{i}</i></div>' for b, i in items)
    return f'<div class="cvu-stats"><div class="cvu-stats-in{c}">{inner}</div></div>'

def sec(inner, alt=False, id_=None, cls=""):
    a = " alt" if alt else ""
    i = f' id="{id_}"' if id_ else ""
    return f'<div class="cvu-sec{a}{cls}"{i}><div class="cvu-in">{inner}</div></div>'

def intro(eye, h2, paras):
    ps = "".join(f'<p class="cvu-p">{p}</p>' for p in paras)
    return sec(f'<div class="cvp-intro"><div><p class="cvs-eye">{eye}</p><h2>{h2}</h2></div><div>{ps}</div></div>')

def cards(eye, h2, lead, items, cols=3, alt=True, id_=None):
    grid = "".join(f'<div class="cvu-c"><em>{e}</em><strong>{s}</strong><span>{t}</span></div>' for e, s, t in items)
    ld = f'<p class="cvu-lead">{lead}</p>' if lead else ""
    return sec(f'<p class="cvs-eye">{eye}</p><h2>{h2}</h2>{ld}<div class="cvu-{cols}">{grid}</div>', alt=alt, id_=id_)

def steps(eye, h2, lead, items, note=None, alt=False, id_="cvp-process"):
    lis = "".join(f'<li><b>{n:02d}</b><strong>{s}</strong><span>{t}</span></li>' for n, (s, t) in enumerate(items, 1))
    nt = f'<p class="cvp-steps-note">{note}</p>' if note else ""
    ld = f'<p class="cvu-lead">{lead}</p>' if lead else ""
    return sec(f'<p class="cvs-eye">{eye}</p><h2>{h2}</h2>{ld}<ol class="cvp-steps" style="--n:{len(items)}">{lis}</ol>{nt}', alt=alt, id_=id_)

def two_col(left, right, alt=False):
    return sec(f'<div class="cvu-2"><div>{left}</div><div>{right}</div></div>', alt=alt)

def ul(items):
    return '<ul class="cvu-ul">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def chips(items):
    return '<div class="cvu-chips">' + "".join(f"<span>{x}</span>" for x in items) + "</div>"

def spot(img, alt, eye, h2, text, st, btn, href):
    s = "".join(f'<div class="cvs-stat"><b>{b}</b><i>{i}</i></div>' for b, i in st)
    return (f'<div class="cvs-spot"><div class="cvs-spot-in"><div class="cvs-spot-ph"><img src="{img}" alt="{alt}" loading="lazy"></div>'
            f'<div><p class="cvs-eye">{eye}</p><h2>{h2}</h2><p class="cvs-sp">{text}</p><div class="cvs-stats">{s}</div>'
            f'<a class="cvs-btn p" href="{href}">{btn}</a></div></div></div>')

REL = {
    "design": ("/design-engineering/", "Design &amp; Engineering", "Needs assessments, system design and documentation."),
    "install": ("/system-installation/", "System Installation", "Certified crews, from one room to multi-site rollouts."),
    "program": ("/custom-program-integration/", "Custom Programming &amp; Integration", "Control programming that makes every system work as one."),
    "sla": ("/service-level-agreements/", "Service Level Agreements", "Support plans that keep critical systems running."),
    "exp": ("/experience-center/", "Experience Center", "Book a guided visit to see working systems in action."),
}

def related(exclude):
    keys = [k for k in ["design", "install", "program", "sla", "exp"] if k != exclude]
    a = "".join(f'<a href="{REL[k][0]}"><strong>{REL[k][1]}</strong><span>{REL[k][2]}</span><em>EXPLORE &#8594;</em></a>' for k in keys)
    return sec(f'<p class="cvs-eye">ONE TEAM. EVERY STAGE.</p><h2>Explore Our Other Services</h2><div class="cvp-rel">{a}</div>', alt=True)

def faq(items, alt=False):
    d = "".join(f'<details{" open" if n == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for n, (q, a) in enumerate(items))
    return sec(f'<p class="cvs-eye">FAQS</p><h2>Frequently Asked Questions</h2><div class="cvp-faq">{d}</div>', alt=alt)

def cta(eye, h2, p):
    return (f'<div class="cvs-cta" id="cvs-quote"><div class="cvs-cta-in"><p class="cvs-eye">{eye}</p>'
            f'<h2>{h2}</h2><p>{p}</p></div></div>')

# ---------------------------------------------------------------- Divi wrapper
def divi(label, body_html, form_src):
    head = (f'[et_pb_section fb_built="1" admin_label="{label} Redesign" _builder_version="4.27.5" _module_preset="default" '
            'custom_margin="0px||0px||false|false" custom_padding="0px||0px||false|false" global_colors_info="{}"]'
            f'[et_pb_row admin_label="{label} Content" _builder_version="4.27.5" _module_preset="default" width="100%" max_width="100%" '
            'custom_margin="0px||0px||false|false" custom_padding="0px||0px||false|false" global_colors_info="{}"]'
            '[et_pb_column type="4_4" _builder_version="4.27.5" _module_preset="default" global_colors_info="{}"]'
            f'[et_pb_code admin_label="{label} Page Content" _builder_version="4.27.5" _module_preset="default" '
            'custom_margin="0px||0px||false|false" custom_padding="0px||0px||false|false" global_colors_info="{}"]')
    tail = '[/et_pb_code][/et_pb_column][/et_pb_row][/et_pb_section]'
    form = ('[et_pb_section fb_built="1" admin_label="Quote Form" module_class="cvu-form-w" _builder_version="4.27.5" _module_preset="default" '
            'background_color="#FFFFFF" custom_margin="0px||0px||false|false" custom_padding="20px||20px||false|false" global_colors_info="{}"]'
            '[et_pb_row _builder_version="4.27.5" _module_preset="default" width="90%" max_width="900px" module_alignment="center" '
            'custom_padding="0px||0px||false|false" global_colors_info="{}"][et_pb_column type="4_4" _builder_version="4.27.5" '
            '_module_preset="default" global_colors_info="{}"][et_pb_code _builder_version="4.27.5" _module_preset="default" global_colors_info="{}"]'
            f"<iframe aria-label='Request a Free Demo or Quote!' frameborder=\"0\" style=\"height:600px;width:100%;border:none;\" src='{form_src}'></iframe>"
            '[/et_pb_code][/et_pb_column][/et_pb_row][/et_pb_section]')
    return head + body_html + tail + form

def build(slug, label, hero_img, css_extra, sections, form_ref):
    css = CSS_BASE.replace("__HERO__", hero_img) + css_extra
    body = f"<style>{css}</style>" + "".join(sections)
    assert "[" not in re.sub(r"<style>.*?</style>", "", body), f"{slug}: square bracket in body breaks Divi shortcodes"
    form_src = f"{FORM_DEMO}?zf_rszfm=1&ref={form_ref}"
    content = divi(label, body, form_src)
    open(os.path.join(OUT, f"{slug}.divi.txt"), "w").write(content)
    return body, form_src

# ================================================================ PAGES
PAGES = {}

# ---------------------------------------------------------------- 1. Design & Engineering
PAGES["design-engineering"] = dict(
    label="Design &amp; Engineering", hero=f"{UP}/2022/08/design-engineering-header-2.jpg", css="",
    form_ref="Design%20and%20Engineering",
    title="Design & Engineering",
    excerpt="AV system design and engineering from ClearVista: needs assessments, site surveys, system design, drawings and documentation from AVIXA CTS-certified designers.",
    sections=[
        hero("DESIGN &amp; ENGINEERING", "Systems Designed Around How You Work",
             "Needs assessments, system design, drawings and documentation from certified designers, engineered for today and ready for what comes next.",
             "Schedule a Consultation", "See Our Process", "#cvp-process"),
        stats([("1953", "Solving technology problems since"), ("100+", "Authorized manufacturer brands"),
               ("CTS", "AVIXA-certified design staff"), ("In-House", "Design through long-term support")]),
        intro("OUR APPROACH", "Figuring Stuff Out Is One of Our Core Values", [
            "Great systems start long before the first cable is pulled. Our engineers learn your objectives, budget, technical requirements and the people who will use the space, then design a system that fits all four.",
            "We improve existing AV systems and design brand-new spaces. Along the way, our specialists explain the technologies and options available so you can choose with confidence, and we plan for the upgrades you&#8217;ll want down the road.",
            "If there&#8217;s a goal and no obvious way to reach it, we do the research and the legwork to make it happen. That&#8217;s been true for decades, from helping our partner brands refine their products to engineering custom systems that solve problems no off-the-shelf product could."]),
        cards("WHAT&#8217;S INCLUDED", "Design Services That Remove the Guesswork", None, [
            ("01", "Needs Assessment", "We start with your goals, budget, technical requirements and the people who&#8217;ll use the system every day."),
            ("02", "Site Surveys", "On-site walkthroughs capture room conditions, infrastructure and constraints before anything is specified."),
            ("03", "System Design", "Equipment selection from more than 100 authorized brands, matched to your application instead of a single product line."),
            ("04", "Drawings &amp; Documentation", "System diagrams, line drawings and component lists that show exactly how everything connects."),
            ("05", "Codes &amp; Standards", "Designs prepared in accordance with building codes and regulations, so installation and inspection go smoothly."),
            ("06", "Future Planning", "We plan for growth and technology changes so today&#8217;s system doesn&#8217;t limit tomorrow&#8217;s needs.")]),
        steps("OUR PROCESS", "From First Conversation to Final Design", "A proven process that keeps your goals, budget and users at the center of every decision.", [
            ("Discover", "We discuss your objectives, budget, timeline and the people who will use the space."),
            ("Assess", "Site surveys and technical requirements capture everything the design needs to account for."),
            ("Design", "Our engineers select equipment and produce system designs, drawings and documentation."),
            ("Review", "We walk you through the options and trade-offs so you can choose the right system for your space and budget."),
            ("Deliver", "The same in-house team carries your design through programming, installation, training and support.")],
            note='Need contract pricing? Government and education customers can purchase through our <a href="/state-of-utah-contract/">State of Utah cooperative contract</a>.'),
        two_col(
            '<h2 class="cvu-h">Certified to Design It Right</h2><p class="cvu-p">Our design team holds manufacturer and industry certifications across displays, audio, control, networking and conferencing, including AVIXA&#8217;s Certified Technology Specialist (CTS) credential.</p><p class="cvu-small">See the full list on our <a href="/certifications-trainings/">Certifications &amp; Trainings</a> page.</p>',
            chips(["AVIXA CTS", "Crestron DMC-D Certified Designer", "Extron XTP Systems Engineer", "Extron Network AV Specialist", "Kramer Control System Designer",
                   "Q-SYS Certified", "Shure Integrated Systems L1 &amp; L2", "Shure Microflex Advanced", "HDBaseT Master", "Harman Core Curriculum",
                   "ClearOne ProAV Conferencing", "Sony Tatsu-Jin Master", "Zoom Rooms Accredited", "And more"]), alt=True),
        spot(f"{UP}/2023/03/UDOT-with-person.jpg", "UDOT Traffic Operations Center with direct view LED video walls",
             "PROJECT SPOTLIGHT", "UDOT Traffic Operations Center",
             "The Utah Department of Transportation asked our team (then TVS Pro) to design and install replacement displays for its main Traffic Operations Center, a room that operates around the clock. The solution: three direct view LED walls, one large center wall flanked by two smaller walls.",
             [("24/7", "Mission-critical operations"), ("3", "Direct view LED video walls")],
             "Read the Project Story", "/blog/udot-traffic-operations-center/"),
        faq([
            ("What do you need from us to get started?", "A conversation about your goals, the spaces involved, your timeline and your budget. Floor plans or existing drawings help if you have them. From there we&#8217;ll schedule a site visit."),
            ("Can you work with our existing equipment?", "Yes. We can improve an existing AV system or design a brand-new space. We&#8217;ll evaluate what you have and recommend what to keep, upgrade or replace."),
            ("What documentation will we receive?", "System diagrams, line drawings and a complete component list. At project close you&#8217;ll also receive product manuals and warranty information."),
            ("Who will we work with after the design is done?", "The same in-house team handles project planning, programming and integration, installation, training and ongoing support, so nothing gets lost in a hand-off."),
            ("Can we purchase through a state contract?", 'Yes. Government and education customers can buy through our <a href="/state-of-utah-contract/">State of Utah cooperative contract</a>.')]),
        related("design"),
        cta("START A PROJECT", "Schedule a Design Consultation", "Tell us about your space and goals. A ClearVista specialist will follow up."),
    ])

# ---------------------------------------------------------------- 2. System Installation
PAGES["system-installation"] = dict(
    label="System Installation", hero=f"{UP}/2023/03/UDOT-wall-install-2.jpg", css="",
    form_ref="System%20Installation",
    title="System Installation",
    excerpt="Certified AV system installation from ClearVista: in-house project management, installation and commissioning for single rooms, campuses and 24/7 operations centers across Utah and the Intermountain West.",
    sections=[
        hero("SYSTEM INSTALLATION", "Installed Right. Documented Completely.",
             "Certified installation teams for single rooms, campuses and 24/7 operations centers, with in-house project management from kickoff to commissioning.",
             "Request an Installation Quote", "See Our Process", "#cvp-process"),
        stats([("900+", "Pieces installed at the Delta Center"), ("Regional", "Utah, Idaho, Nevada and beyond"),
               ("In-House", "Project managers, installers and technicians"), ("Complete", "Documentation with every project")]),
        intro("OUR TEAMS", "Large Enough for Complex Systems. Local Enough to Know You.", [
            "Our installation teams are highly skilled and certified by many of today&#8217;s leading manufacturers. They&#8217;re large enough to handle complex integrated systems without losing the local touch our clients count on.",
            "In-house project managers, lead installers and service technicians keep learning new technologies and market trends, so your system is installed to current best practices.",
            "We&#8217;ve installed systems in so many government facilities, universities, schools, businesses, stadiums and venues across the region that chances are you&#8217;ve seen our work without knowing it."]),
        cards("WHY CLEARVISTA", "What You Can Expect From Our Crews", None, [
            ("01", "Certified Installers", "Crews trained and certified by leading manufacturers, installing to manufacturer and industry standards."),
            ("02", "In-House Project Management", "One project manager coordinates schedules, site requirements and communication from kickoff to closeout."),
            ("03", "Any Scale", "From a single self-contained conference room to large venues with fully automated, integrated systems."),
            ("04", "Commissioning &amp; Testing", "Every system is tested, verified and fine-tuned before handoff, so it works on day one."),
            ("05", "Training &amp; Handoff", "Your team learns how to use and care for the system, with documentation to back it up."),
            ("06", "Ongoing Support", "Service Level Agreements keep your investment maintained, monitored and supported for the long term.")]),
        steps("OUR PROCESS", "How We Deliver Your Installation", "A complete solution from the initial stages of design through final commissioning and ongoing support.", [
            ("Plan", "Your project manager builds the schedule and coordinates with your facilities team and contractors."),
            ("Prepare", "We confirm site readiness, infrastructure and equipment so installation day runs smoothly."),
            ("Install", "Certified crews install and integrate the system with clean, professional workmanship."),
            ("Commission", "We test, verify and fine-tune every component and confirm the system performs as designed."),
            ("Hand Off", "Training for your users, plus a complete closeout packet with everything your team needs.")]),
        two_col(
            '<p class="cvs-eye">PROJECT CLOSEOUT</p><h2 class="cvu-h">Every Project Ends With a Complete Packet</h2><p class="cvu-p">We believe in long-term relationships, and that starts with leaving you fully informed. With every system we install, you receive:</p>'
            + ul(["All product manuals", "Warranty information", "A complete list of components", "System diagrams", "Line drawings that show how your system is connected"]),
            '<p class="cvs-eye">MARKETS WE SERVE</p><h2 class="cvu-h">Proven Across Every Environment</h2><p class="cvu-p">Installations across Utah, Idaho and Nevada, with projects completed in California, Arizona, Texas and beyond.</p>'
            + chips(["Higher Education", "K&#8211;12", "State &amp; Local Government", "Military", "Public Safety", "Operations Centers", "Corporate", "Hospitality", "Stadiums &amp; Venues", "Healthcare"]),
            alt=True),
        sec('<p class="cvs-eye">CERTIFIED CREWS</p><h2>Installation Certifications</h2><p class="cvu-lead">A few of the certifications our installation teams hold. See the full list on our <a href="/certifications-trainings/" style="color:#292d5b;font-weight:700;border-bottom:2px solid #d9a13a">Certifications &amp; Trainings</a> page.</p>'
            + chips(["AVIXA CTS", "Extron Certified AV Associate", "HDBaseT Master", "Harman Core Curriculum", "Sharp/NEC dvLED Installer (FA &amp; FE Series)", "Epson Projector Installer", "Control4 Associate Installer", "And more"])),
        spot(f"{UP}/2018/12/VivintSmartHomeArena.jpg", "Delta Center arena in Salt Lake City during a Utah Jazz playoff game",
             "PROJECT SPOTLIGHT", "Delta Center, Salt Lake City",
             "Our team (then TVS Pro) was part of the arena&#8217;s renovation, installing more than 900 pieces of equipment across the venue. The project was featured in Sound &amp; Communications magazine.",
             [("900+", "Pieces of equipment installed"), ("Featured", "Sound &amp; Communications magazine")],
             "Read the Project Story", "/blog/concourse-engagment/"),
        faq([
            ("How large a project can you handle?", "Anything from a single conference room to large venues and campus-wide rollouts. Our teams are large enough for complex integrated systems, with in-house project managers, programmers and installation technicians."),
            ("Where do you install?", "Our teams install across Utah, Idaho and Nevada, and we&#8217;ve completed projects in California, Arizona, Texas and beyond."),
            ("Will you coordinate with our contractors and facilities team?", "Yes. Your project manager coordinates schedules and site requirements so the installation fits your construction timeline and daily operations."),
            ("What do we receive when the project is finished?", "A closeout packet with product manuals, warranty information, a complete component list, system diagrams and line drawings, plus training for your users."),
            ("What happens if something needs attention after installation?", 'Every system includes standard warranty support, and our <a href="/service-level-agreements/">Service Level Agreements</a> add faster response, maintenance visits and proactive monitoring. Existing customers can also <a href="/service-request/">submit a service request</a>.')]),
        related("install"),
        cta("START A PROJECT", "Request an Installation Quote", "Tell us about your project and timeline. A ClearVista specialist will follow up."),
    ])

# ---------------------------------------------------------------- 3. Custom Programming & Integration
PAGES["custom-program-integration"] = dict(
    label="Custom Programming &amp; Integration", hero=f"{UP}/2022/09/Programming-and-integration-2.jpg", css="",
    form_ref="Custom%20Programming%20and%20Integration",
    title="Custom Programming & Integration",
    excerpt="In-house AV control programming and system integration from ClearVista: Q-SYS, Extron, Kramer and Control4 programming, Dante networked audio, conferencing and custom user interfaces.",
    sections=[
        hero("CUSTOM PROGRAMMING &amp; INTEGRATION", "Complex Systems. Simple Control.",
             "In-house configuration and control programming that makes every device work together, with an interface your people will actually use.",
             "Talk to an Integration Expert", "See Our Process", "#cvp-process"),
        stats([("In-House", "Configuration and programming"), ("Dante L1&#8211;L3", "Certified networked audio"),
               ("Q-SYS", "Certified audio, video and control"), ("Custom", "Interfaces built for your users")]),
        intro("WHY IT MATTERS", "Your System Should Work the Way You Do", [
            "Advanced systems built for specific applications, budgets and technical needs rarely work well straight out of the box. The difference between a room people avoid and a room people love is usually the programming.",
            "Our certified programmers configure and program every device in your system so it communicates seamlessly, then give you a simple interface to control complex processes. A room can start up, switch sources or join a call with one touch.",
            "Because we design, program and install in-house, the system operates the way you envisioned from day one, and you have one team to call when your needs change."]),
        cards("WHAT WE DO", "Integration Services", None, [
            ("01", "Control System Programming", "Touch panels, keypads and automation that turn complex, multi-device processes into one-touch actions."),
            ("02", "Audio &amp; DSP Configuration", "Q-SYS, Extron ProDSP and Dante networked audio, configured and tuned for clear, consistent sound."),
            ("03", "Conferencing Integration", "Cameras, microphones, displays and conferencing platforms working together in rooms that are simple to join."),
            ("04", "AV-over-IP &amp; Networking", "Networked video and audio distribution designed and configured to live reliably on your network."),
            ("05", "Custom User Interfaces", "Interfaces branded with your logos, building and room names, and custom images so the system feels like yours."),
            ("06", "Live Production &amp; Streaming", "Switching, capture and streaming systems for broadcast studios, meetings, trainings and events.")]),
        steps("OUR PROCESS", "How We Make It All Work Together", None, [
            ("Define", "We learn how your people will use each space and what the system needs to do for them."),
            ("Configure", "Displays, audio processors, codecs and network devices are configured to work as one system."),
            ("Program", "Control logic and automation are written, then tested against real-world use cases."),
            ("Customize", "The interface is built around your users, with your branding, room names and workflows."),
            ("Train &amp; Support", "We train your users and administrators, and stay available as your needs evolve.")],
            alt=True),
        sec('<p class="cvs-eye">CERTIFIED PROGRAMMERS</p><h2>Platforms and Certifications</h2><p class="cvu-lead">A few of the programming and integration certifications our team holds. See the full list on our <a href="/certifications-trainings/" style="color:#292d5b;font-weight:700;border-bottom:2px solid #d9a13a">Certifications &amp; Trainings</a> page.</p>'
            + chips(["Q-SYS Certified", "Audinate Dante Levels 1&#8211;3", "Extron Control Professional", "Extron ProDSP Specialist", "Extron Network AV Specialist",
                     "Kramer Control System Programmer", "Kramer K-Touch", "Control4 Automation Programmer", "Universal Remote Control Total Control",
                     "Araknis Certified Network Administrator", "NewTek TriCaster &amp; 3Play", "Shure Integrated Systems L1 &amp; L2", "ClearOne ProAV Conferencing",
                     "Zoom Rooms Technical Accreditation", "AVIXA CTS", "And more"])),
        spot(f"{UP}/2023/10/USBE-1.jpg", "Utah State Board of Education production control room",
             "PROJECT SPOTLIGHT", "Utah State Board of Education",
             "The Utah State Board of Education asked our team (then TVS Pro) to upgrade its production studio with a control room that broadcasts and streams meetings and trainings. We upgraded the existing equipment and integrated new components for a more productive, easier-to-run studio.",
             [("Broadcast", "Production control room"), ("Live", "Meeting and training streams")],
             "Read the Project Story", "/blog/utah-state-board-of-education/"),
        faq([
            ("Which control and audio platforms do you program?", "Our team is certified on Q-SYS, Extron, Kramer, Control4 and Universal Remote Control platforms, with Audinate Dante networked audio certification through Level 3."),
            ("Can the touch panel match our brand?", "Yes. We can build your user interface with company logos, building and room names, and custom images so the system feels unique to your organization."),
            ("Will our staff be trained on the system?", "Yes. Training is part of every project, so your users and administrators know how to run the system from the first day."),
            ("What if our needs change after the system is installed?", 'Our team stays available for programming changes and support, and a <a href="/service-level-agreements/">Service Level Agreement</a> adds faster response, maintenance visits and firmware updates.'),
            ("Do you also design and install the systems you program?", 'Yes. We handle <a href="/design-engineering/">design and engineering</a>, programming and <a href="/system-installation/">installation</a> in-house, which means one accountable team for the whole system.')]),
        related("program"),
        cta("START A PROJECT", "Talk to an Integration Expert", "Tell us how you want your spaces to work. A ClearVista specialist will follow up."),
    ])

# ---------------------------------------------------------------- 4. Service Level Agreements
Y = '<span class="cvp-y" aria-label="Included"></span>'
N = '<span class="cvp-n" aria-label="Not included">&#8212;</span>'
TIER_ROWS = [
    ("sec", "COVERAGE"),
    ("90-day support &amp; labor coverage", 1, 1, 1, 1),
    ("180-day support &amp; labor coverage", 0, 1, 1, 1),
    ("1-year support &amp; labor coverage", 0, 0, 1, 1),
    ("sec", "SUPPORT &amp; RESPONSE"),
    ("Standard phone support (business hours)", 1, 1, 1, 1),
    ("Extended phone support (after hours)", 0, 0, 1, 1),
    ("Reactive remote support*", 0, 0, 1, 1),
    ("Reactive service visits*", 0, 0, 1, 1),
    ("2 business day response time*", 0, 0, 1, 0),
    ("1 business day response time with priority scheduling", 0, 0, 0, 1),
    ("sec", "HARDWARE"),
    ("Discounted replacement hardware", 0, 0, 1, 1),
    ("Free interconnect replacements", 0, 0, 0, 1),
    ("Supplemental advanced product replacement", 0, 0, 0, 1),
    ("sec", "PROACTIVE CARE"),
    ("Two semi-annual maintenance visits", 0, 0, 0, 1),
    ("Documented service checklists (ANSI/INFOCOMM 10-2013)", 0, 0, 0, 1),
    ("Firmware updates", 0, 0, 0, 1),
    ("Re-management of exposed cabling", 0, 0, 0, 1),
    ("Proactive monitoring &amp; remote repair*", 0, 0, 0, 1),
]

def tier_table():
    head = ('<thead><tr><th scope="col">What&#8217;s included</th><th scope="col">Standard Warranty<small>INCLUDED FREE</small></th>'
            '<th scope="col">Extended Warranty<small>WARRANTY</small></th><th scope="col">Silver SLA<small>SERVICE LEVEL</small></th>'
            '<th scope="col" class="g">Gold SLA<small>MOST COMPLETE</small></th></tr></thead>')
    rows = []
    for r in TIER_ROWS:
        if r[0] == "sec":
            rows.append(f'<tr><td class="sec" colspan="5">{r[1]}</td></tr>')
        else:
            G = ' class="g"'
            cells = "".join(f'<td{G if i == 3 else ""}>{Y if v else N}</td>' for i, v in enumerate(r[1:]))
            rows.append(f"<tr><td>{r[0]}</td>{cells}</tr>")
    return f'<div class="cvp-tw"><table class="cvp-t">{head}<tbody>{"".join(rows)}</tbody></table></div>'

PAGES["service-level-agreements"] = dict(
    label="Service Level Agreements", hero=f"{UP}/2023/03/UDOT-rack-3-scaled.jpg", css=CSS_TIERS,
    form_ref="SLA%20Page",
    title="Service Level Agreements",
    excerpt="ClearVista Service Level Agreements go beyond manufacturer warranties with extended support and labor coverage, faster response times, scheduled maintenance and proactive monitoring.",
    sections=[
        hero("SERVICE LEVEL AGREEMENTS", "Keep Critical Systems Running",
             "Support plans that go beyond the manufacturer warranty, with faster response, scheduled maintenance and proactive monitoring.",
             "Request SLA Pricing", "Compare Plans", "#cvp-tiers"),
        stats([("1 Day", "Response time with Gold"), ("2 Visits", "Semi-annual maintenance each year"),
               ("Proactive", "Monitoring and remote repair")]),
        intro("MORE THAN PRODUCT AND INSTALLATION", "Support That Protects Your Investment", [
            "Your systems only deliver value when they work. ClearVista offers levels of service beyond traditional manufacturer warranties, from extended support and labor coverage to proactive monitoring that catches issues before your users do.",
            "Every system we install includes our standard warranty support. When uptime matters, a Silver or Gold Service Level Agreement adds faster response times, discounted hardware, maintenance visits and remote support from the team that knows your system best."]),
        sec(f'<p class="cvs-eye">COMPARE PLANS</p><h2>Service Level Agreement Tiers</h2><p class="cvu-lead">Choose the coverage that matches how critical your systems are. Every tier builds on the one before it.</p><p class="cvp-swipe">Swipe to compare plans &#8594;</p>{tier_table()}'
            '<p class="cvp-tnote">*Remote support and proactive monitoring require hardware with OvrC capabilities. Reactive service visits cover up to two separate issues per month. Service and maintenance scheduling is subject to availability. '
            'Prefer a printable version? <a href="https://www.goclearvista.com/wp-content/uploads/2021/11/TVS-Pro-Service-Level-Agreements-2021.pdf" target="_blank" rel="noopener" style="color:#292d5b;font-weight:700;border-bottom:2px solid #d9a13a">Download the plan details (PDF)</a>.</p>',
            alt=True, id_="cvp-tiers"),
        cards("KEY BENEFITS", "What an SLA Adds", None, [
            ("RESPONSE", "Shorter Response Times", "Silver guarantees a response within two business days. Gold responds within one business day, with priority scheduling."),
            ("MAINTENANCE", "Scheduled Maintenance Visits", "Gold includes two semi-annual visits with cable management, a documented service checklist and firmware updates."),
            ("MONITORING", "Reactive or Proactive Support", "Remote support when hardware fails, or proactive monitoring with Gold so you don&#8217;t have to worry about outages."),
            ("HARDWARE", "Discounted Replacement Hardware", "When equipment is out of warranty, replacement products are discounted. Gold adds supplemental replacements to keep you running.")],
            cols=4, alt=False),
        steps("HOW IT WORKS", "Getting Started Is Simple", None, [
            ("Choose Your Coverage", "We review your systems and how critical they are, then recommend the right tier."),
            ("Onboard Your System", "We document your equipment and set up remote support and monitoring where supported."),
            ("Maintain &amp; Monitor", "Scheduled visits, firmware updates and monitoring keep small issues from becoming outages."),
            ("Respond Fast", "When something needs attention, you get a guaranteed response time from a team that already knows your system.")],
            alt=True),
        two_col(
            '<p class="cvs-eye">WHO IT&#8217;S FOR</p><h2 class="cvu-h">Built for Systems That Can&#8217;t Go Down</h2><p class="cvu-p">An SLA makes sense wherever downtime interrupts learning, operations, public meetings or revenue.</p>',
            chips(["Command &amp; Operations Centers", "Council &amp; Board Rooms", "Classrooms &amp; Lecture Halls", "Conference &amp; Huddle Rooms",
                   "Digital Signage Networks", "Production Studios", "Stadiums &amp; Venues", "Public Safety Facilities"])),
        faq([
            ("What does the standard warranty include?", "Every system includes 90 days of support and labor coverage plus standard phone support during business hours at no additional cost."),
            ("What&#8217;s the difference between Silver and Gold?", "Silver adds one year of support and labor coverage, extended phone support, remote support, service visits, discounted hardware and a two business day response time. Gold adds a one business day response, two semi-annual maintenance visits, firmware updates, free interconnect replacements, proactive monitoring and supplemental product replacement."),
            ("Can we get an SLA for equipment we didn&#8217;t buy from ClearVista?", "Our Service Level Agreements cover products and systems purchased from ClearVista, so we can stand behind the design, installation and equipment."),
            ("Do you follow an industry standard during maintenance visits?", "Yes. Each Gold maintenance visit includes a complete performance and verification checklist based on the ANSI/INFOCOMM 10-2013 standard."),
            ("How do I request service?", 'Call <a href="tel:801-486-5757">(801) 486-5757</a> during business hours or <a href="/service-request/">submit a service request</a> online.')],
            alt=False),
        related("sla"),
        cta("PROTECT YOUR SYSTEMS", "Request SLA Pricing", "Tell us about your systems. A ClearVista specialist will recommend the right coverage."),
    ])

# ---------------------------------------------------------------- 5. Experience Center
PAGES["experience-center"] = dict(
    label="Experience Center", hero=f"{UP}/2023/05/IMG-6694-scaled.jpg", css=CSS_EXP,
    form_ref="Experience%20Center",
    title="Experience Center",
    excerpt="Book a guided visit to the ClearVista Experience Center in Salt Lake City for hands-on demonstrations and side-by-side comparisons of displays, conferencing, audio, control and AV-over-IP systems.",
    sections=[
        hero("EXPERIENCE CENTER", "See Working Systems. Decide With Confidence.",
             "Book a guided visit to our Salt Lake City Experience Center for hands-on demonstrations and side-by-side comparisons, led by the people who design and install these systems.",
             "Book a Guided Visit", "What You Can Experience", "#cvp-demos"),
        stats([("Live", "Working systems, not brochures"), ("Side-by-Side", "Technology comparisons"),
               ("Zoom + Teams", "Meeting room demonstrations")]),
        intro("WHY VISIT", "Technology Is Easier to Choose When You Can Experience It", [
            "Technology changes quickly, and spec sheets only tell part of the story. Our Experience Center lets your team see, hear and use working systems before you commit to a design.",
            "Our specialists guide you through hands-on demonstrations and side-by-side comparisons, explain the options available, and show how each solution applies to your spaces and your people.",
            "You&#8217;ll leave with a clear sense of what will work for your organization, and a team ready to design, install and support it."]),
        cards("WHAT YOU CAN EXPERIENCE", "Solutions on Display", "Tell us what you&#8217;re planning when you book, and we&#8217;ll tailor your visit to the technologies that matter most to you.", [
            ("DISPLAYS", "Displays &amp; Direct View LED", "Compare LCD flat panels and direct view LED side by side for brightness, detail and viewing angles."),
            ("PROJECTION", "Projection Systems", "See projection for presentation, classroom and large-venue applications."),
            ("CONFERENCING", "Video Conferencing", "Join a meeting in working Zoom and Microsoft Teams rooms and see the difference good audio and cameras make."),
            ("SIGNAGE", "Digital Signage", "Explore signage displays and content that inform, direct and engage visitors."),
            ("DISTRIBUTION", "AV-over-IP", "Watch networked video and audio route across a building from a single interface."),
            ("AUDIO", "Microphones, Speakers &amp; Soundbars", "Hear how microphone and speaker choices affect meeting and presentation quality."),
            ("CONTROL", "Control &amp; Interactive Technology", "Try configurable control systems and interactive displays built for collaboration."),
            ("PRODUCTION", "Live Production &amp; PTZ Cameras", "See live production switching and pan-tilt-zoom cameras for streaming and events.")],
            cols=4, alt=True, id_="cvp-demos"),
        steps("YOUR VISIT", "What to Expect", None, [
            ("Book", "Choose a time that works for your team using the form below or by calling us."),
            ("Share Your Goals", "Tell us about your spaces, users and priorities so we can prepare relevant demonstrations."),
            ("Experience", "A specialist guides you through hands-on demos and side-by-side comparisons."),
            ("Plan Next Steps", "Leave with clear recommendations and a path to design, pricing and installation.")]),
        sec('<p class="cvs-eye">INSIDE THE EXPERIENCE CENTER</p><h2>Built for Hands-On Evaluation</h2><p class="cvu-lead">Meeting spaces, display walls and working demonstrations set up the way you&#8217;ll use them.</p>'
            f'<div class="cvp-gal"><img src="{UP}/2023/05/IMG-6698-scaled.jpg" alt="Meeting room demonstration in the ClearVista Experience Center" loading="lazy">'
            f'<img src="{UP}/2023/05/IMG_7113-scaled.jpg" alt="Video conferencing demonstration space" loading="lazy">'
            f'<img src="{UP}/2023/05/IMG_7119-scaled.jpg" alt="Collaboration technology on display" loading="lazy">'
            f'<img src="{UP}/2023/05/IMG_7125-scaled.jpg" alt="Conferencing equipment demonstration" loading="lazy"></div>', alt=True),
        two_col(
            '<p class="cvs-eye">WHO SHOULD VISIT</p><h2 class="cvu-h">Bring the Whole Decision Team</h2><p class="cvu-p">Visits work best when the people who will use, manage and approve the system can experience it together.</p>',
            chips(["IT &amp; AV Managers", "Facilities Teams", "Procurement &amp; Purchasing", "Architects &amp; Consultants",
                   "Educators &amp; Administrators", "Public Safety &amp; Operations Leaders", "Executives &amp; Decision-Makers"])),
        '<div class="cvp-visit"><div class="cvu-in"><p class="cvs-eye">PLAN YOUR VISIT</p><h2>Visit the Experience Center</h2><div class="cvp-vg"><div class="cvp-info">'
        '<div><small>ADDRESS</small><span>170 East 2100 South<br>Salt Lake City, UT 84115</span></div>'
        '<div><small>HOURS</small><span>Monday&#8211;Friday, 9:00am&#8211;5:00pm MST<br>Appointments recommended</span></div>'
        '<div><small>PHONE</small><a class="big" href="tel:801-486-5757">(801) 486-5757</a></div>'
        '<div><small>BOOK ONLINE</small><span><a href="#cvs-quote" style="border-bottom:2px solid #d9a13a">Book a guided visit &#8594;</a></span></div></div>'
        '<div class="cvp-map"><iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1511.8379539044017!2d-111.88732766131557!3d40.72515052555627!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x87528ac8a8c5dfe9%3A0x44d641e2bcf681c1!2sTVS%20Pro!5e0!3m2!1sen!2sus!4v1751574474350!5m2!1sen!2sus" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="ClearVista Experience Center location map" allowfullscreen></iframe></div>'
        '</div></div></div>',
        faq([
            ("Do I need an appointment?", "We recommend booking ahead so the right specialist is available and demonstrations are set up for your application."),
            ("Can we bring our whole team?", "Yes. Visits work best when the people who will use, manage and approve the system can experience it together."),
            ("Can you demonstrate a specific product?", "Tell us what you&#8217;re considering when you book. We&#8217;ll let you know what&#8217;s available to see and set up comparable technology where we can."),
            ("What if we can&#8217;t visit Salt Lake City?", 'Our <a href="/face-to-face-sales/">outside sales team</a> regularly visits organizations across Utah, Idaho, Nevada, Wyoming, Colorado and Montana to assess needs on site.'),
            ("What happens after the visit?", 'We&#8217;ll follow up with recommendations and next steps, from a <a href="/design-engineering/">design consultation</a> to a detailed proposal.')],
            alt=False),
        related("exp"),
        cta("BOOK A GUIDED VISIT", "See It for Yourself", "Tell us a little about your project and when you&#8217;d like to visit. A ClearVista specialist will confirm your appointment."),
    ])

# ================================================================ build
if __name__ == "__main__":
    meta = {}
    # Optional local preview: point UTAH_HTML at a saved copy of the live State of Utah page.
    utah_path = os.environ.get("UTAH_HTML", os.path.join(OUT, "..", "utah.html"))
    utah = open(utah_path, encoding="utf-8", errors="ignore").read() if os.path.exists(utah_path) else None
    start = utah.index("<style>.cvs-hero") if utah else 0
    end_marker = "state contract pricing.</p> </div></div>"
    end = utah.index(end_marker) + len(end_marker) if utah else 0
    for slug, p in PAGES.items():
        body, form_src = build(slug, p["label"], p["hero"], p["css"], p["sections"], p["form_ref"])
        meta[slug] = {"title": p["title"], "excerpt": p["excerpt"], "bytes": len(open(os.path.join(OUT, f"{slug}.divi.txt")).read())}
        if not utah:
            continue
        prev = utah[:start] + body + utah[end:]
        prev = re.sub(r"src='https://forms\.goclearvista\.com[^']*'", f"src='{form_src}'", prev)
        prev = prev.replace('<title>', '<title>PREVIEW ', 1)
        open(os.path.join(OUT, f"{slug}.preview.html"), "w").write(prev)
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
    print(json.dumps(meta, indent=1))
