const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,block] of [['normal',false],['noscript',true]]) {
    const c = await b.newContext({ viewport:{width:390,height:844}, isMobile:true, hasTouch:true, ignoreHTTPSErrors:true });
    const p = await c.newPage();
    if (block) await p.route(/divi-carousel-maker.*\.js|slick.*\.js/, r=>r.abort());
    await p.goto('https://www.goclearvista.com/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(2000);
    for (let i=0;i<14;i++){ await p.mouse.wheel(0,400); await p.waitForTimeout(200); }
    const sec = await p.$('.pa-dcm-blog-4'); await sec.scrollIntoViewIfNeeded(); await p.evaluate(()=>window.scrollBy(0,-150)); await p.waitForTimeout(3000);
    const info = await p.evaluate(()=>{const col=document.querySelector('.pa-dcm-blog-4>.et_pb_column'); return {slick:col.classList.contains('slick-initialized'), rowH:Math.round(document.querySelector('.pa-dcm-blog-4').getBoundingClientRect().height), scrollW:col.scrollWidth, clientW:col.clientWidth, pageSW:document.documentElement.scrollWidth}});
    console.log(n, JSON.stringify(info));
    const s = (await p.$('.pa-dcm-blog-4')).evaluateHandle(e=>e.closest('.et_pb_section'));
    await (await s).asElement().screenshot({path:`blogfix-${n}.png`});
    await c.close();
  }
  await b.close();
})();
