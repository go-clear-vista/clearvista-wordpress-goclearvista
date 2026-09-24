const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [pg,n,vp,m] of [['/','d',{width:1440,height:900},false],['/','t',{width:820,height:1180},true],['/','m',{width:390,height:844},true],['/av-solutions/','sd',{width:1440,height:900},false],['/contact-us/','cd',{width:1440,height:900},false]]) {
    const c = await b.newContext({ viewport:vp, isMobile:m, hasTouch:m, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com'+pg+'?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(1500);
    const f=await p.$('footer'); await f.scrollIntoViewIfNeeded(); await p.waitForTimeout(1200);
    const info=await p.evaluate(()=>{const f=document.querySelector('footer');const cvf=f.querySelector('.cvf');const r=f.getBoundingClientRect();
      const txt=f.innerText;
      return {cvf:!!cvf, fh:Math.round(r.height), sw:document.documentElement.scrollWidth, oldGrey:/Store hours|Stay Connected|TVSPro/.test(txt), sections:f.querySelectorAll('.et_pb_section').length, codeModules:f.querySelectorAll('.et_pb_code').length, links:cvf?cvf.querySelectorAll('a').length:0, logo:cvf?(()=>{const i=cvf.querySelector('.cvf-logo img');return i&&i.complete&&i.naturalWidth>0})():null, gapAbove: (()=>{const s=f.querySelector('.et_pb_section');return s?getComputedStyle(s).paddingTop+'/'+getComputedStyle(s).paddingBottom:null})(), rowPad:(()=>{const s=f.querySelector('.et_pb_row');return s?getComputedStyle(s).paddingTop+'/'+getComputedStyle(s).paddingBottom+' w='+Math.round(s.getBoundingClientRect().width):null})(), cvfW: cvf?Math.round(cvf.getBoundingClientRect().width):0, brs:(f.innerHTML.match(/<br\s*\/?>|<p>\s*<\/p>/g)||[]).length, pInCode:(f.querySelector('.et_pb_code_inner')?.innerHTML.match(/<p>/g)||[]).length}});
    console.log(n, JSON.stringify(info));
    await f.screenshot({path:`footlive-${n}.png`});
    await c.close();
  }
  await b.close();
})();
