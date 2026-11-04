const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
for (const [w,h,n] of [[412,900,'m'],[1400,900,'d']]){
const p=await b.newPage({viewport:{width:w,height:h},colorScheme:'dark'});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',r=>r.fulfill({path:'/home/claude/sim/three.min.js',contentType:'application/javascript'}));
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync('bench_full.html','utf8')+'</body></html>',{waitUntil:'load'});
await p.evaluate(()=>{const s=document.getElementById('seek');s.value=15;s.dispatchEvent(new Event('input'))});
await p.waitForTimeout(2500);
await p.locator('#stage').scrollIntoViewIfNeeded(); await p.waitForTimeout(800); await p.screenshot({path:`P_${n}.png`});
await p.click('#pause'); const a=await p.textContent('#pause'); await p.waitForTimeout(1500); const s1=await p.textContent('#stepOut'); await p.click('#pause'); const b2=await p.textContent('#pause');
console.log(n,a,s1,b2,'errors',errs.slice(0,3)); }
await b.close();})();
