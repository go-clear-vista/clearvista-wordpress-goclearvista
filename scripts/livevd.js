// Verify live Visual Displays page: layout, overflow, links.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const out='/tmp/claude-0/vdlive';
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['d',{width:1440,height:900},false],['l',{width:1280,height:800},false],['s',{width:1024,height:768},false],['t',{width:820,height:1180},true],['m',{width:390,height:844},true]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/visual-displays/?nocache='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.mouse.wheel(0,400); await p.waitForTimeout(2500);
    await p.evaluate(()=>Promise.all([...document.querySelectorAll('.cvs-hero ~ * img, .cvs-tc img, .cvs-gal img')].map(i=>(i.loading='eager',i.complete?1:new Promise(r=>{i.onload=i.onerror=r})))));
    const r=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,hero:!!document.querySelector('.cvs-hero'),cards:[...document.querySelectorAll('.cvs-tc h3')].map(e=>e.textContent),broken:[...document.querySelectorAll('.cvs-tc img,.cvs-gal img')].filter(i=>!i.naturalWidth).length,iframe:(document.querySelector('iframe[src*="ContactaPro"]')||{}).src,anchor:!!document.getElementById('cvs-quote'),oldPopup:!!document.getElementById('wonderbox')}));
    console.log(n,vp.width,JSON.stringify(r));
    if(n=='d'||n=='m'||n=='t'){await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(500);await p.screenshot({path:`${out}/live-${n}.png`,fullPage:true});}
    await c.close();
  }
  const c=await b.newContext({ignoreHTTPSErrors:true}); const p=await c.newPage();
  for (const u of ['/av-solutions/','/design-engineering/','/custom-program-integration/','/system-installation/','/service-level-agreements/','/state-of-utah-contract/','/digital-signage-2/','/command-control-systems/','/web-conferencing/','/classroom-technologies/']) {const r=await p.goto('https://www.goclearvista.com'+u,{timeout:60000});console.log(u,r.status());}
  await b.close();
})();
