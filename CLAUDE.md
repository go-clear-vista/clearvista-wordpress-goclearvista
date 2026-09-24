# ClearVista Website (goclearvista.com)

Working notes for updating the ClearVista WordPress site. ClearVista (DBA of TV Specialists, Inc.; formerly TVS Pro) is a Salt Lake City AV, security and communications integrator for enterprise, education and government.

## Site

- WordPress, Jetpack-connected, site ID **257551135**, managed through the WordPress.com connector.
- Theme: **Extra** (child theme) with the **Divi** builder and a Divi Theme Builder header/footer.
- Pages are Divi shortcode layouts. Redesigned pages use a single `[et_pb_code]` module holding scoped `<style>` + HTML, full-width template (`page-template-fullwidth.php`), and meta `_et_pb_use_builder: on`.
- Forms are Zoho Forms iframes (`forms.goclearvista.com`); tag each with a `ref` query value naming the page.
- Relevant plugins: WP Rocket (cache), Redirection (301s, permalink monitoring on), Squirrly SEO, Imagify.

## Style reference

Model new or updated pages on the redesigned **Home, Solutions (`/av-solutions/`), Services and State of Utah Contract** pages, and on competitors **AVI-SPL, Ford AV and CTI** (see `docs/competitor-research-summary.md`).

- Colors: navy `#161834` / `#292d5b`, gold `#d9a13a` (text-on-light gold `#b07d1f`), body `#3d3f55`, muted `#595959`, alt background `#f6f7fb`.
- Components (class prefixes `cvs-`, `cvu-`, `cvp-`): photo hero with gold eyebrow and two buttons, navy stats bar, intro split, gold-topped cards, numbered process steps, chips, dark project spotlight, FAQ accordion, related-services cards, dark CTA band, then the form.
- The reusable implementation is `service-pages/gen.py`.

## Content rules

- **Never "showroom" or retail language** on current pages. It is the **Experience Center**, framed as a guided visit. Historical pages and old blog posts may keep "showroom".
- Use only facts ClearVista has published (years, certifications, projects, plan details). No invented stats or guarantees.
- Services order everywhere (menu, Services grid): Design & Engineering, System Installation, Custom Programming & Integration, Service Level Agreements, Experience Center, Other Resources. Exception: the homepage strip keeps Integration before Installation, in the order projects happen.
- Never use `[` or `]` in page copy (Divi parses them as shortcodes).

## Workflow

1. **Drafts first.** Create a draft copy of the page (title suffix "(Redesign Draft)"). ClearVista approves before anything goes live.
2. To publish, copy the approved content onto the existing live page ID so the URL and menu items stay the same, then trash the draft.
3. Connector edits replace the whole page: fetch raw content with `pages.get` and `context: edit`, change only what's needed, and diff before and after with `service-pages/tools/page-text.py`.
4. Preview locally against the live theme CSS (`gen.py` with `UTAH_HTML`, then `tools/preview-shot.js`) at desktop 1440px and mobile 390px, and check for horizontal overflow.
5. Changing a slug: Redirection's permalink monitor now creates the 301 automatically; still confirm with `curl -I`.
6. Record live-site changes in `docs/` (see `docs/site-change-log-2026-09-24.md`).

## Environment notes

- Uploading media through the connector needs `public-api.wordpress.com` on the environment's network allowlist; otherwise ClearVista uploads in WP Admin → Media and shares the URL.
- Live screenshots: wait several seconds after load, or CSS background images appear missing.

## Company pages (Our Team, Certifications, Product Line Card, Careers)

Redesigned and **live 2026-09-24** (drafts trashed). Record: `docs/company-pages-drafts-2026-09-24.md`.

| Page | Live ID | Draft ID (trashed) | Form |
|---|---|---|---|
| Our Team | 185496 | 254240 | ContactaPro `ref=Our Team` |
| Certifications & Trainings | 251672 | 254243 | ContactaPro `ref=Certifications and Trainings` |
| Product Line Card | 185025 | 254246 | ContactaPro `ref=Product Line Card` |
| Careers | 184914 | 254245 | JobInterestForm `ref=Careers` |

- Build: `python3 company-pages/gen_company.py` (reuses `service-pages/gen.py` components; adds `cvc-` team cards, cert groups, logo wall, job cards). Brands live in `company-pages/brands.json`.
- Preview: `node scripts/mockpage.js <slug> company-pages/build/<slug>-code.html <outdir>`. Live check: `python3 company-pages/verify_live.py <slug>...` and `node company-pages/livecheck.js <outdir>`.
- Old hero photos `2023/01/TVS-Pro-2022-21-NEW.jpg` and `2023/02/Certifications-and-Training.jpg` show TVS PRO branding; don't reuse them. Most 2022 headshots have a small TVS PRO shirt logo (owner to replace).

## Solution pages (tier 3 conversion pages)

The seven solution detail pages under `/av-solutions/` were redesigned and went live on 2026-09-24. Full record: `docs/solution-pages-change-log-2026-09-24.md`. Status tracker: `notes/conversion-pages.md`.

| Page | ID | URL | Form `ref` |
|---|---|---|---|
| Command & Control | 186604 | /command-control-systems/ | Command & Control |
| Physical Security | 254056 | /physical-security/ | Physical Security |
| Video Conferencing | 247136 | /web-conferencing/ | Video Conferencing |
| Classroom Technologies | 189670 | /classroom-technologies/ | Classroom Technologies |
| Council Rooms | 247146 | /council-room/ | Council Rooms |
| Digital Signage | 247125 | /digital-signage-2/ | Digital Signage |
| Visual Displays | 189477 | /visual-displays/ | Visual Displays |

This is also the order of the header Solutions menu, the Solutions landing page cards (183940) and the footer Solutions column. Keep all four in step. Home Theater is not in any of them.

**Owner rules for these pages**
- **"One partner" is the key message** on every page (hero sub line, "One Partner. Every Stage." band, SEO descriptions).
- Keep a claim only if it sets ClearVista apart; drop any that make ClearVista look smaller than AVI-SPL, Ford AV or CTI (e.g. "30 years" was removed).
- No TVS / T.V.S. Pro branding in copy or photos. Photos showing TVS PRO on screens or signs are excluded.
- Never name state contracts (e.g. MA516) or give a contract count. Link to `/state-of-utah-contract/` only.
- The Classroom diagrams are not ClearVista's work. Never caption them "from our engineers" or similar.
- Visual Displays order: Direct View LED, then Large Format Displays & Video Walls, then Projection. No size or resolution limits ("any size, any resolution").

**How they're built**
- Spec per page: `notes/specs/<page>.json` (Visual Displays is hand-built in `notes/visual-displays-code.html`, which also supplies the shared CSS).
- Build: `python3 scripts/build_solution.py notes/specs/<page>.json notes/<page>-code.html` (output must contain no `[` or `]`; empty `gallery` skips the gallery).
- Preview on the live theme: `node scripts/mockpage.js <slug> notes/<page>-code.html <outdir>`.
- Wrap for Divi: `python3 scripts/wrap_divi.py notes/<page>-code.html "<Admin Label>" "<ref>" <out.txt>` (use "and", not "&", in the label). Produces the Code section plus a separate Zoho ContactaPro form section with **no negative margin** (the old -48px margin hid the CTA phone link).
- Save with `pages.update` (full content) after re-checking `modified`; confirm the saved content equals the local file; back up to `page-backups/page-<id>_<modified>.divi.txt`.
- Live check: `node scripts/livepage.js <slug> <outdir>` (1440/1280/1024/820/390px, overflow, all links, form ref).
- Phone H1: put a space before `<br>`; `.cvs-hero h1 br` is hidden on phones.

**SEO:** Squirrly titles and descriptions for all seven pages are in `notes/seo-solution-pages.md`, all verified live. The owner enters them in Squirrly → Bulk SEO → Edit Snippet; Claude verifies with `curl` and checks `og:image`.

**Footer:** current code in `notes/footer-code.html`, one-line paste version `notes/footer-code-paste.txt`, steps `notes/footer-update-steps.md`. Verified live 2026-09-24.

**Open items (waiting on the owner)**
1. Newer photos for Visual Displays (gallery), Video Conferencing, Command & Control and the Digital Signage hero.
2. Classroom share image is a manufacturer render; replace it.
3. Physical Security `og:image:width` reads 500 with no height (real size 1920×1080); re-selecting the image in Squirrly's Open Graph tab should fix it.
4. Hide or unpublish the Home Theater page.
5. The "One Partner. Every Stage." steps run Design, Integration, Installation, Support (project order, like the homepage strip), not the Services menu order. Ask whether to keep it.
6. The older memory branch `claude/zealous-keller-b29qex` (home and landing page history, conversation log) was never merged into main.
