# clearvista-wordpress-goclearvista
Website update repo for **goclearvista.com**.

This repo tracks the 2026 redesign. The site itself lives in WordPress (Extra theme with the Divi builder). This repo holds the memory, backups and build notes.

| Path | What's in it |
|---|---|
| `CLAUDE.md` | Project memory: goals, design system, site and access facts, the safe editing workflow, what's live, and what's pending. |
| `docs/conversation-log.md` | The full redesign discussion in order (user messages and Claude's replies). |
| `page-backups/` | The Divi content of each page (home 249762, Solutions 183940, Services 183281), saved as `page-<id>_<modified>.divi.txt` at every save, so any version can be restored. |
| `notes/*-steps.md` | Step-by-step instructions for the owner's Theme Builder edits (header button, footer). |
| `notes/*-code.html` | The HTML/CSS for each new section: home Why ClearVista, home About/contact, Solutions, Services, footer. |
| `notes/previews/` | Before, after and live screenshots at desktop, tablet and phone sizes. |
| `scripts/` | The Playwright scripts used to preview mockups and check the live pages. |

## Restoring a page
1. Open the backup file for the version you want.
2. Copy its contents.
3. Paste them into a `pages.update` call through the WordPress.com connector (see `CLAUDE.md` → Safe editing workflow).

WordPress also keeps its own page revisions under Page → Revisions.
