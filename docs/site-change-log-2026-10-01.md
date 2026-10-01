# Site change log: 2026-10-01

## Service Request page: Fluent Forms replaced with Zoho Forms

- **Page:** Service Request, ID 253966, https://www.goclearvista.com/service-request/ (header "Service Request" link; footer "Submit a Service Request").
- **Before:** Fluent Forms shortcode `fluentform id="3"` (free version, so no file uploads or conditional routing).
- **After:** Zoho Forms iframe `clearvista/form/ServiceRequest/formperma/FsgahFxyRZgJ-4H9BKLggH4kEuCAZ3wVciowbywl9KM`, `ref=Service Request`.
  - Fields: Name, Company, Email (required), Phone, Subject (required), Description (required), Order or Invoice Reference, Preferred contact method (Email/Phone), Image/Screenshot Upload, verification code.
  - Routing, set up and tested by ClearVista in Zoho: emails containing `@goclearvista.com` go to the IT/dev team (`dev@goclearvista.com`); all others go to scheduling.
- **Frame height:** 1700px desktop, 2100px under 768px. A small script also resizes the frame if Zoho posts its height (`perma|height` messages). No square brackets in the code module.
- **URL, title, template and menu items unchanged.** The Divi heading "Submit a Service Request" is kept.
- **Backups:** `page-backups/page-253966_2026-03-17T113522.divi.txt` (before), `page-backups/page-253966_2026-10-01T112824.divi.txt` (after, equals the saved content).
- **Verified live:** new iframe served on desktop and mobile caches, Fluent form gone, file-upload input present, no horizontal overflow at 1440px or 390px.
- **Not verified from Claude's environment:** the styled look of the form and its final height, because `static.zohocdn.com` was still blocked by the session's network policy. ClearVista to check the page on desktop and phone.

### Height adjustment (14:13)
- ClearVista hid the Zoho form title, which removes the duplicate heading.
- Their desktop screenshot showed the frame running about 220px past the form card: Zoho does not post its height, so the auto-resize script never fires. Frame height set to **1500px desktop** (was 1700) and **1800px under 768px** (was 2100, estimated, waiting on a phone screenshot).
- Backup: `page-backups/page-253966_2026-10-01T141322.divi.txt`. Verified live on desktop and mobile caches.

### Follow-ups
- Confirm the phone height from a phone screenshot.
- Fluent Forms form 3 is no longer used on this page. Leave it, or delete it in WP Admin once nothing else uses it.
