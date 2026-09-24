const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const css='.et-l--footer .et_pb_section{padding:0!important}.et-l--footer .et_pb_row:has(.cvf){width:100%!important;max-width:100%!important;padding:0!important;margin:0!important}.et-l--footer .et_pb_code:has(.cvf){margin:0!important}';
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp,m] of [['d',{width:1440,height:900},false],['t',{width:820,height:1180},true],['m',{width:390,height:844},true]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(1500);
    
    const f=await p.$('footer'); await f.scrollIntoViewIfNeeded(); await p.waitForTimeout(800);
    console.log(n, await p.evaluate(()=>{const f=document.querySelector('footer').getBoundingClientRect();const c=document.querySelector('.cvf').getBoundingClientRect();return JSON.stringify({fw:Math.round(f.width),fh:Math.round(f.height),cw:Math.round(c.width),ch:Math.round(c.height),sw:document.documentElement.scrollWidth})}));
    await f.screenshot({path:`footfinal-${n}.png`});
    await c.close();
  }
  await b.close();
})();
