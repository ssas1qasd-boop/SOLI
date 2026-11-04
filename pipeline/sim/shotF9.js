const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:412,height:900},colorScheme:'dark'}); const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',r=>r.fulfill({path:'/home/claude/sim/three.min.js',contentType:'application/javascript'}));
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync('bench_full.html','utf8')+'</body></html>',{waitUntil:'load'});
await p.click('#reftoggle'); await p.locator('#refimg').scrollIntoViewIfNeeded(); await p.click('#refimg'); await p.waitForTimeout(400); await p.screenshot({path:'BIG1.png'});
await p.click('#refzoom'); await p.waitForTimeout(300); await p.screenshot({path:'BIG2.png'}); await p.click('#refclose');
console.log(await p.evaluate(()=>document.getElementById('refbig').hidden), errs); await b.close();})();
