const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const html=require('fs').readFileSync('footer.html','utf8');
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['d',{width:1440,height:900},false],['t',{width:820,height:1180},true],['m',{width:390,height:844},true]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/av-solutions/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(1500);
    const old=await p.$('footer.et-l--footer'); await old.scrollIntoViewIfNeeded(); await p.waitForTimeout(800);
    if(n==='d') await old.screenshot({path:'foot-before-d.png'});
    await p.evaluate(h=>{const f=document.querySelector('footer.et-l--footer'); f.innerHTML='<div id="cvfoot">'+h+'</div>';}, html);
    await p.evaluate(()=>Promise.all([...document.querySelectorAll('#cvfoot img')].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))));
    await p.waitForTimeout(600);
    const el=await p.$('#cvfoot'); await el.scrollIntoViewIfNeeded();
    console.log(n, JSON.stringify(await el.boundingBox()), await p.evaluate(()=>document.documentElement.scrollWidth));
    await el.screenshot({path:`foot-after-${n}.png`});
    await c.close();
  }
  await b.close();
})();
