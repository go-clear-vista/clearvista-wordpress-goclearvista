const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy: process.env.HTTPS_PROXY ? {server: process.env.HTTPS_PROXY} : undefined });
  const failed = new Set();
  for (const [name, vp, mobile] of [['desktop',{width:1440,height:900},false],['mobile',{width:390,height:844},true]]) {
    const ctx = await b.newContext({ viewport: vp, isMobile: mobile, hasTouch: mobile, ignoreHTTPSErrors:true });
    const p = await ctx.newPage();
    p.on('requestfailed', r => failed.add(new URL(r.url()).host));
    const t0 = Date.now();
    await p.goto('https://www.goclearvista.com/', { waitUntil: 'load', timeout: 90000 });
    console.log(name, 'load ms', Date.now()-t0);
    // trigger lazy load
    await p.evaluate(async () => { for (let y=0; y<document.body.scrollHeight; y+=600){ window.scrollTo(0,y); await new Promise(r=>setTimeout(r,250)); } window.scrollTo(0,0); });
    await p.waitForTimeout(2500);
    await p.screenshot({ path: `${name}-fold.png` });
    await p.screenshot({ path: `${name}-full.png`, fullPage: true });
    const h = await p.evaluate(() => document.body.scrollHeight);
    const ow = await p.evaluate(() => document.documentElement.scrollWidth);
    console.log(name, 'height', h, 'scrollWidth', ow);
    await ctx.close();
  }
  console.log('failed hosts', [...failed]);
  await b.close();
})();
