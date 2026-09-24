// Screenshot the top of a live page after it has fully loaded.
//
//   node tools/live-shot.js <url> <out.png> [width=1440] [height=900]
//
// Waits 8 seconds after scrolling so CSS background images (hero photos) load;
// shorter waits can show an empty grey hero even when the page is fine.
let playwright;
try { playwright = require('playwright'); } catch { playwright = require('/opt/node22/lib/node_modules/playwright'); }

(async () => {
  const [url, out, w = '1440', h = '900'] = process.argv.slice(2);
  if (!url || !out) { console.error('usage: live-shot.js <url> <out.png> [width] [height]'); process.exit(1); }
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const b = await playwright.chromium.launch(proxy ? { proxy: { server: proxy } } : {});
  const p = await b.newPage({ viewport: { width: +w, height: 1000 }, deviceScaleFactor: +w > 800 ? 0.5 : 1, ignoreHTTPSErrors: true });
  await p.goto(url, { waitUntil: 'load', timeout: 60000 });
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } window.scrollTo(0, 0); });
  await p.waitForTimeout(8000);
  console.log('height', await p.evaluate(() => document.body.scrollHeight), 'scrollWidth', await p.evaluate(() => document.documentElement.scrollWidth));
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: +w, height: +h }, fullPage: true });
  await b.close();
})();
