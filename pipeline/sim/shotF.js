const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1400,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',r=>r.fulfill({path:'/home/claude/sim/three.min.js',contentType:'application/javascript'}));
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync('bench_full.html','utf8')+'</body></html>',{waitUntil:'load'});
for (const k of [30,131]){ await p.evaluate(k=>{const s=document.getElementById('seek');s.value=k;s.dispatchEvent(new Event('input'))},k); await p.waitForTimeout(1800); await p.screenshot({path:`F_${k}.png`}); console.log(k, await p.textContent('#rGpu'), await p.textContent('#rStack'), await p.textContent('#rFb')); }
console.log('errors',errs.slice(0,5)); await b.close();})();
