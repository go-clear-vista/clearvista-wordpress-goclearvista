"""Build a solution conversion page from the Visual Displays template CSS + a page spec.
Usage: python3 scripts/build_solution.py <spec.json> <out.html>"""
import json,sys,html,re
U='https://www.goclearvista.com/wp-content/uploads/'
tpl=open('notes/visual-displays-code.html').read()
css=tpl[:tpl.index('</style>')+8]
s=json.load(open(sys.argv[1]))
css=css.replace('</style>','@media (max-width:980px){.cvs-gal a:nth-child(3):last-child{grid-column:1/-1}.cvs-gal a:nth-child(3):last-child img{aspect-ratio:2/1}}</style>')
css=re.sub(r'url\(https://www\.goclearvista\.com/wp-content/uploads/[^)]*\)','url('+U+s['hero_img']+')',css,1)
e=lambda t:t.replace('&','&amp;')
out=[css]
out.append(f'<div class="cvs-hero"><div class="cvs-hero-in"><p class="cvs-crumb"><a href="/av-solutions/">Solutions</a> / {e(s["crumb"])}</p><p class="cvs-eye">{e(s["eyebrow"])}</p><h1>{e(s["h1a"])} <br>{e(s["h1b"])}</h1><p class="cvs-sub">{e(s["sub"])}</p><div class="cvs-btns"><a class="cvs-btn p" href="#cvs-quote">Request a Quote</a><a class="cvs-btn s" href="tel:801-486-5757">Call (801) 486-5757</a></div></div></div>')
out.append(f'<div class="cvs-intro"><div class="cvs-intro-in"><h2>{e(s["intro_h"])}</h2><div><p class="cvs-p">{e(s["intro_p"])}</p><div class="cvs-env">'+''.join(f'<span>{e(c)}</span>' for c in s['chips'])+'</div></div></div></div>')
cards=''.join(f'<div class="cvs-tc"><img src="{U}{c["img"]}" alt="{e(c["alt"])}" loading="lazy"><div><h3>{e(c["h"])}</h3><p>{e(c["p"])}</p><ul>'+''.join(f'<li>{e(b)}</li>' for b in c['b'])+'</ul><a href="#cvs-quote">GET A RECOMMENDATION →</a></div></div>' for c in s['cards'])
out.append(f'<div class="cvs-sec"><h2>{e(s["tech_h"])}</h2><p class="cvs-lead">{e(s["tech_p"])}</p><div class="cvs-tech">{cards}</div></div>')
out.append(f'<div class="cvs-dark"><div class="cvs-sec"><p class="cvs-eye">WHY CLEARVISTA</p><h2>One Partner. Every Stage.</h2><p class="cvs-lead">{e(s["partner_p"])}</p><div class="cvs-steps"><a class="cvs-step" href="/design-engineering/"><em>01</em><strong>Design &amp; Engineering</strong><span>Needs assessments, system design and documentation.</span></a><a class="cvs-step" href="/custom-program-integration/"><em>02</em><strong>Custom Integration</strong><span>Control programming that makes every system work as one.</span></a><a class="cvs-step" href="/system-installation/"><em>03</em><strong>Installation</strong><span>Certified crews, from one room to multi-site rollouts.</span></a><a class="cvs-step" href="/service-level-agreements/"><em>04</em><strong>Service &amp; Support</strong><span>Service agreements that keep critical systems running.</span></a></div></div></div>')
gal=''.join(f'<a href="{U}{g[0]}" target="_blank" rel="noopener"><img src="{U}{g[0]}" alt="{e(g[1])}" loading="lazy">'+(f'<span class="cvs-gcap">{e(g[2])}</span>' if len(g)>2 else '')+'</a>' for g in s['gallery'])
if s.get('gal_contain'): out[0]=out[0].replace('</style>','.cvs-gal a{background:#fff;border:1px solid #e3e5ee}.cvs-gal img{object-fit:contain;background:#fff}.cvs-gcap{display:block;padding:12px 14px;border-top:3px solid #d9a13a;color:#292d5b;font-weight:800;font-size:15px}</style>')
out.append(f'<div class="cvs-sec"><h2>{e(s["gal_h"])}</h2><p class="cvs-lead">{e(s["gal_p"])}</p><div class="cvs-gal">{gal}</div></div>')
rel=''.join(f'<a href="{u}">{e(t)} →</a>' for t,u in s['related'])
out.append(f'<div class="cvs-band"><div class="cvs-band-in"><div><h3>Buying for a Public Entity?</h3><p>{e(s.get("band_p","Government and education buyers can purchase through our State of Utah cooperative contract, and we also serve out-of-state government and education customers."))}</p><a class="cvs-btn n" href="/state-of-utah-contract/">State of Utah Contract</a></div><div class="cvs-rel">{rel}</div></div></div>')
out.append(f'<div class="cvs-cta" id="cvs-quote"><div class="cvs-cta-in"><p class="cvs-eye">START A PROJECT</p><h2>{e(s["cta_h"])}</h2><p>Tell us about your space and goals. A ClearVista system engineer will follow up.</p><a class="cvs-ph" href="tel:801-486-5757">(801) 486-5757</a></div></div>')
h='\n'.join(out)
assert '[' not in h and ']' not in h
open(sys.argv[2],'w').write(h+'\n')
