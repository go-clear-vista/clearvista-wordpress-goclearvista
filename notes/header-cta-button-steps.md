# Header "Talk to an Expert" button — saved steps

Adds a gold **Talk to an Expert** button in the site header, immediately to the right of the
search magnifying glass (desktop only). Built in Divi Theme Builder, because the Menu module
always places the search icon last, so a menu-item button would land *before* the icon.

Where: **wp-admin → Extra → Theme Builder → Default Website Template → Global Header (pencil icon)**

## 1. Right-align the menu
Menu module (grey outline) → gear → **Design → Text → Text Alignment: Right** → ✓
(Logo stays left; menu items + search icon move to the right.)

## 2. Add the Button module
Hover the Menu module → grey **+** below it → **Button**

- **Content**
  - Button Text: `Talk to an Expert`
  - Button Link URL: `/contact-us/` (the popup form only exists on the home page)
- **Design → Button**
  - Use Custom Styles For Button: **Yes**
  - Text Size: `15px` · Text Color: `#292d5b` · Background: `#d9a13a`
  - Border Width: `0` · Border Radius: `4px` · Font weight: **Bold**
  - Show Button Icon: **No**
- **Advanced → Visibility:** Disable on **Phone** and **Tablet**
- ✓

## 3. Name the column
Open the menu row's **column** settings (column gear, or the **Layers** icon bottom-right)
→ **Advanced → CSS Class:** `cv-navcol` → ✓ → **Save**

> The class goes on the **column** (the green outline that holds both the Menu and the
> Button), *not* on the Button module. If it is on the Button, the button drops below the logo.
> Also confirm the Button's **Button Background Color** saved as `#d9a13a`; if it shows no
> fill on the live site, re-pick it under **Design → Button → Button Background Color**.

## 4. Custom CSS
**Extra → Theme Options → General → Custom CSS** — add below the existing rules:

```css
/* Header CTA button (cv-navcol is on the header ROW) */
@media (min-width: 981px) {
  .cv-navcol { display: block !important; }
  .cv-navcol > .et_pb_column { display: flex !important; align-items: center; }
  .cv-navcol .et_pb_menu { flex: 1 1 auto; margin-bottom: 0 !important; }
  .cv-navcol .et_pb_button_module_wrapper { flex: 0 0 auto; margin: 0 0 0 20px !important; }
}
/* Small laptops: keep search + button on one line */
@media (min-width: 981px) and (max-width: 1150px) {
  .cv-navcol .et-menu > li { padding-left: 7px !important; padding-right: 7px !important; }
  .cv-navcol .et-menu > li > a { font-size: 15px !important; }
  .cv-navcol .et_pb_button_module_wrapper { margin-left: 12px !important; }
  .cv-navcol .et_pb_button_0_tb_header { font-size: 14px !important; }
}
```

**Save Changes**, then **clear the WP Rocket cache**.

## Checks afterwards
- Button sits on the same line, right after the magnifying glass (desktop).
- Hidden on tablet/phone.
- Clicking it opens `/contact-us/`.

## Already in Custom CSS (for reference, from the header top-bar fix)
```css
@media (max-width: 980px) {
  .cv-topbar .et_pb_column { margin-bottom: 4px !important; }
}
@media (max-width: 767px) {
  .cv-topbar .et_pb_text { text-align: center !important; }
}
```
