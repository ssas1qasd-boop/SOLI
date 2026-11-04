const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:420,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+require('fs').readFileSync('story.html','utf8')+'</body></html>');
for(let k=0;k<9;k++){ await p.evaluate(k=>document.querySelectorAll('#dots button')[k].click(),k); await p.waitForTimeout(3500); await p.locator('#cv').screenshot({path:`S_${k}.png`}); }
console.log(errs, await p.evaluate(()=>document.documentElement.scrollWidth)); await b.close();})();
