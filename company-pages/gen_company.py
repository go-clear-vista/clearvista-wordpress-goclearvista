#!/usr/bin/env python3
"""Redesign drafts for the company pages: Our Team, Certifications & Trainings, Product Line Card, Careers.

Reuses the component library and CSS from service-pages/gen.py (cvs-, cvu-, cvp- classes) and adds a few
company-page components prefixed cvc- (team cards, certification groups, logo wall, job listings).

    python3 company-pages/gen_company.py        # writes build/<slug>.divi.txt and build/<slug>-code.html

Preview on the live theme: node scripts/mockpage.js <slug> company-pages/build/<slug>-code.html <outdir>
"""
import json, os, re, sys, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "service-pages"))
from gen import (CSS_BASE, UP, hero, stats, sec, intro, cards, steps, two_col, ul, chips, faq, cta)  # noqa: E402

OUT = os.environ.get("OUT_DIR", os.path.join(HERE, "build"))
FORM_CONTACT = "https://forms.goclearvista.com/clearvista/form/ContactaPro/formperma/O7JlkryEddXItSwvNTodTFWnAsHCI4_YceBLw9NwsmE"
FORM_JOBS = "https://forms.goclearvista.com/clearvista/form/JobInterestForm/formperma/S5-laKfQAqqb2fQwunlNS7WcU7s-Hck5qJ2NnBoHo_k"

# ---------------------------------------------------------------- extra CSS
CSS_CO = (
    # team cards
    ".cvc-team{display:grid;grid-template-columns:repeat(var(--n,4),minmax(0,240px));gap:22px;justify-content:center}"
    ".cvc-p{background:#fff;border:1px solid #e3e5ee;border-top:3px solid #d9a13a;border-radius:6px;padding:26px 18px 22px;text-align:center;box-shadow:0 6px 20px rgba(41,45,91,.07)}"
    ".cvc-p img,.cvc-p .cvc-ini{display:block;width:132px;height:132px;border-radius:50%;object-fit:cover;margin:0 auto 16px;box-shadow:0 0 0 4px #fff,0 0 0 6px #d9a13a}"
    ".cvc-p .cvc-ini{display:flex!important;align-items:center;justify-content:center;background:#161834;color:#d9a13a;font-size:40px;font-weight:800;letter-spacing:.04em;line-height:1;margin-top:0}"
    ".cvc-p strong{display:block;color:#292d5b;font-size:19px;font-weight:800;line-height:1.25em}"
    ".cvc-p span{display:block;color:#595959;font-size:15px;line-height:1.45em;margin-top:4px}"
    ".cvc-grp{margin:0 0 44px}.cvc-grp:last-child{margin:0}"
    ".cvc-grp h3{color:#292d5b;font-size:22px;font-weight:800;text-align:center;margin:0 0 20px;padding:0}"
    ".cvc-grp h3:after{content:\"\";display:block;width:48px;height:3px;background:#d9a13a;margin:10px auto 0}"
    ".cvc-center{text-align:center}.cvc-center .cvu-lead{margin:0 auto}"
    # certification groups
    ".cvc-cert ul{list-style:none!important;margin:14px 0 0!important;padding:0!important}"
    ".cvc-cert li{list-style:none!important;color:#3d3f55;font-size:15px;line-height:1.45em;margin:0!important;padding:8px 0 8px 18px!important;border-top:1px solid #eef0f6;position:relative}"
    ".cvc-cert li:before{content:\"\";position:absolute;left:0;top:15px;width:7px;height:7px;border-radius:50%;background:#d9a13a}"
    ".cvc-cert.dk{background:#161834;border-color:#161834}.cvc-cert.dk strong{color:#fff}.cvc-cert.dk span{color:#c9cbe0}"
    ".cvc-cert.dk a{display:inline-block;margin-top:16px;color:#d9a13a!important;font-weight:800;font-size:14px;letter-spacing:.04em}"
    # logo wall
    ".cvc-find{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin:0 0 22px}"
    ".cvc-find input{flex:0 1 360px;min-width:0;padding:12px 14px;border:1px solid #cfd2e0;border-left:3px solid #d9a13a;border-radius:3px;font-size:16px;color:#292d5b;background:#fff;text-transform:none;letter-spacing:normal;font-weight:400}"
    ".cvc-find small{color:#595959;font-size:14px}"
    ".cvc-logos{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}"
    ".cvc-logo{display:flex;flex-direction:column;align-items:center;justify-content:center;background:#fff;border:1px solid #e3e5ee;border-radius:4px;padding:16px 12px 10px;min-height:108px;transition:border-color .2s,box-shadow .2s}"
    ".cvc-logo:hover{border-color:#d9a13a;box-shadow:0 8px 20px rgba(41,45,91,.1)}"
    ".cvc-logo img{display:block;max-width:100%;height:48px;object-fit:contain}"
    ".cvc-logo span{display:block;color:#595959;font-size:12px;line-height:1.3em;margin-top:8px;text-align:center}"
    ".cvc-none{display:none;color:#3d3f55;font-size:16px;padding:18px 20px;background:#fff;border-left:3px solid #d9a13a;border-radius:3px;margin:0}"
    ".cvc-none a,.cvc-band a.l{color:#292d5b!important;font-weight:700;border-bottom:2px solid #d9a13a}"
    # navy band with text + buttons
    ".cvc-band{background:#161834;color:#fff}"
    ".cvc-band-in{max-width:1240px;margin:0 auto;padding:44px 40px;display:flex;gap:30px;align-items:center;justify-content:space-between;flex-wrap:wrap}"
    ".cvc-band h2{color:#fff;font-size:28px;font-weight:800;margin:0 0 6px;padding:0;line-height:1.2em}"
    ".cvc-band p{color:#c9cbe0;font-size:16px;line-height:1.55em;margin:0;padding:0;max-width:680px}"
    ".cvc-band .cvs-eye{color:#d9a13a;padding:0 0 8px}"
    # photo split
    ".cvc-ph img{display:block;width:100%;border-radius:6px;box-shadow:0 20px 44px rgba(41,45,91,.18)}"
    ".cvc-ph{position:relative}.cvc-ph:before{content:\"\";position:absolute;right:-14px;bottom:-14px;width:45%;height:45%;border-right:4px solid #d9a13a;border-bottom:4px solid #d9a13a;border-radius:0 0 6px 0}"
    # benefits list in two columns
    ".cvc-ben{columns:2;column-gap:28px}.cvc-ben li{break-inside:avoid}"
    # job listings
    ".cvc-jobs details{background:#fff;border:1px solid #e3e5ee;border-left:3px solid #d9a13a;border-radius:4px;margin:0 0 14px}"
    ".cvc-jobs summary{cursor:pointer;list-style:none;padding:22px 60px 22px 24px;position:relative}"
    ".cvc-jobs summary::-webkit-details-marker{display:none}"
    ".cvc-jobs summary strong{display:block;color:#292d5b;font-size:21px;font-weight:800}"
    ".cvc-jobs summary span{display:block;color:#595959;font-size:14px;margin-top:4px}"
    ".cvc-jobs summary:after{content:\"+\";position:absolute;right:24px;top:20px;color:#d9a13a;font-size:30px;font-weight:400}"
    ".cvc-jobs details[open] summary:after{content:\"–\"}"
    ".cvc-job{padding:0 24px 24px}"
    ".cvc-job>p{color:#3d3f55;font-size:16px;line-height:1.65em;margin:0;padding:0 0 18px;max-width:900px}"
    ".cvc-job-g{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;border-top:1px solid #eef0f6;padding-top:20px}"
    ".cvc-job-g h4{color:#b07d1f;font-size:13px;font-weight:800;letter-spacing:.14em;margin:0 0 12px;padding:0}"
    ".cvc-job-g .cvu-ul li{font-size:15px;margin-bottom:10px!important}"
    ".cvc-job .cvs-btn{margin-top:22px}"
    # responsive
    "@media (max-width:980px){.cvc-team{grid-template-columns:repeat(3,minmax(0,1fr))}.cvc-logos{grid-template-columns:repeat(4,1fr)}"
    ".cvc-band-in{padding:40px 28px}.cvc-job-g{grid-template-columns:1fr 1fr}}"
    "@media (max-width:767px){.cvc-team{display:flex;flex-wrap:wrap;justify-content:center;gap:12px}.cvc-team .cvc-p{width:calc(50% - 6px)}.cvc-p{padding:18px 10px 16px}"
    ".cvc-p img,.cvc-p .cvc-ini{width:96px;height:96px;margin-bottom:12px}.cvc-p .cvc-ini{font-size:30px}.cvc-p strong{font-size:16px}.cvc-p span{font-size:13px}"
    ".cvc-grp{margin-bottom:34px}.cvc-logos{grid-template-columns:repeat(2,1fr);gap:8px}.cvc-logo{min-height:96px}.cvc-find input{flex:1 1 100%}"
    ".cvc-band-in{padding:34px 20px}.cvc-band h2{font-size:23px}.cvc-band .cvs-btn{flex:1 1 100%;text-align:center}"
    ".cvc-ben{columns:1}.cvc-ph:before{right:-8px;bottom:-8px}"
    ".cvc-jobs summary{padding:18px 50px 18px 16px}.cvc-jobs summary strong{font-size:18px}.cvc-job{padding:0 16px 18px}.cvc-job-g{grid-template-columns:1fr;gap:6px}}"
)

# ---------------------------------------------------------------- components
def band(eye, h2, p, buttons):
    b = "".join(f'<a class="cvs-btn {k}" href="{h}">{t}</a>' for k, t, h in buttons)
    return (f'<div class="cvc-band"><div class="cvc-band-in"><div><p class="cvs-eye">{eye}</p><h2>{h2}</h2><p>{p}</p></div>'
            f'<div class="cvs-btns">{b}</div></div></div>')

def person(name, title, img=None):
    if img:
        pic = f'<img src="{UP}/{img}" alt="{name}, {title}" loading="lazy">'
    else:  # no headshot yet: initials instead of the "No Picture Available" placeholder
        ini = "".join(w[0] for w in re.sub(r"&#?\w+;|'.*?'", "", name).split()[:2]).upper()
        pic = f'<span class="cvc-ini" aria-hidden="true">{ini}</span>'
    return f'<div class="cvc-p">{pic}<strong>{name}</strong><span>{title}</span></div>'

def team_group(title, people):
    n = min(len(people), 5)
    return f'<div class="cvc-grp"><h3>{title}</h3><div class="cvc-team" style="--n:{n}">' + "".join(person(*p) for p in people) + "</div></div>"

def cert_card(tag, title, items):
    return (f'<div class="cvu-c cvc-cert"><em>{tag}</em><strong>{title}</strong>'
            '<ul>' + "".join(f"<li>{x}</li>" for x in items) + "</ul></div>")

def job(title, meta, summary, groups, open_=False):
    g = "".join(f'<div><h4>{h}</h4>{ul(items)}</div>' for h, items in groups)
    return (f'<details{" open" if open_ else ""}><summary><strong>{title}</strong><span>{meta}</span></summary>'
            f'<div class="cvc-job"><p>{summary}</p><div class="cvc-job-g">{g}</div>'
            f'<a class="cvs-btn p" href="#cvs-quote">Apply for This Position</a></div></details>')

SERVICES = [  # Services menu order (CLAUDE.md)
    ("/design-engineering/", "Design &amp; Engineering", "Needs assessments, system design and documentation."),
    ("/system-installation/", "System Installation", "Certified crews, from one room to multi-site rollouts."),
    ("/custom-program-integration/", "Custom Programming &amp; Integration", "Control programming that makes every system work as one."),
    ("/service-level-agreements/", "Service Level Agreements", "Support plans that keep critical systems running."),
    ("/experience-center/", "Experience Center", "Book a guided visit to see working systems in action."),
]

def services_rel(eye, h2, lead=None):
    a = "".join(f'<a href="{u}"><strong>{t}</strong><span>{d}</span><em>EXPLORE &#8594;</em></a>' for u, t, d in SERVICES)
    ld = f'<p class="cvu-lead">{lead}</p>' if lead else ""
    return sec(f'<p class="cvs-eye">{eye}</p><h2>{h2}</h2>{ld}<div class="cvp-rel" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">{a}</div>', alt=True)

# ---------------------------------------------------------------- Divi wrapper
def divi(label, body, form_iframe, form_label):
    head = (f'[et_pb_section fb_built="1" admin_label="{label} Redesign" _builder_version="4.27.5" _module_preset="default" '
            'custom_margin="0px||0px||false|false" custom_padding="0px||0px||false|false" global_colors_info="{}"]'
            '[et_pb_row _builder_version="4.27.5" _module_preset="default" width="100%" max_width="100%" '
            'custom_margin="0px||0px||false|false" custom_padding="0px||0px||false|false" global_colors_info="{}"]'
            '[et_pb_column type="4_4" _builder_version="4.27.5" _module_preset="default" global_colors_info="{}"]'
            f'[et_pb_code admin_label="{label} Page" _builder_version="4.27.5" _module_preset="default" '
            'custom_margin="0px||0px||false|false" custom_padding="0px||0px||false|false" global_colors_info="{}"]')
    tail = '[/et_pb_code][/et_pb_column][/et_pb_row][/et_pb_section]'
    # Separate form section, no negative margin (same layout as scripts/wrap_divi.py).
    form = (f'[et_pb_section fb_built="1" admin_label="{form_label}" _builder_version="4.27.5" _module_preset="default" '
            'custom_margin="0px||0px||false|false" custom_padding="20px||20px||false|false" global_colors_info="{}"]'
            '[et_pb_row column_structure="1_5,3_5,1_5" _builder_version="4.27.5" _module_preset="default" global_colors_info="{}"]'
            '[et_pb_column type="1_5" _builder_version="4.27.5" _module_preset="default" global_colors_info="{}"][/et_pb_column]'
            '[et_pb_column type="3_5" _builder_version="4.27.5" _module_preset="default" global_colors_info="{}"]'
            f'[et_pb_code _builder_version="4.27.5" _module_preset="default" global_colors_info="{{}}"]{form_iframe}[/et_pb_code][/et_pb_column]'
            '[et_pb_column type="1_5" _builder_version="4.27.5" _module_preset="default" global_colors_info="{}"][/et_pb_column]'
            '[/et_pb_row][/et_pb_section]')
    return head + body + tail + form

def contact_form(ref):
    src = f"{FORM_CONTACT}?ref={urllib.parse.quote(ref)}"
    return f"<iframe aria-label='Contact a Pro' frameborder=\"0\" style=\"height:500px;width:99%;border:none;\" src='{src}'></iframe>"

def jobs_form(ref):
    src = f"{FORM_JOBS}?ref={urllib.parse.quote(ref)}"
    return f"<iframe aria-label='Job Interest Form' frameborder=\"0\" style=\"height:1450px;width:100%;border:none;\" src='{src}'></iframe>"

# ================================================================ PAGES
PAGES = {}

# ---------------------------------------------------------------- Our Team (185496)
PAGES["our-team"] = dict(
    id=185496, label="Our Team", hero=f"{UP}/2021/12/Employees-top.jpg",
    form=contact_form("Our Team"), form_label="Contact Form",
    sections=[
        hero("OUR TEAM", "The People Behind Every Project",
             "One in-house team designs, programs, installs and supports every system we deliver, so the people you meet at the start are the people who see it through.",
             "Talk to Our Team", "See Certifications", "/certifications-trainings/"),
        stats([("1953", "Solving technology problems since"), ("100+", "Authorized manufacturer brands"),
               ("CTS", "AVIXA-certified design staff"), ("In-House", "Design through long-term support")]),
        sec('<div class="cvc-center"><p class="cvs-eye">MEET THE TEAM</p><h2 class="cvu-h">Leadership, Sales and Operations</h2>'
            '<p class="cvu-lead">From your first conversation to long-term support, you&#8217;ll work directly with the ClearVista team.</p></div>'
            '<div style="height:36px"></div>'
            + team_group("Leadership Team", [
                ("Seth B.", "CEO", "2022/06/Seth-B.jpg"),
                ("Christopher &#8216;Bubba&#8217; B.", "Director of Operations", "2022/06/Bubba-B.jpg"),
                ("Dalton P.", "Director of Sales &amp; Marketing", "2022/06/Dalton-P.jpg")])
            + team_group("Sales", [
                ("Brent P.", "Account Manager", "2022/06/Brent-P.jpg"),
                ("Dan A.", "Account Manager", "2022/06/Dan-A.jpg"),
                ("James B.", "Account Manager", "2022/06/James-B.jpg"),
                ("Mike B.", "Account Manager", "2022/06/Mike-B.jpg"),
                ("Dave S.", "Inside Sales Associate", "2025/11/90C44927-E802-45C4-A8BD-59002B672BD9.jpeg")])
            + team_group("Operations", [
                ("Spencer E.", "Project Manager", "2026/03/Spencer-E-2.jpg"),
                ("Chris Isaacson", "Project Engineer", None),
                ("Ryan Long", "Project Manager", None)]), alt=True),
        two_col(
            '<p class="cvs-eye">CERTIFIED EXPERTISE</p><h2 class="cvu-h">Trained on the Systems We Deliver</h2>'
            '<p class="cvu-p">Our team holds manufacturer and industry certifications across displays, audio, control, networking and conferencing, including AVIXA&#8217;s Certified Technology Specialist (CTS) credential.</p>'
            '<p class="cvu-small">See the full list on our <a href="/certifications-trainings/">Certifications &amp; Trainings</a> page.</p>',
            chips(["AVIXA CTS", "Crestron DMC-D Certified Designer", "Extron Certified Control Professional", "Extron Network AV Specialist",
                   "Q-SYS Certified", "Audinate Dante Levels 1&#8211;3", "Shure Integrated Systems L1 &amp; L2", "HDBaseT Master",
                   "Sony Tatsu-Jin Master", "Zoom Rooms Accredited", "And more"])),
        services_rel("ONE TEAM. EVERY STAGE.", "What Our Team Delivers"),
        band("JOIN THE TEAM", "Want to Work With Us?",
             "We&#8217;re always looking for people with a passion for AV technology. See open positions and benefits.",
             [("p", "View Careers", "/careers/")]),
        cta("TALK TO OUR TEAM", "Ready to Start Your Next Project?",
            "Tell us about your space and goals. A ClearVista specialist will follow up."),
    ])

# ---------------------------------------------------------------- Certifications & Trainings (251672)
CERTS = [
    ("INDUSTRY", "Industry &amp; System Design", [
        "AVIXA Certified Technology Specialist (CTS)", "Crestron Digital Media Certified Designer (DMC-D)",
        "Extron Certified AV Associate", "Harman Core Curriculum Certification"]),
    ("AUDIO", "Audio &amp; DSP", [
        "Audinate Dante Certified Levels 1&#8211;3", "QSC Q-SYS Certified", "Shure Integrated Systems Certification Levels 1&#8211;2",
        "Shure Microflex Advanced Certified", "Extron Certified ProDSP Specialist", "D+M Group Advanced Certification"]),
    ("DISPLAYS", "Displays, LED &amp; Projection", [
        "Sony Tatsu-Jin Master Certified", "Sharp NEC Certified FA and FE Series DVLED Installer",
        "Epson FDA RG3 Projectors: Installer Certification", "Epson Integration Authorized Reseller", "Chief Certified Partner"]),
    ("CONTROL", "Control &amp; Automation", [
        "Extron Certified Control Professional", "Control4 Associate Installer", "Control4 Tech Certified",
        "Control4 Certified Automation Programmer"]),
    ("NETWORKING", "Networking &amp; Signal Distribution", [
        "Araknis Professional Certified Network Administrator (PCNA)", "Extron Certified Network AV Specialist",
        "Extron Certified XTP Engineer", "HDBaseT Master Certification"]),
    ("CONFERENCING", "Conferencing &amp; Collaboration", [
        "ClearOne ProAV Conferencing Certification", "Wolfvision Cynap",
        "Zoom Technical Sales Accreditation (ZTSA): Zoom Foundations", "ZTSA: Zoom Meetings &amp; Chat",
        "ZTSA: Zoom Phone", "ZTSA: Zoom Rooms"]),
    ("PRODUCTION", "Cameras, Production &amp; Security", [
        "NewTek 3Play Operation", "NewTek Certified Operator", "NewTek Live Production with TriCaster",
        "RED Certified/Authorized Dealer", "Panasonic i-PRO Certified Reseller"]),
]

PAGES["certifications-trainings"] = dict(
    id=251672, label="Certifications and Trainings", hero=f"{UP}/2022/08/design-engineering-header-2.jpg",
    form=contact_form("Certifications and Trainings"), form_label="Contact Form",
    sections=[
        hero("CERTIFICATIONS &amp; TRAINING", "Certified Specialists for Every System",
             "Looking for specialists? Our team is trained and certified by the industry and the manufacturers behind the systems we design, program, install and support.",
             "Contact a Pro", "Meet Our Team", "/our-team/"),
        stats([("CTS", "AVIXA-certified design staff"), ("100+", "Authorized manufacturer brands"),
               ("1953", "Solving technology problems since")]),
        intro("WHY IT MATTERS", "Certified on the Technology We Recommend", [
            "Manufacturer certifications mean our designers, programmers and installers know the products we recommend inside and out, from DSP configuration and control programming to direct view LED installation.",
            "Industry credentials such as AVIXA&#8217;s Certified Technology Specialist (CTS) mean our designs follow recognized standards. Together they help your system work the way it should on day one and keep working for years."]),
        sec('<p class="cvs-eye">OUR CERTIFICATIONS</p><h2>Certifications &amp; Training by Specialty</h2>'
            '<p class="cvu-lead">Here&#8217;s a list of some of our certifications and training.</p>'
            '<div class="cvu-4">' + "".join(cert_card(*c) for c in CERTS)
            + '<div class="cvu-c cvc-cert dk"><em>AND MORE</em><strong>Always Learning</strong>'
              '<span>Our team keeps adding certifications as technology changes. Looking for a specific credential? Ask a specialist.</span>'
              '<a href="#cvs-quote">CONTACT A PRO &#8594;</a></div></div>', alt=True),
        services_rel("PUT OUR EXPERTISE TO WORK", "Certified Teams at Every Stage"),
        cta("CONTACT A PRO", "Contact a Pro Today",
            "Tell us about your project and the expertise you need. A ClearVista specialist will follow up."),
    ])

# ---------------------------------------------------------------- Product Line Card (185025)
BRANDS = json.load(open(os.path.join(HERE, "brands.json")))
FIND_JS = ("<script>(function(){var q=document.getElementById('cvc-q');if(!q)return;q.addEventListener('input',function(){"
           "var v=q.value.toLowerCase().trim(),n=0;document.querySelectorAll('#cvc-logos .cvc-logo').forEach(function(e){"
           "var m=!v||e.getAttribute('data-b').indexOf(v)>-1;e.style.display=m?'':'none';if(m)n++;});"
           "document.getElementById('cvc-none').style.display=n?'none':'block';});})();</script>")

def logo(name, path):
    return (f'<div class="cvc-logo" data-b="{name.lower()}"><img src="{UP}/{path}" alt="{name} logo" loading="lazy">'
            f'<span>{name}</span></div>')

PAGES["product-line-card"] = dict(
    id=185025, label="Product Line Card", hero=f"{UP}/2022/09/Programming-and-integration-2.jpg",
    form=contact_form("Product Line Card"), form_label="Contact Form",
    sections=[
        hero("PRODUCT LINE CARD", "100+ Brands. One Partner.",
             "We&#8217;re an Authorized Dealer or Reseller for more than 100 manufacturers, and in many cases we buy and work directly with the manufacturer.",
             "Ask About a Brand", "Browse Our Brands", "#cvc-brands"),
        stats([("100+", "Authorized manufacturer brands"), ("Direct", "Manufacturer relationships"),
               ("1953", "Solving technology problems since")]),
        intro("WHY IT MATTERS", "The Right Equipment for Your Application", [
            "Because we carry so many lines, we recommend the equipment that fits your space, users and budget instead of steering you toward a single product line.",
            "Working directly with manufacturers gives our team access to product support and training, and it helps keep your project moving from design and procurement through installation and support."]),
        sec('<p class="cvs-eye">OUR TOP BRANDS</p><h2>Brands We Carry</h2>'
            '<p class="cvu-lead">We sell and have access to more brands than are shown here.</p>'
            '<div class="cvc-find"><input id="cvc-q" type="search" placeholder="Search brands, e.g. Crestron" aria-label="Search brands">'
            f'<small>{len(BRANDS)} brands shown</small></div>'
            '<div class="cvc-logos" id="cvc-logos">' + "".join(logo(n, p) for n, p in BRANDS) + '</div>'
            '<p class="cvc-none" id="cvc-none">Not listed here? We likely have access to it. Call <a href="tel:801-486-5757">(801) 486-5757</a> or <a href="#cvs-quote">send us a message</a>.</p>'
            + FIND_JS, alt=True, id_="cvc-brands"),
        band("NOT SEEING A BRAND?", "We Can Likely Get It",
             "We sell and have access to more brands than are listed here. Call us or send a message to see if we can help.",
             [("p", "Call (801) 486-5757", "tel:801-486-5757"), ("s", "Send a Message", "#cvs-quote")]),
        services_rel("ONE PARTNER. EVERY STAGE.", "More Than Equipment",
                     "The same in-house team that recommends your equipment designs, programs, installs and supports it."),
        cta("ASK ABOUT A BRAND", "Looking for a Specific Product?",
            "Tell us what you need. A ClearVista specialist will follow up with options and pricing."),
    ])

# ---------------------------------------------------------------- Careers (184914)
PAGES["careers"] = dict(
    id=184914, label="Careers", hero=f"{UP}/2023/03/UDOT-wall-install-2.jpg",
    form=jobs_form("Careers"), form_label="Job Interest Form",
    sections=[
        hero("CAREERS", "Join Our Team",
             "Come grow with a company that has over 70 years of passionate experience.",
             "Apply Now", "View Open Positions", "#cvc-jobs"),
        stats([("1953", "In business since"), ("4", "Core values in everything we do"),
               ("401K", "Plus profit sharing and paid time off")]),
        sec('<div class="cvu-2" style="align-items:center"><div><p class="cvs-eye">WHY WORK FOR US</p>'
            '<h2 class="cvu-h">Build What&#8217;s Next in AV Technology</h2>'
            '<p class="cvu-p">ClearVista is committed to being the most sought-after AV technology solutions partner in the Mountain West. Since 1953, we&#8217;ve consistently been recognized as industry leaders by the manufacturers we partner with, and we have appeared on several of CE Pro&#8217;s (Custom Electronics Professionals Magazine) nationwide yearly &#8216;top&#8217; lists.</p>'
            '<p class="cvu-p">We&#8217;re always looking for candidates who have a passion for AV technologies and are excited to bring our core values to their work. We offer competitive pay, benefits and advancement opportunities.</p></div>'
            f'<div class="cvc-ph"><img src="{UP}/2021/12/Top-Golf.jpg" alt="ClearVista team members at a company outing" loading="lazy" style="aspect-ratio:4/3;object-fit:cover;object-position:center 30%"></div></div>'),
        cards("OUR CORE VALUES", "Four Values in Everything We Do", None, [
            ("01", "Doing the Right Thing", "For our customers, our partners and each other."),
            ("02", "Driving Relationships", "Long-term relationships built on trust and follow-through."),
            ("03", "Being Passionate", "About the technology we work with and the work we do."),
            ("04", "Figuring Stuff Out", "If there&#8217;s a goal and no obvious way to reach it, we find one.")], cols=4),
        sec('<div class="cvu-2"><div><p class="cvs-eye">BENEFITS</p><h2 class="cvu-h">Benefits That Support You</h2>'
            '<p class="cvu-p">Full-time positions include a complete benefits package, plus the training and opportunities to grow your career.</p></div><div>'
            + ul(["Medical &amp; Dental Insurance", "Life Insurance", "Flexible Spending Account (FSA) or Health Savings Account (HSA)",
                  "Identity Theft Protection", "Profit Sharing", "401K", "Paid Time Off (PTO)", "Paid Holidays", "Bereavement Leave",
                  "Work From Home Options (dependent upon position)", "Paid Training", "Company Sponsored Activities", "Recognition Awards",
                  "Employee Discounts", "Employee Referral Program", "Self Improvement Compensation",
                  "Opportunities for Career Growth &amp; Advancement", "In-house Workout Room &amp; Equipment",
                  "Break/Lunch Room with Free Snacks &amp; Drinks"]).replace('class="cvu-ul"', 'class="cvu-ul cvc-ben"')
            + '</div></div>'),
        sec('<p class="cvs-eye">AVAILABLE CAREERS</p><h2>Open Positions</h2>'
            '<p class="cvu-lead">Interested in a position? Fill out the form below and upload your resume.</p><div class="cvc-jobs">'
            + job("Installer", "Full time &#183; $15&#8211;$19/hour depending on experience",
                  "Have a passion for hands-on work and technology? We&#8217;re looking for candidates who work well with their hands, have a passion for technology, like working in a team environment and interact well with customers at an install location. The ideal candidate maintains a professional, friendly persona in all types of situations and with all types of customers, and helps exceed customer expectations. Experience tipping cables, hanging TVs and/or projectors and other AV installation work is preferred, along with a thorough understanding of cabling standards.",
                  [("RESPONSIBILITIES", ["Participating in site manpower planning meetings",
                                         "Performing team installations on-site at customer locations, within given time parameters",
                                         "Using Zoho to communicate, log work and prepare required reports"]),
                   ("MINIMUM REQUIREMENTS", ["High school diploma or equivalent", "Pass a background check", "Clean driving record",
                                             "Ability to lift 100 lbs", "Not afraid of heights"]),
                   ("THIS POSITION", ["Full time (normally M&#8211;F, 8:00am&#8211;5:00pm)", "Full-time benefits",
                                      "Starting wage $15&#8211;$19/hour depending on experience", "Advancement opportunities available"])],
                  open_=True)
            + job("Sales Associate", "Full time &#183; $45K&#8211;$65K/year depending on experience",
                  "Have a passion for technology and helping people? We&#8217;re looking for associate candidates who will help customers find the right audiovisual solution for their needs. You&#8217;ll work with customers in-house at ClearVista, at the customer&#8217;s location or remotely. The ideal candidate has experience with Microsoft tools, maintains a friendly, professional persona in all types of situations and with all types of customers, and wants to exceed customer expectations.",
                  [("RESPONSIBILITIES", ["Answering phone calls, listening to customers&#8217; needs and directing them to the most appropriate sales account representative",
                                         "Visiting customer locations for walk-throughs and needs analyses to find the right technology solution and services for their budget",
                                         "Using Zoho to track customer orders, projects and installs"]),
                   ("MINIMUM REQUIREMENTS", ["High school diploma or equivalent", "Pass a background check", "Clean driving record"]),
                   ("THIS POSITION", ["Full time (normally M&#8211;F, 9:00am&#8211;5:00pm)", "Full-time benefits",
                                      "Yearly salary starts at $45K&#8211;$65K depending on experience", "Advancement opportunities"])])
            + '</div>', alt=True, id_="cvc-jobs"),
        cta("APPLY NOW", "Ready to Join ClearVista?",
            "Fill out the form below and upload your resume. We&#8217;ll be in touch."),
    ])

# ================================================================ build
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for slug, p in PAGES.items():
        css = CSS_BASE.replace("__HERO__", p["hero"]) + CSS_CO
        body = f"<style>{css}</style>" + "".join(p["sections"])
        html_only = re.sub(r"<style>.*?</style>", "", body)  # CSS keeps details[open], as on the live service pages
        assert "[" not in html_only and "]" not in html_only, f"{slug}: square bracket breaks Divi shortcodes"
        assert "showroom" not in html_only.lower() and not re.search(r"tvs ?pro|t\.v\.s", html_only, re.I), f"{slug}: banned wording"
        open(os.path.join(OUT, f"{slug}-code.html"), "w").write(body + "\n")
        content = divi(p["label"], body, p["form"], p["form_label"])
        open(os.path.join(OUT, f"{slug}.divi.txt"), "w").write(content)
        meta[slug] = {"live_id": p["id"], "bytes": len(content)}
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
    print(json.dumps(meta, indent=1))
