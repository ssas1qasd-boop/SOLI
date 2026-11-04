const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:412,height:900}}); const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',r=>r.fulfill({path:'/home/claude/sim/three.min.js',contentType:'application/javascript'}));
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync('bench_full.html','utf8')+'</body></html>',{waitUntil:'load'});
const h=async()=>p.evaluate(()=>document.getElementById('refbody').hidden);
const a=await h(); await p.click('#reftoggle'); const b2=await h(); const t=await p.textContent('#reftoggle'); await p.click('#refimg'); const big=await p.evaluate(()=>!document.getElementById('refbig').hidden); await p.click('#refclose'); await p.click('#reftoggle'); const c=await h();
console.log(a,b2,t,big,c,errs); await b.close();})();
