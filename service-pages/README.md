# Service Page Redesign

Redesigned conversion pages that sit under **Services** on goclearvista.com, built in the same style as the live Home, Solutions, Services and State of Utah Contract pages.

| Page | Live page (ID) | Draft |
| --- | --- | --- |
| Design & Engineering | `/design-engineering/` (250158) | **Live** (Sept 24) |
| System Installation | `/system-installation/` (250199) | 254198 |
| Custom Programming & Integration | `/custom-program-integration/` (250190) | 254199 |
| Service Level Agreements | `/service-level-agreements/` (185332) | 254200 |
| Experience Center | `/walk-in-showroom/` → `/experience-center/` (250210) | 254202 |

## How it works

`gen.py` holds the copy and a small component library (hero, stats bar, cards, process steps, spotlight, FAQ, tier table). It writes one Divi layout per page to `build/<slug>.divi.txt`: a single Code module with scoped CSS and HTML, followed by the Zoho demo/quote form section.

```sh
python3 gen.py                                   # regenerate build/*.divi.txt
UTAH_HTML=/path/to/saved-utah-page.html python3 gen.py   # also writes local previews
```

To publish a page, paste the `.divi.txt` content into the page (or send it through the WordPress connector) with the full-width template and the Divi builder enabled.

## Notes

- Never use `[` or `]` in page copy; Divi treats them as shortcodes. `gen.py` asserts on this.
- Internal links point to `/experience-center/` (the live Design & Engineering page temporarily links to `/walk-in-showroom/` until the slug changes). Change the Experience Center slug and add a 301 from `/walk-in-showroom/` before or with go-live.
- `previews/` contains local screenshots rendered against the live theme CSS.
