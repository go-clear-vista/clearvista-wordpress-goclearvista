# goclearvista.com Change Log — September 24, 2026

All edits were made through the WordPress.com connector on site ID 257551135 (Divi / Extra theme). WordPress keeps a revision of every page edit, so any change below can be rolled back from the page's **Revisions** screen.

## Navigation

- **Main Menu Bar (menu 525), Services dropdown**, reordered to:
  1. Design & Engineering
  2. System Installation
  3. Custom Programming & Integration (renamed from "Custom Program & Integration")
  4. Service Level Agreements
  5. Experience Center
  6. Other Resources
- **Dropdown width:** CSS added by ClearVista in Divi → Theme Options → Custom CSS so labels no longer wrap:
  ```css
  .et_pb_menu_0_tb_header .nav li ul { width: 300px !important; }
  .et_pb_menu_0_tb_header .nav li li a { width: 260px !important; white-space: nowrap; padding: 6px 20px; }
  ```

## Service pages (redesigned and published)

| Page | ID | URL |
| --- | --- | --- |
| Design & Engineering | 250158 | `/design-engineering/` |
| System Installation | 250199 | `/system-installation/` |
| Custom Programming & Integration | 250190 | `/custom-program-integration/` |
| Service Level Agreements | 185332 | `/service-level-agreements/` |
| Experience Center | 250210 | `/experience-center/` (was `/walk-in-showroom/`) |

- Built from `service-pages/gen.py`; source layouts are in `service-pages/build/`.
- Each uses the full-width template with the Divi builder enabled, one Code module with scoped CSS, and the Zoho "Request a Free Demo or Quote" form tagged with a per-page `ref`.
- The SLA table follows `ClearVista_SLA_9-24-2026.pdf` (five tiers: Standard Warranty, Extended Warranty, Silver, Gold, Platinum). The PDF is in the media library at `/wp-content/uploads/2026/09/ClearVista_SLA_9-24-2026.pdf` and linked from the page.
- The review drafts (IDs 254192, 254198, 254199, 254200, 254202) were moved to the trash after publishing.

## "Showroom" removed from current pages

ClearVista no longer wants to suggest retail. Updated wording on:

- **Services (183281):** the card grid was reordered to match the menu, and "Walk-In Showroom" became "Experience Center", linked to `/experience-center/`.
- **Homepage (249762):** the Experience Center card copy was changed to "Book a guided visit to see working systems in action." and the card now links to `/experience-center/`.
- **About Us (184927):** "showroom and demo models" became "demo and display models". The visit block's "SHOWROOM / Visit our Walk-In Showroom" became "EXPERIENCE CENTER / Book a guided visit".
- **Contact Us (185238)** and **Face to Face Sales (189043):** "showroom" was replaced with "Experience Center".

Left as-is by decision, since they are historical (the business was retail then): History of T.V.S. Pro, About Ken Bollinger, the 2021 Remodel Open House page, older blog posts (including "TVS Pro Showroom Update"), the Old Pages list, and "Automotive Showrooms" as an industry name on the Sony Bravia page.

## Redirects

- **Redirection plugin** (v5.10.1) installed and activated. ClearVista completed setup with permalink monitoring on.
- **Rule:** `/walk-in-showroom/` → `/experience-center/`, 301, case- and trailing-slash-insensitive, query parameters passed through. Verified returning 301.
- A temporary meta-refresh page (ID 254204) covered the gap before the rule existed. It is now in the trash.

## Not changed

- Homepage services strip order (Integration 02, Installation 03) was kept on purpose, in the order projects happen.
- Home theater was left off the Experience Center list to keep it commercial.

## Environment notes

- Media uploads through the connector need `public-api.wordpress.com` on the environment's network allowlist. Until then, upload files in WP Admin → Media and share the URL.
- Connector page edits replace the whole page content, so fetch the current raw content first (`pages.get` with `context: edit`) and change only what's needed.
