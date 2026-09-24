// Screenshot a local preview page (built by gen.py with UTAH_HTML set) in chunks.
//
//   node tools/preview-shot.js <build-dir> <slug> <desk|mob> [out-dir]
//
// Uses the Chromium that Playwright finds (PLAYWRIGHT_BROWSERS_PATH) and routes
// through HTTPS_PROXY when set, so live theme CSS, fonts and images load.
const path = require('path');
const fs = require('fs');
let playwright;
try { playwright = require('playwright'); } catch { playwright = require('/opt/node22/lib/node_modules/playwright'); }

(async () => {
  const [buildDir, slug, tag = 'desk', outDir = path.join(buildDir, 'shots')] = process.argv.slice(2);
  if (!buildDir || !slug) { console.error('usage: preview-shot.js <build-dir> <slug> <desk|mob> [out-dir]'); process.exit(1); }
  fs.mkdirSync(outDir, { recursive: true });
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const b = await playwright.chromium.launch(proxy ? { proxy: { server: proxy } } : {});
  const w = tag === 'mob' ? 390 : 1440, scale = tag === 'mob' ? 1 : 0.5, chunk = tag === 'mob' ? 1400 : 1700;
  const p = await b.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: scale, ignoreHTTPSErrors: true });
  await p.goto('file://' + path.resolve(buildDir, `${slug}.preview.html`), { waitUntil: 'load', timeout: 60000 }).catch(e => console.log('nav', e.message));
  // Scroll through once so lazy-loaded images render.
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); });
  await p.waitForTimeout(1500);
  const top = await p.evaluate(() => { const e = document.querySelector('.cvs-hero'); return e ? e.getBoundingClientRect().top + scrollY : 0; });
  const bot = await p.evaluate(() => { const e = document.querySelector('.cvu-form-w') || document.querySelector('#cvs-quote'); return e ? e.getBoundingClientRect().bottom + scrollY : document.body.scrollHeight; });
  const sw = await p.evaluate(() => document.documentElement.scrollWidth);
  console.log(slug, tag, 'content', Math.round(top), '->', Math.round(bot), 'scrollWidth', sw, sw > w ? '(HORIZONTAL OVERFLOW)' : '');
  let i = 0;
  for (let y = top; y < bot; y += chunk, i++) {
    await p.screenshot({ path: path.join(outDir, `${slug}-${tag}-${i}.png`), fullPage: true, clip: { x: 0, y, width: w, height: Math.min(chunk, bot - y) } });
  }
  console.log('chunks', i, '->', outDir);
  await b.close();
})();
