const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1400,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',r=>r.fulfill({path:'/home/claude/sim/three.min.js',contentType:'application/javascript'}));
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync('bench.html','utf8')+'</body></html>',{waitUntil:'load'});
await p.waitForTimeout(800); console.log('load', await p.textContent('#loadOut'));
await p.click('#key'); await p.evaluate(()=>{const l=document.getElementById('lever'); l.value=0.75; l.dispatchEvent(new Event('input'))});
await p.evaluate(()=>document.querySelector('[data-mode=cutaway]').click());
for (const [t,n] of [[7500,'B_boot'],[3000,'B_l1'],[3000,'B_l2'],[3000,'B_l3']]){ await p.waitForTimeout(t); await p.screenshot({path:n+'.png'}); console.log(n, await p.textContent('#rPhase'), await p.textContent('#rLap'), await p.textContent('#rBack'), await p.textContent('#rFront')); }
await p.evaluate(()=>document.querySelector('[data-mode=exploded]').click()); await p.waitForTimeout(1500); await p.screenshot({path:'B_exp.png'});
console.log('errors',errs.slice(0,5));
await b.close();})();
