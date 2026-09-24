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
