const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:950}});
await p.setContent('<!doctype html><html><head><meta charset=utf-8></head><body>'+require('fs').readFileSync('gpu_sim.html','utf8')+'</body></html>');
await p.evaluate(()=>{const s=document.getElementById('seek');s.value=131;s.dispatchEvent(new Event('input'))});
await p.waitForTimeout(600); await p.locator('#hw').screenshot({path:'c_hw.png'}); await b.close();})();
