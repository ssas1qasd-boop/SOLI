const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const [w,h,n] of [[1250,950,'d'],[400,900,'m']]){
const p=await b.newPage({viewport:{width:w,height:h}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+require('fs').readFileSync('loop.html','utf8')+'</body></html>');
await p.selectOption('#speed','0.45');
for (const ms of [2500,6000,12000]){ await p.waitForTimeout(ms===2500?2500:ms===6000?3500:6000); await p.screenshot({path:`L_${n}_${ms}.png`,fullPage:true}); }
if(n==='d'){ await p.click('#close'); await p.waitForTimeout(6000); await p.screenshot({path:'L_d_end.png',fullPage:true}); }
console.log(n,'sw',await p.evaluate(()=>document.documentElement.scrollWidth),'errs',errs, await p.textContent('#title'));
}
await b.close();})();
