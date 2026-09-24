# Link-preview (Open Graph) share image

Problem (2026-09-24): sharing goclearvista.com in iMessage showed a blank grey card.
- Squirrly auto-picked `2026/03/AV-Solutions-featured-2-2.jpg` (540x304, TVS PRO branding) as og:image,
  with `og:image:width=500` and no height. The home page (249762) has no featured image.
- og:description still says "Since 1953".

Fix: `clearvista-share-1200x630.jpg` (Command & Control photo, navy gradient, tagline).
Rebuild: put `cc.jpg` (uploads/2021/10/Command-Control-scaled.jpg) and `logo-foot.png`
(uploads/2025/06/ClearVista-footer.png) next to `og.html`, then `node shot.js`.

Proposed description: "Enterprise AV integration for education, government and business.
Design, installation and support. Clarity in Technology. Vision for Tomorrow."

Status (2026-09-24 09:16 site time): LIVE. Owner uploaded the image (media ID 254173,
`uploads/2026/09/clearvista-share-1200x630-1.jpg`); Claude set it as the home page (249762)
featured image and added alt text. Squirrly now outputs og:image = that file, 1200x630.
Still open: og:description ("...Since 1953" meta description) - owner couldn't edit it in Squirrly.
