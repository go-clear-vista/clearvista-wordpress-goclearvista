# Service Page Redesign

Redesigned conversion pages that sit under **Services** on goclearvista.com, built in the same style as the live Home, Solutions, Services and State of Utah Contract pages.

| Page | Live page (ID) | Status |
| --- | --- | --- |
| Design & Engineering | `/design-engineering/` (250158) | Live |
| System Installation | `/system-installation/` (250199) | Live |
| Custom Programming & Integration | `/custom-program-integration/` (250190) | Live |
| Service Level Agreements | `/service-level-agreements/` (185332) | Live, five tiers from ClearVista_SLA_9-24-2026.pdf |
| Experience Center | `/experience-center/` (250210) | Live |

## How it works

`gen.py` holds the copy and a small component library (hero, stats bar, cards, process steps, spotlight, FAQ, tier table). It writes one Divi layout per page to `build/<slug>.divi.txt`: a single Code module with scoped CSS and HTML, followed by the Zoho demo/quote form section.

```sh
python3 gen.py                                   # regenerate build/*.divi.txt
UTAH_HTML=/path/to/saved-utah-page.html python3 gen.py   # also writes local previews
```

To publish a page, paste the `.divi.txt` content into the page (or send it through the WordPress connector) with the full-width template and the Divi builder enabled.

## Tools

| Script | Purpose |
| --- | --- |
| `tools/preview-shot.js <build-dir> <slug> <desk\|mob>` | Screenshot a local preview (needs `UTAH_HTML` builds) in chunks; flags horizontal overflow. |
| `tools/live-shot.js <url> <out.png>` | Screenshot the top of a live page after images load. |
| `tools/page-text.py <saved.html>` | Visible text of a saved page, for before/after diffs of live edits. |

The scripts use Playwright's Chromium and route through `HTTPS_PROXY` when set.

## Updating a page (runbook)

1. Edit the copy or components in `gen.py` and run `python3 gen.py`.
2. Preview: save the live State of Utah page (`curl -sL https://www.goclearvista.com/state-of-utah-contract/ -o utah.html`), run `OUT_DIR=/tmp/cv UTAH_HTML=utah.html python3 gen.py`, then `node tools/preview-shot.js /tmp/cv <slug> desk` and `... mob`.
3. Create a draft page with the new `build/<slug>.divi.txt` for approval.
4. On approval, update the live page ID with the same content, verify it live (`tools/live-shot.js`, then check for raw `[et_pb_` text in the HTML), and trash the draft.
5. Commit `gen.py` and `build/` so the repo matches the live site.

See `../docs/site-change-log-2026-09-24.md` for what changed on the live site, and `../CLAUDE.md` for site conventions.

## Notes

- Never use `[` or `]` in page copy; Divi treats them as shortcodes. `gen.py` asserts on this.
- `/walk-in-showroom/` 301-redirects to `/experience-center/` via the Redirection plugin (Tools → Redirection).
- SLA tier data lives in `TIER_ROWS` in `gen.py`; update it (and `SLA_PDF`) when the plan PDF changes.
- `previews/` contains local screenshots rendered against the live theme CSS.
