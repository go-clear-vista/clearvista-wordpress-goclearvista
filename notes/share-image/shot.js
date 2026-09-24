const {chromium}=require('/opt/node22/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch({args:['--ignore-certificate-errors'],proxy:{server:process.env.HTTPS_PROXY}});
const p=await b.newPage({viewport:{width:1200,height:630}});
await p.goto('file://'+__dirname+'/og.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
console.log(await p.evaluate(()=>document.fonts.check('800 54px "Open Sans"')));
await p.screenshot({path:'clearvista-share-1200x630.jpg',type:'jpeg',quality:88});await b.close();})();
