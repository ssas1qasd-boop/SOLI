const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:950}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+require('fs').readFileSync('gpu_sim.html','utf8')+'</body></html>');
await p.evaluate(()=>{const s=document.getElementById('seek');s.value=129;s.dispatchEvent(new Event('input'))});
await p.waitForTimeout(4000); await p.click('#apause');
await p.locator('#p-scr').screenshot({path:'b_raster.png'}); console.log(errs);
await b.close();})();
