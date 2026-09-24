const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['d',{width:1440,height:900},false],['t',{width:820,height:1180},true],['m',{width:390,height:844},true]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/av-solutions/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(1500);
    for (let i=0;i<12;i++){ await p.mouse.wheel(0,500); await p.waitForTimeout(150); }
    await p.evaluate(()=>window.scrollTo(0,0)); await p.waitForTimeout(1500);
    const info=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,H:document.documentElement.scrollHeight,cards:document.querySelectorAll('.cvs-card').length,imgs:[...document.querySelectorAll('.cvs-card img, .cvs-hero')].length,broken:[...document.querySelectorAll('.cvs-card img')].filter(i=>!(i.complete&&i.naturalWidth)).length,old:document.body.innerText.includes('Chances are'),iframe:!!document.querySelector('iframe[src*=RequestaFreeDemo]')}));
    console.log(n, JSON.stringify(info));
    await p.screenshot({path:`sol-live-${n}.png`, fullPage:true, clip:{x:0,y:0,width:vp.width,height:Math.min(info.H,2600)}});
    if(n==='d'){ await p.click('.cvs-btn.p'); await p.waitForTimeout(1200); console.log('anchor scrollY', await p.evaluate(()=>Math.round(scrollY)), await p.evaluate(()=>Math.round(document.querySelector('#cvs-quote').getBoundingClientRect().top))); }
    await c.close();
  }
  await b.close();
})();
