const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:420,height:900},colorScheme:'dark'});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+require('fs').readFileSync('gpu_sim.html','utf8')+'</body></html>');
for (const k of [20,126,130,131,137,138]){
 await p.evaluate(k=>{const s=document.getElementById('seek');s.value=k;s.dispatchEvent(new Event('input'))},k);
 await p.waitForTimeout(k===130||k===137?13000:700);
 await p.locator('#p-scr').screenshot({path:`g_${k}.png`});
 console.log(k, await p.evaluate(()=>[...document.querySelectorAll('#pipe li')].map(l=>l.dataset.k+':'+l.className).join(' ')), await p.textContent('#roleA'), await p.textContent('#roleB'));
}
console.log(errs); await b.close();})();
