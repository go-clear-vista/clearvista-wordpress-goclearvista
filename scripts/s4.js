const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['d',{width:1440,height:520},false],['t',{width:820,height:600},true],['m',{width:390,height:700},true]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(2500);
    await p.screenshot({path:`hdr-${n}.png`});
    if (m) { const t = await p.$('.et_pb_menu_0_tb_header .mobile_menu_bar'); if (t) { await t.click().catch(()=>{}); await p.waitForTimeout(1200); await p.screenshot({path:`hdr-${n}-open.png`}); } else console.log(n,'no hamburger'); }
    console.log(n, await p.evaluate(()=>{const h=document.querySelector('header.et-l--header'); return {hdrH:Math.round(h.getBoundingClientRect().height), sw:document.documentElement.scrollWidth, logos:[...h.querySelectorAll('img')].filter(i=>i.offsetParent).length}}));
    await c.close();
  }
  await b.close();
})();
