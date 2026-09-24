const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['d',{width:1440,height:900},false],['d2',{width:1024,height:768},false],['t',{width:820,height:1180},true],['m',{width:390,height:844},true]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(2500);
    const info = await p.evaluate(()=>{
      const btns=[...document.querySelectorAll('header .et_pb_button, [class*=_tb_header] .et_pb_button')];
      const srch=document.querySelector('[class*=_tb_header] .et_pb_menu__search-button');
      const sr=srch&&srch.getBoundingClientRect();
      return {navcol:!!document.querySelector('.cv-navcol'), btns:btns.map(x=>{const r=x.getBoundingClientRect();const cs=getComputedStyle(x);return {t:x.textContent.trim(),href:x.getAttribute('href'),vis:x.offsetParent!==null&&r.width>0,x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),bg:cs.backgroundColor,c:cs.color,fs:cs.fontSize,fw:cs.fontWeight}}), search: sr?{x:Math.round(sr.x),y:Math.round(sr.y),w:Math.round(sr.width),h:Math.round(sr.height)}:null, sw:document.documentElement.scrollWidth, iw:innerWidth};
    });
    console.log(n, JSON.stringify(info));
    await p.screenshot({path:`cta-${n}.png`, clip:{x:0,y:0,width:vp.width,height:m?260:180}});
    if (n==='d') { const bt=await p.$('.cv-navcol .et_pb_button'); if (bt){ await bt.hover(); await p.waitForTimeout(600); await p.screenshot({path:'cta-d-hover.png', clip:{x:0,y:0,width:1440,height:180}}); } }
    await c.close();
  }
  await b.close();
})();
