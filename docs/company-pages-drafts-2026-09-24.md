# Company Pages Redesign — September 24, 2026

Four company pages were rebuilt in the redesigned style (same components and colors as the Services and Solutions pages). ClearVista approved the drafts and all four went **live on 2026-09-24**; the drafts were moved to the trash.

| Page | Live ID | Live URL | Draft ID | Form |
|---|---|---|---|---|
| Our Team | 185496 | /our-team/ | 254240 | Contact a Pro, `ref=Our Team` (new; the page had no form) |
| Certifications & Trainings | 251672 | /certifications-trainings/ | 254243 | Contact a Pro, `ref=Certifications and Trainings` (same ref as before) |
| Product Line Card | 185025 | /product-line-card/ | 254246 | Contact a Pro, `ref=Product Line Card` (new) |
| Careers | 184914 | /careers/ | 254245 | Job Interest Form, `ref=Careers` |

Preview a draft: `https://www.goclearvista.com/?page_id=<draft id>&preview=true` (logged in). Edit: `/wp-admin/post.php?post=<draft id>&action=edit`.

Source: `company-pages/gen_company.py` (imports the components and CSS from `service-pages/gen.py`). Built layouts: `company-pages/build/<slug>.divi.txt`; code-only files for previews: `company-pages/build/<slug>-code.html`. Brand list: `company-pages/brands.json`.

## What changed on each page

**Our Team**
- Photo hero, stats bar, and team cards grouped Leadership / Sales / Operations, with gold-ringed headshots.
- Chris Isaacson and Ryan Long had the "No Picture Available" placeholder; the draft shows navy initials badges until headshots exist.
- "DAVE S." shown as "Dave S." to match the others.
- New: certifications chips linking to the Certifications page, Services cards (menu order), a careers band, CTA, and the Contact a Pro form.
- Hero photo: `2021/12/Employees-top.jpg`. The old hero (`2023/01/TVS-Pro-2022-21-NEW.jpg`) shows TVS PRO shirts and signage, so it isn't used.

**Certifications & Trainings**
- The 34 certifications are grouped into 7 gold-topped cards by field, plus an "And more" card. No certification was added or removed.
- Typo fixes: "TriCasterooms" is now "TriCaster", "XTP engineer" is now "XTP Engineer" and "iPro" is now "i-PRO".
- The pop-up "Contact a Pro" button (`#wonderbox`) is replaced by an on-page CTA and form.
- Hero photo: `2022/08/design-engineering-header-2.jpg`. The old hero (`2023/02/Certifications-and-Training.jpg`) shows a TVS PRO banner.

**Product Line Card**
- The Supsystic gallery (shortcode `supsystic-gallery id=4`) is replaced by a responsive logo wall of the same 113 brands, with names under each logo and a live search box. The small search script contains no square brackets.
- Brand name fixes: "Stewart FIlmscreen" is now "Stewart Filmscreen" and "Control 4" is now "Control4".
- The copy keeps the published claims: 100+ brands, Authorized Dealer or Reseller, buys direct from manufacturers in many cases, access to more brands than listed.
- The old `tel:486-5757` link (missing its area code) is now `tel:801-486-5757`.

**Careers**
- Hero, stats, a "Why Work for Us" split with the Top Golf photo, core-values cards, a two-column benefits checklist, and the job openings as expandable cards (Responsibilities / Requirements / This Position).
- The Sales Associate copy said "in-house at TVS Pro"; it now says "in-house at ClearVista".
- The Job Interest form moved from `forms.tvsproslc.com` to `forms.goclearvista.com` (same form) and is tagged `ref=Careers`.
- Wages, hours, requirements and benefits are unchanged.

## Wording for the owner to check
- Core value one-liners (Careers) are new: "For our customers, our partners and each other.", "Long-term relationships built on trust and follow-through.", "About the technology we work with and the work we do.". The fourth reuses the Design & Engineering page line.
- The certification group names and which group each certification sits in.
- Hero headlines: "The People Behind Every Project", "Certified Specialists for Every System", "100+ Brands. One Partner.", "Join Our Team".

## Open items
1. Most headshots show a small TVS PRO logo on the shirt (everyone except Dave S.). New headshots are needed to remove it.
2. Headshots for Chris Isaacson and Ryan Long, and whether to show their last names as initials like everyone else.
3. The Installer posting says "tipping cables". Confirm the wording (possibly "terminating cables").

## Published 2026-09-24

| Page | Live ID | Saved (modified) | Backup before | Backup after |
|---|---|---|---|---|
| Our Team | 185496 | 15:16:08 | page-185496_2026-05-18T095419 | page-185496_2026-09-24T151608 |
| Certifications & Trainings | 251672 | 15:18:54 | page-251672_2026-04-13T103121 | page-251672_2026-09-24T151854 |
| Careers | 184914 | 15:22:47 | page-184914_2025-07-02T155404 | page-184914_2026-09-24T152247 |
| Product Line Card | 185025 | 15:25:40 | page-185025_2026-03-30T101656 | page-185025_2026-09-24T152540 |

- Live pages were unchanged since first read (checked `modified` before saving). Same URLs, slugs, templates and featured images, so menus and the footer need no change.
- Verified live: `python3 company-pages/verify_live.py` (rendered Code module matches the local build, correct form ref, no raw `et_pb_` shortcodes) and `node company-pages/livecheck.js <outdir>` (1440/1280/1024/820/390px: no horizontal overflow, no broken images incl. all 113 logos, brand search works, all internal links 200).
- Drafts 254240, 254243, 254245, 254246 moved to the trash.
- Rollback: WordPress Revisions on each page, or paste the "Backup before" file from `page-backups/`.
