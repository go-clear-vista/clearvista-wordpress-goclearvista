const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const html=require('fs').readFileSync('svcmock.html','utf8');
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['d',{width:1440,height:900},false],['m',{width:390,height:844},true]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/services/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(2000);
    await p.evaluate(h=>{const s0=document.querySelector('#et-boc .et_pb_section_0'); const s1=document.querySelector('#et-boc .et_pb_section_1'); const s3=document.querySelector('#et-boc .et_pb_section_3'); const d=document.createElement('div'); d.id='cvsvc'; d.innerHTML=h; s0.replaceWith(d); s1.remove(); if(s3) s3.remove(); const s2=document.querySelector('#et-boc .et_pb_section_2'); if(s2){s2.querySelectorAll('h1,h2,h3,p,strong').forEach(e=>{if(/Request a Free Demo/.test(e.textContent)) e.style.display='none'})}}, html);
    await p.evaluate(()=>Promise.all([...document.querySelectorAll('#cvsvc img')].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))));
    await p.waitForTimeout(1500);
    const el=await p.$('#cvsvc'); const bb=await el.boundingBox(); const y0=bb.y+await p.evaluate(()=>scrollY);
    console.log(n, Math.round(bb.height), await p.evaluate(()=>document.documentElement.scrollWidth));
    for (let y=0,i=0;y<bb.height;y+=2000,i++) await p.screenshot({path:`svcmock-${n}-${i}.png`, fullPage:true, clip:{x:0,y:y0+y,width:vp.width,height:Math.min(2000,bb.height-y)+ (y+2000>=bb.height?200:0)}});
    await c.close();
  }
  await b.close();
})();
