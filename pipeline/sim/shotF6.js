const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:412,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',r=>r.fulfill({path:'/home/claude/sim/three.min.js',contentType:'application/javascript'}));
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync('bench_full.html','utf8')+'</body></html>',{waitUntil:'load'});
for (const k of [28,100]){ await p.evaluate(k=>{const s=document.getElementById('seek');s.value=k;s.dispatchEvent(new Event('input'))},k); await p.waitForTimeout(900); await p.locator('#epath').scrollIntoViewIfNeeded(); await p.waitForTimeout(400); await p.locator('#epath').screenshot({path:`EP_${k}.png`}); }
console.log(errs.slice(0,3)); await b.close();})();
