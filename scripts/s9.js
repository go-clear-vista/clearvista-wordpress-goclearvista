const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const tag = process.argv[2];
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['m',{width:390,height:844},true],['d',{width:1440,height:900},false]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(2000);
    for (let i=0;i<14;i++){ await p.mouse.wheel(0,400); await p.waitForTimeout(250); }
    const el = await p.$('.pa-dcm-blog-4'); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(3000);
    const bb = await el.boundingBox();
    console.log(tag,n,JSON.stringify({h:Math.round(bb.height), slick: await p.evaluate(()=>document.querySelectorAll('.slick-initialized').length), imgs: await p.evaluate(()=>[...document.querySelectorAll('.pa-dcm-blog-4 img')].map(i=>i.complete&&i.naturalWidth>0).filter(Boolean).length)}));
    await el.screenshot({path:`blogv-${tag}-${n}.png`});
    await c.close();
  }
  await b.close();
})();
