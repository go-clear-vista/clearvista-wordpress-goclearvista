# ClearVista website (goclearvista.com) — project memory

This repo holds the working memory for redesigning **goclearvista.com**. The code lives in WordPress, not here. What's here:

- the decisions made
- how to edit the site safely
- the page content saved at each step
- the HTML/CSS for every new section
- screenshots
- the verification scripts

The full discussion is in `docs/conversation-log.md`.

## Goal and brand direction
- Look like the competitors we used as references: **AVI-SPL, Ford AV, CTI**.
- Look **"larger than we actually are"**: enterprise-grade, "this company can achieve ANYTHING".
  - Don't come across as a family business or small team.
  - Don't lean on "Since 1953". The owner considers it irrelevant and not a credential.
  - Don't market consumer or commodity tech (no Home Theater, no CE Pro).
- The rollout runs in three tiers:
  1. **Home page**: done except one photo.
  2. **Landing pages**: Solutions, Services, State of Utah Contract, About Us, Blog.
  3. **Conversion pages**: pages that entice visitors to contact us.
- Never invent claims, numbers or testimonials. Use only facts that are on the site or that the owner supplied.
  - Anonymise quotes by role; never make up a name. Example: "IT Specialist, Cancer Institute".
- Tagline: **"Clarity in Technology. Vision for Tomorrow."** Line under it: "Enterprise, Education and Government".

## Design system (used on every rebuilt section)

**Colours**

| Colour | Hex | Use |
|---|---|---|
| Navy | `#292d5b` | Brand |
| Deep navy | `#161834` | Dark bands, footer |
| Gold | `#d9a13a` | Accents, primary buttons |
| Dark gold | `#b07d1f` | "EXPLORE →" link text |
| Light panel | `#f3f4f8` | Card and chip backgrounds |
| Body text | `#3d3f55` or `#595959` | Paragraphs |

**Type**
- Theme font (Open Sans). Headings are weight 800; the theme uppercases h2.
- Eyebrow labels: gold, weight 800, letter-spacing `.18em`, 12–14px.

**Components**
- **Buttons:** primary is gold with navy text, 4px radius, padding 14px 26px. Secondary is a white outline on dark backgrounds.
- **Hero:** a photo under the gradient `linear-gradient(180deg, rgba(20,22,52,.55), rgba(20,22,52,.88))`, with left-aligned text.
- **Cards:** white, 1px border `#e3e5ee`, 6px radius, a soft shadow and a 3px gold top border. On phones they become a horizontal row: a 118px image, then the text.
- **Breakpoints:** 980px (tablet) and 767px (phone). Test at 1440, 1280, 1024, 820 and 390px.

**CSS class prefixes**

| Prefix | Section |
|---|---|
| `cvw-` / `cvq-` | Home Why ClearVista + testimonials |
| `cva-` | Home About + contact card |
| `cvs-` | Solutions and Services pages |
| `cvf-` | Footer |
| `cv-tiles`, `cv-logos`, `cv-certs`, `cv-call`, `cv-ind` | Home rows |
| `cv-topbar`, `cv-navcol` | Header |

## Site and access facts

**Platform**
- Self-hosted WordPress 7.1.2. Theme: Extra / Extra-child, with Divi Builder 4.27.5.
- Other plugins:
  - WP Rocket (cache).
  - Divi Carousel Maker (slick).
  - Wonder Lightbox: the popup `#wonderbox`, opened by any link with class `wplightbox` and `href="#wonderbox"`. It exists on the **home page only**; other pages link to `/contact-us/`.
  - Squirrly and UpdraftPlus.
- Forms are Zoho, embedded from forms.goclearvista.com as iframes.

**How Claude edits the site**
- Editing goes through the **WordPress.com MCP connector**, which works via Jetpack plus a paid Jetpack AI plan.
  - Site ID `257551135`. Account `daltonptvspeccom`.
- **Never ask for or accept the WordPress password.**

**Page IDs**

| Page | ID | URL |
|---|---|---|
| Home | `249762` | https://www.goclearvista.com/ |
| Solutions | `183940` | /av-solutions/ |
| Services | `183281` | /services/ |

**What the owner edits by hand** (the connector can't reach these)
- **Theme Builder** header and footer: wp-admin → Extra → Theme Builder → Default Website Template.
- **Custom CSS**: Extra → Theme Options → General → Custom CSS.
- Claude writes step-by-step instructions for these; see `notes/*-steps.md`.

## Safe editing workflow (always follow)
1. The `page-sections.*` operations fail on Divi shortcode content, so always use **`pages.update` with the full content** and `user_confirmed: true`.
2. Before saving:
   - Get the owner's approval.
   - Re-check the page's `modified` value, so someone else's edit isn't overwritten.
   - Snapshot the live HTML.
3. Preserve exact characters:
   - The non-breaking space in "industry organizations. " on the home page.
   - `\r` after "Industries We Serve".
   - Tabs in the blog code module.
   - Curly quotes (`’`, `“`).
4. New sections go in as **one Code module** holding minified HTML and CSS:
   - Put everything on one line; the builder turns newlines into line-break holders.
   - Don't use `[` or `]`, because they break shortcodes.
5. Divi attribute gotchas:
   - The gradient overlay needs `use_background_color_gradient="on"` plus `_stops`, `_start`, `_end` and `background_color_gradient_overlays_image="on"`.
   - Responsive values use the `_tablet` and `_phone` suffixes plus `*_last_edited="on|phone"`.
6. After saving:
   - Verify with Playwright at desktop, tablet and phone sizes.
   - Check `scrollWidth` equals the viewport width (no sideways scroll).
   - Check that links and popups work.
   - Screenshot the result and send it to the owner.
7. Playwright notes:
   - Launch with `--ignore-certificate-errors` and proxy `process.env.HTTPS_PROXY`.
   - WP Rocket delays JavaScript until the user interacts, so move the mouse or wheel-scroll before measuring.
   - This environment blocks `static.zohocdn.com`, so Zoho forms render blank in screenshots. That's expected; real visitors see them.
8. Prefer a one-line Custom CSS fix over sending the owner back into Theme Builder (see the header and footer fixes).

## What's live now (as of 2026-09-23 21:19 site time)

### Header (Theme Builder, built by the owner)
- A thin top bar:
  - Left: tap-to-dial (801) 486-5757.
  - Right: SERVICE REQUEST and CAREERS.
- A white bar with the logo, menu (Solutions, Services, State of Utah Contract, About Us, Blog) and search.
- A gold **Talk to an Expert** button that links to /contact-us/.
  - Desktop only; hidden at 980px and below.
  - The class `cv-navcol` sits on the header **row**. The CSS, including a 981–1150px rule that tightens the menu, is in `notes/header-cta-button-steps.md`.

### Home page (latest backup `page-backups/page-249762_2026-09-23T211144.divi.txt`), top to bottom
1. **Hero.** Background IMG_5175 (a video-wall venue photo) with a navy gradient. The "Mobile Layout CSS" code module lives inside this section.
2. **Five tiles:** Technology Solutions, Professional Services, State Contracts, About Us, Blog.
   - The **About Us tile still shows the vintage storefront photo.** Waiting on a new photo.
3. **About + contact card.** "A Full-Service Technology Integrator" on the left; on the right a navy card with "Talk to an Expert", the phone number and a "Contact Us Now" button that opens the popup.
4. **Logos and certifications:** five member logos (AVIXA, CTS, Edge Technology, NSCA, ProSource) and a "See our Certifications" button.
5. **Popup section** (`#wonderbox`): heading "Contact ClearVista!" plus the Zoho form.
6. **Industries We Serve:** a 12-item grid.
7. **Why ClearVista.**
   - Headline: "One Partner. Every Stage. Any Scale."
   - Photo: fire station install (`Timeline-1_01_00_01_28.jpg`). The owner approved it and will replace it later.
   - Five capability cards.
8. **"Trusted When It Matters Most": three quotes.**
   - IT Specialist, Cancer Institute (lightly edited from the real quote).
   - Alexander Lee.
   - Tom Chamberlain.
   - The Chris Forbes quote was removed because it mentions "TVS" and a gear store.
9. **Blog carousel:** heading "Inside Our Latest Projects".
   - On mobile it falls back to a scroll strip if the carousel script doesn't load.

### Solutions page (backup `page-183940_2026-09-23T211921.divi.txt`; original in `..._2026-04-13...`)
- **Hero:** Command & Control photo. Buttons: "Request a Demo or Quote" (jumps to `#cvs-quote`) and "Our Services".
- **"Proven Across Every Environment":** intro copy with environment labels.
- **Six cards.**
  - Video Conferencing reads "Meeting rooms built for Microsoft Teams and Zoom."
  - **Home Theater is removed** from Solutions; its own page still exists.
- **"Let's Talk About Your Project" band** above the existing Zoho form.

### Footer (Theme Builder, built by the owner)
- A single Code module; the code is in `notes/footer-code.html` and the install steps in `notes/footer-rebuild-steps.md`.
- Layout:
  - A "Ready to start your next project?" CTA bar.
  - Four columns: brand and social, Solutions, Company, Contact.
  - A legal bar: © 2026, "ClearVista is a DBA of TV Specialists, Inc.", Privacy, Terms, Archived Pages.
- Full width comes from Custom CSS: `.et-l--footer .et_pb_row:has(.cvf){width:100%!important;max-width:100%!important;padding:0!important;margin:0!important}`.
- The BBB seal and Google-review badge were removed. "Store hours" now reads "Office Hours".

### Services page (backup `page-183281_2026-09-23T214859.divi.txt`; original in `..._2025-07-02...`)
- **Hero:** "Professional Services" over the team photo.
- **"One Team. Every Stage.":** Utah's first Authorized Professional Panasonic dealer, 100+ brands, link to the Product Line Card.
- **Six service cards.** Two card photos were swapped to remove the TVS Pro banners:
  - Design & Engineering → `2022/08/Design-Engineering-Feature`.
  - Walk-In Showroom → `2023/05/IMG-6694`.
- **Delta Center "Project Spotlight":** arena photo, "900+ pieces of equipment installed", Sound & Communications feature, link to the blog story. The owner approved keeping "(then TVS Pro)" because the published article names TVS Pro.
- **"Let's Talk About Your Project" band** above the Services form (`?ref=Services`).
- The "Did You Know?" puzzle section was removed.

### State of Utah Contract page (ID 183285; backup `page-183285_2026-09-23T215901`; original `..._2025-07-02...`)
- **Hero:** "Buy Smarter Through the State Contract" over the SLC skyline. Buttons: "Request Contract Pricing" (#cvs-quote) and "Institution Portals" (#cvu-portals).
- **Facts band:** 5-year price guarantee · 10,000s of products · Beyond Utah (out-of-state government and education served).
- **The owner said the LCD & DLP Projectors and Integrated Classroom Solutions contracts are no longer held.** The contract cards and the "3 contracts" stat were removed at their request. **Never list specific contracts or a contract count** without confirming with the owner first. The page excerpt was also rewritten; it used to say "T.V.S. Pro… three contracts".
- **Sections:** Why buy through a cooperative contract (check list plus the Utah training link) · Designed, Installed and Supported (with the SLA link) · "Products Available on Contract" labels · Need Funding (3 cards: grants.gov, utahgrants, Panasonic) · the 6 institution portal buttons · the CTA band · the form (`ref=State of Utah Contract`).

### About Us page (ID 184927 at /about-us-2/; backup `page-184927_2026-09-23T220350`; original `..._2026-04-13...`)
- **Hero:** "About ClearVista" over the DVLed lobby photo.
- **Facts band:** Hundreds of organizations · 100+ brands · State of Utah contract provider · 900+ pieces at the Delta Center.
- **Our Story:** Ken Bollinger photo and a timeline (1953 TV Specialists → 1966 Panasonic → 2013 TVS Pro → today ClearVista). The "repair business", "home video electronics" and "CE Pro" wording was dropped.
- **Clients:** a custom 29-logo grid replaces the Supsystic gallery shortcode (id 6), which was huge and absolutely positioned. It sits above a collapsible list of 114+ client names, open on desktop and collapsed on phone and tablet. Obvious typos fixed: Hill Air Force Base, Utah County Auditor's Office, Latter-day Saints.
- **FAQs:** rebuilt as `<details>`. "TVS Pro order products" now reads "ClearVista". The used-equipment phone number was changed from "1-800-486-5757" to (801) 486-5757; **ask the owner whether the 800 number was real.**
- **Visit or contact:** phone, address, hours, showroom link, Google map, contact form (`ref=About Us`).

## Waiting on the owner
**Photos:**
- the About Us tile on the home page
- a larger Why ClearVista project photo
- a real team/showroom photo for the Services cards if one exists

**Follow-ups:**
- Clear the WP Rocket cache after each hand edit.
- The home page's preload link may still reference the old conference room photo until the cache is cleared.

**Owner's plan:** once every change is done, the owner reviews the whole site and sends specific change requests.

## Next up
1. Blog.
2. The "conversion pages" (tier 3).

Reuse the `cvs-` components so every landing page matches.
