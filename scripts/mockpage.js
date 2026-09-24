// Preview a code file on a live solution page (no save): node scripts/mockpage.js <slug> <code.html> <outdir>
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs=require('fs'); const slug=process.argv[2]; const html=fs.readFileSync(process.argv[3],'utf8');
const out=process.argv[4];
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['d',{width:1440,height:900},false],['t',{width:820,height:1180},true],['m',{width:390,height:844},true]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/'+slug+'/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.mouse.wheel(0,300); await p.waitForTimeout(2500); await p.evaluate(()=>scrollTo(0,0));
    await p.evaluate(h=>{const S=[...document.querySelectorAll('#et-boc .et_pb_section')].filter(s=>!s.closest('header,footer,.et-l--header,.et-l--footer'));
      const d=document.createElement('div'); d.id='cvvd'; d.innerHTML=h; S[0].replaceWith(d); S[1].remove(); S[2].remove(); S[4]&&S[4].remove();
      S[3].querySelectorAll('h5').forEach(e=>e.closest('.et_pb_row').remove()); const w=S[3].querySelector('#wonderbox'); w&&w.remove(); S[3].id='cvform'; S[3].style.marginTop='0'; d.after(S[3]);}, html);
    await p.evaluate(()=>Promise.all([...document.querySelectorAll('#cvvd img')].map(i=>(i.loading='eager',i.complete?1:new Promise(r=>{i.onload=i.onerror=r})))));
    await p.waitForTimeout(1500);
    const el=await p.$('#cvvd'); const bb=await el.boundingBox(); const y0=bb.y+await p.evaluate(()=>scrollY);
    console.log(n, 'height',Math.round(bb.height),'scrollWidth',await p.evaluate(()=>document.documentElement.scrollWidth),'vw',vp.width);
    const H=bb.height+500; for (let y=0,i=0;y<H;y+=1800,i++) await p.screenshot({path:`${out}/mock-${n}-${i}.png`, fullPage:true, clip:{x:0,y:y0+y,width:vp.width,height:Math.min(1800,H-y)}});
    await c.close();
  }
  await b.close();
})();
