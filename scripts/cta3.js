const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const css=`@media (min-width:981px){.cv-navcol{display:block!important}.cv-navcol>.et_pb_column{display:flex!important;align-items:center}.cv-navcol .et_pb_menu{flex:1 1 auto;margin-bottom:0!important}.cv-navcol .et_pb_button_module_wrapper{flex:0 0 auto;margin:0 0 0 20px!important}}@media (min-width:981px) and (max-width:1150px){.cv-navcol .et-menu>li{padding-left:7px!important;padding-right:7px!important}.cv-navcol .et-menu>li>a{font-size:15px!important}.cv-navcol .et_pb_button_module_wrapper{margin-left:12px!important}.cv-navcol .et_pb_button_0_tb_header{font-size:14px!important}}`;
(async () => {
  const b = await chromium.launch({ args:['--ignore-certificate-errors'], proxy:{server:process.env.HTTPS_PROXY} });
  for (const [n,vp] of [['d',{width:1440,height:900}],['d2',{width:1024,height:768}],['d3',{width:1280,height:800}]]) {
    const c = await b.newContext({ viewport:vp, ignoreHTTPSErrors:true });
    const p = await c.newPage(); await p.goto('https://www.goclearvista.com/?v='+Date.now(), {waitUntil:'load', timeout:90000});
    await p.mouse.move(100,400); await p.waitForTimeout(2500);
    
    console.log(n, await p.evaluate(()=>{const bt=document.querySelector('.et_pb_button_0_tb_header').getBoundingClientRect();const s=document.querySelector('[class*=_tb_header] .et_pb_menu__search-button').getBoundingClientRect();const h=document.querySelector('.et_pb_section_2_tb_header').getBoundingClientRect();return JSON.stringify({btn:[Math.round(bt.x),Math.round(bt.y),Math.round(bt.width)],search:[Math.round(s.x),Math.round(s.right)],hdrH:Math.round(h.height),sw:document.documentElement.scrollWidth})}));
    await p.screenshot({path:`cta4-${n}.png`, clip:{x:0,y:0,width:vp.width,height:170}});
    await c.close();
  }
  await b.close();
})();
