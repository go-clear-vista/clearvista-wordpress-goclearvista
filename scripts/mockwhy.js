const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs=require('fs'); const html=fs.readFileSync('why.html','utf8');
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['d',{width:1440,height:900},false],['m',{width:390,height:844},true]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true, deviceScaleFactor:1 });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(1500);
    const before = await p.$('.et_pb_section_4'); await before.scrollIntoViewIfNeeded(); await p.waitForTimeout(1500);
    await before.screenshot({path:`why-before-${n}.png`});
    await p.evaluate(h=>{const s=document.querySelector('.et_pb_section_4'); const d=document.createElement('div'); d.id='cvnew'; d.innerHTML=h; s.replaceWith(d);}, html);
    await p.waitForTimeout(500);
    const el = await p.$('#cvnew'); await el.scrollIntoViewIfNeeded();
    await p.evaluate(()=>Promise.all([...document.querySelectorAll('#cvnew img')].map(i=>{i.loading='eager';return i.complete?1:new Promise(r=>{i.onload=i.onerror=r})})));
    await p.waitForTimeout(800);
    console.log(n, JSON.stringify(await el.boundingBox()), await p.evaluate(()=>document.documentElement.scrollWidth));
    if (n==='d') await el.screenshot({path:`why-after-d.png`});
    else { const bb=await el.boundingBox(); const y0=bb.y+await p.evaluate(()=>scrollY); let i=0; for(let y=0;y<bb.height;y+=1700,i++){ await p.screenshot({path:`why-after-m${i}.png`, fullPage:true, clip:{x:0,y:y0+y,width:390,height:Math.min(1700,bb.height-y)}}); } }
    await c.close();
  }
  await b.close();
})();
