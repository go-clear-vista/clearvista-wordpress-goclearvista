const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['d',{width:1440,height:900},false],['t',{width:820,height:1180},true],['m',{width:390,height:844},true]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(2500);
    const el = await p.$('.cva'); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(800);
    const sec = await p.evaluateHandle(()=>document.querySelector('.cva').closest('.et_pb_section'));
    const bb = await sec.asElement().boundingBox();
    console.log(n, JSON.stringify({sw:await p.evaluate(()=>document.documentElement.scrollWidth), cva:await p.evaluate(()=>{const r=document.querySelector('.cva').getBoundingClientRect();return [Math.round(r.width),Math.round(r.height)]}), oldCall:await p.evaluate(()=>document.body.innerText.includes('Call US TODAY')), lb:!!(await p.$('.cva .wplightbox'))}));
    const y0=bb.y+await p.evaluate(()=>scrollY);
    await p.screenshot({path:`about-live-${n}.png`, fullPage:true, clip:{x:0,y:y0,width:vp.width,height:Math.min(bb.height,1800)}});
    if(n==='d'){ await p.click('.cva .b'); await p.waitForTimeout(2000); console.log('popup', await p.evaluate(()=>[...document.querySelectorAll('[class*=lightbox]')].some(e=>e.offsetParent&&e.getBoundingClientRect().height>200)));}
    await c.close();
  }
  await b.close();
})();
