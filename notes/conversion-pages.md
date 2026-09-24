# Conversion pages (tier 3) — solution detail pages

Template: `notes/visual-displays-code.html` (cvs- components; one Code module + a separate form section, no negative margin).
Section order: hero (crumb, eyebrow, H1, Request a Quote -> #cvs-quote, Call) · intro + environment chips ·
3 technology cards (bullets, "Get a recommendation") · dark "One Partner. Every Stage." with 4 service steps ·
6-photo install gallery · public-entity band (State of Utah Contract link, NO contract names/counts) + related solutions ·
CTA band #cvs-quote with phone · Zoho ContactaPro form (ref=<Page>).
Removed from old pages: wonderbox popup, "Our Installs" carousel, blog carousel.

Owner direction (2026-09-24):
- "One partner" is THE key message on these pages.
- Visual Displays: DVLED first, then "Large Format Displays & Video Walls", then Projection. No size/resolution constraints ("any size, any resolution — fits your vision").
- The 6 gallery photos are fine; owner will supply updated photos later.

| Page | ID | Backup (original) | Status |
|---|---|---|---|
| Visual Displays | 189477 | page-189477_2026-03-12T180848 | LIVE 2026-09-24 09:52 (page-189477_2026-09-24T095248) |
| Digital Signage | 247125 | page-247125_2025-07-02T144900 | LIVE 2026-09-24 10:03 (page-247125_2026-09-24T100344) |
| Video Conferencing | 247136 | page-247136_2026-04-13T102323 | LIVE 2026-09-24 11:39 (page-247136_2026-09-24T113915; IMG_3078-2 and Web-COnference-Room-2 excluded: TVS PRO branding) |
| Classroom Technologies | 189670 | page-189670_2025-07-02T145959 | LIVE 2026-09-24 11:57 (page-189670_2026-09-24T115742) (MA516 + T.V.S. Pro removed; diagrams shown as example designs, owner confirmed diagrams are NOT ClearVista-made: never caption them as ours) |
| Council Rooms | 247146 | page-247146_2025-06-12T130416 | preview sent 2026-09-24 (removed "well over 30 years": undersells vs AVI-SPL/Ford AV; owner rule: keep only claims that differentiate) |
| Command & Control | 186604 | page-186604_2026-04-13T100703 | preview sent 2026-09-24 |

Other: duplicate home page 253376 set to draft 2026-09-24 (backup page-253376_2026-09-24_drafted).
Preview script: `node scripts/mockvd.js` · live check: `node scripts/livevd.js`.
Build: `python3 scripts/build_solution.py notes/specs/<page>.json notes/<page>-code.html` then `node scripts/mockpage.js <slug> notes/<page>-code.html <outdir>`.
Save: `python3 scripts/wrap_divi.py notes/<page>-code.html "<Label>" "<ref>" <out.txt>` → pages.update; verify: `node scripts/livepage.js <slug> <outdir>`.
