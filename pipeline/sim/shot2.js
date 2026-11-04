const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:420,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+require('fs').readFileSync('gpu_sim.html','utf8')+'</body></html>');
await p.evaluate(()=>{const s=document.getElementById('seek');s.value=128;s.dispatchEvent(new Event('input'))});
await p.waitForTimeout(2500); await p.locator('#p-scr').screenshot({path:'a_vs.png'});
await p.evaluate(()=>{const s=document.getElementById('seek');s.value=129;s.dispatchEvent(new Event('input'))});
await p.waitForTimeout(3000); await p.click('#apause'); const v1=await p.inputValue('#aseek'); await p.waitForTimeout(1500); const v2=await p.inputValue('#aseek');
await p.locator('#p-scr').screenshot({path:'a_raster.png'});
console.log('paused progress',v1,v2,'errors',errs);
// autoplay waits for animation
await p.evaluate(()=>{const s=document.getElementById('seek');s.value=130;s.dispatchEvent(new Event('input'))});
await p.click('#play'); await p.waitForTimeout(4000); console.log('step after 4s autoplay', await p.textContent('#count'));
await b.close();})();
