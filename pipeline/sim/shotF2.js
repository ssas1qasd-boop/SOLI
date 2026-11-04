const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
for (const f of ['bench_full.html','bench.html']){
const p=await b.newPage({viewport:{width:1400,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',r=>r.fulfill({path:'/home/claude/sim/three.min.js',contentType:'application/javascript'}));
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync(f,'utf8')+'</body></html>',{waitUntil:'load'});
await p.waitForTimeout(800);
if (f==='bench_full.html'){ const btns=await p.$$('#laps button'); console.log('lap buttons',btns.length); await btns[1].click(); await p.waitForTimeout(1200); await p.locator('.instruments').screenshot({path:'I_full.png'}); console.log(await p.textContent('#story'), await p.textContent('#stepOut'), await p.textContent('#leverOut')); }
await p.click('#zin'); await p.click('#zin'); await p.waitForTimeout(600); await p.screenshot({path:'Z_'+f+'.png'});
console.log(f,'errors',errs.slice(0,3)); }
await b.close();})();
