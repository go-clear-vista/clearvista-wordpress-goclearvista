// Live check for company pages: node company-pages/livecheck.js <outdir> [slug...]
// 5 widths, horizontal overflow, broken images, form iframe, internal link status; brand search on the line card.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const out = process.argv[2] || '.';
const slugs = process.argv.slice(3).length ? process.argv.slice(3) : ['our-team', 'certifications-trainings', 'product-line-card', 'careers'];
(async () => {
  const b = await chromium.launch({ args: ['--ignore-certificate-errors'], proxy: { server: process.env.HTTPS_PROXY } });
  const links = new Set();
  for (const slug of slugs) {
    for (const [n, vp, m] of [['d', { width: 1440, height: 900 }, false], ['l', { width: 1280, height: 800 }, false], ['s', { width: 1024, height: 768 }, false], ['t', { width: 820, height: 1180 }, true], ['m', { width: 390, height: 844 }, true]]) {
      const c = await b.newContext({ viewport: vp, isMobile: m, hasTouch: m, ignoreHTTPSErrors: true });
      const p = await c.newPage();
      await p.goto(`https://www.goclearvista.com/${slug}/?nocache=${Date.now()}`, { waitUntil: 'load', timeout: 90000 });
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); } });
      await p.evaluate(() => Promise.all([...document.querySelectorAll('.cvs-hero ~ * img')].map(i => (i.loading = 'eager', i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })))));
      await p.waitForTimeout(1500);
      const r = await p.evaluate(() => ({
        sw: document.documentElement.scrollWidth, hero: !!document.querySelector('.cvs-hero'),
        imgs: [...document.querySelectorAll('.cvu-sec img,.cvc-p img,.cvc-logo img,.cvc-ph img')].length,
        broken: [...document.querySelectorAll('.cvu-sec img,.cvc-p img,.cvc-logo img,.cvc-ph img')].filter(i => !i.naturalWidth).map(i => i.src.split('/').pop()),
        form: ((document.querySelector('iframe[src*="forms.goclearvista.com"]') || {}).src || 'MISSING').split('?')[1],
        anchor: !!document.getElementById('cvs-quote'),
        links: [...document.querySelectorAll('.cvs-hero a,.cvu-sec a,.cvc-band a')].map(a => a.getAttribute('href')),
      }));
      r.links.filter(h => h && h.startsWith('/')).forEach(h => links.add(h));
      console.log(slug, n, vp.width, JSON.stringify({ ...r, links: undefined, overflow: r.sw > vp.width }));
      if (n === 'd' || n === 'm') { await p.evaluate(() => scrollTo(0, 0)); await p.screenshot({ path: `${out}/${slug}-live-${n}.png`, fullPage: true }); }
      if (slug === 'product-line-card' && n === 'd') {
        await p.fill('#cvc-q', 'crestron'); const shown = await p.$$eval('#cvc-logos .cvc-logo', e => e.filter(x => x.style.display !== 'none').length);
        await p.fill('#cvc-q', 'zzzz'); const none = await p.$eval('#cvc-none', e => getComputedStyle(e).display);
        console.log('  search crestron ->', shown, 'shown; zzzz -> fallback', none);
      }
      await c.close();
    }
  }
  const c = await b.newContext({ ignoreHTTPSErrors: true }); const p = await c.newPage();
  for (const u of links) { const r = await p.goto('https://www.goclearvista.com' + u, { timeout: 60000 }); console.log('link', u, r.status()); }
  await b.close();
})();
