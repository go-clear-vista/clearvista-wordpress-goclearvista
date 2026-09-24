# Solution pages redesign: change log (2026-09-24)

Archive of the session that redesigned the tier 3 "conversion pages" under Solutions. All times are site time. Every page has a backup from before and after each change in `page-backups/`.

## What the owner asked for, in order

1. Review the project notes and list the conversion pages.
2. Fix the grey iMessage link preview.
3. Redesign the solution pages and put them live, one at a time after approval.
4. Squirrly SEO titles and descriptions for each page.
5. Reorder the Solutions landing page cards to match the header menu.
6. Redesign Physical Security; send an updated footer with paste steps.
7. Put Physical Security live, give its Squirrly text, and check the footer.

## Changes made

### Link preview (iMessage)
- Made a 1200×630 share image (`notes/share-image/`). The owner uploaded it, since the connector can't upload media here, and it was set as the home page's featured image.
- The owner first edited the duplicate "New Homepage Redesign" page (253376) in Squirrly by mistake. That page was set to draft (backup `page-253376_2026-09-24_drafted`).

### Solution pages (all LIVE)

| Time | Page | ID | Notes |
|---|---|---|---|
| 09:52 | Visual Displays | 189477 | Reordered to Direct View LED, Large Format Displays & Video Walls, Projection. Size and resolution limits removed. |
| 10:03 | Digital Signage | 247125 | |
| 11:39 | Video Conferencing | 247136 | Two photos left out because they show TVS PRO branding. Share image changed to `Simple-Conference-Room-2.jpg`. |
| 11:57 | Classroom Technologies | 189670 | MA516 contract and T.V.S. Pro wording removed. Diagrams shown as example designs; the owner confirmed they are not ClearVista's work. |
| 12:21 | Council Rooms | 247146 | Headline shortened to "Council Chambers Built for Public Meetings". "30 years" removed. |
| 12:25 | Command & Control | 186604 | |
| 14:08 | Physical Security | 254056 | No gallery (only three security photos exist). Form `ref` changed from "Command & Control" to "Physical Security". |

Common layout, top to bottom:
1. Photo hero with breadcrumb, eyebrow, headline, "Request a Quote" and "Call" buttons.
2. Intro with environment chips.
3. Three technology cards.
4. Dark "One Partner. Every Stage." band with four service steps.
5. Install gallery.
6. Public-entity band (State of Utah Contract link, no contract names) plus related solution links.
7. Dark CTA band with phone number.
8. Zoho ContactaPro form with a per-page `ref`.

Removed from the old pages: the wonderbox popup, the "Our Installs" carousel, the blog carousel, and the form section's -48px margin, which hid the CTA phone link.

### SEO
- Squirrly titles and descriptions written for all seven pages (`notes/seo-solution-pages.md`). The owner entered them; each was verified live with `curl`.
- The Council Rooms description was first pasted with the Classroom text; it was fixed and re-verified.
- Physical Security share image set to `2026/04/Timeline-1_01_00_27_24.jpg`.

### Solutions landing page (183940)
- 13:42: seven cards in menu order (Command & Control, Physical Security, Video Conferencing, Classroom Technologies, Council Rooms, Digital Signage, Visual Displays), centered so the last row doesn't leave one card alone.
- The owner reordered the header menu to match and removed Home Theater from it.

### Footer (Theme Builder, pasted by the owner)
- Only the Solutions column changed: new order above, with Physical Security added.
- Verified live: matches `notes/footer-code-paste.txt` apart from attributes WordPress and Squirrly add automatically (`decoding="async"`, `rel="nofollow"`, `<br />`). No sideways scrolling at 1440 or 390px.

## Not touched
- The Services landing page (183281) and service detail pages: another session redesigned those (see `docs/site-change-log-2026-09-24.md`).

## Lessons for next time
- Previews on the live theme (`scripts/mockpage.js`) caught every layout bug before going live: the hidden phone link, "FORANY" in a headline (missing space before `<br>`), a lone last card on tablet, a lone gallery photo.
- Full-page phone screenshots can show lazy-loaded photos as blank. Scroll the page and check `naturalWidth` before calling it a bug.
- Playwright here needs `require('/opt/node22/lib/node_modules/playwright')`, `--ignore-certificate-errors`, the `HTTPS_PROXY` proxy and `ignoreHTTPSErrors`.
- The WordPress connector drops now and then; reload it with ToolSearch.

## Open items
See "Open items" in the Solution pages section of `CLAUDE.md`.
