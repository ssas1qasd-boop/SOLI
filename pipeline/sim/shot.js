const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const [w,h,name,scheme] of [[1300,900,'desk','light'],[400,860,'phone','dark']]){
 const p=await b.newPage({viewport:{width:w,height:h},colorScheme:scheme});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+require('fs').readFileSync('gpu_sim.html','utf8')+'</body></html>');
 await p.waitForTimeout(800);
 for (const k of [60,128,129,131]){ await p.evaluate(k=>{document.getElementById('seek').value=k;document.getElementById('seek').dispatchEvent(new Event('input'))},k); await p.waitForTimeout(2200); await p.screenshot({path:`s_${name}_${k}.png`,fullPage:name==='desk'});}
 const sw=await p.evaluate(()=>document.documentElement.scrollWidth); console.log(name,'scrollWidth',sw,'errors',errs);
}
await b.close();})();
