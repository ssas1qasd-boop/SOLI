const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
for (const [w,h,n] of [[1400,900,'d'],[400,900,'m']]){
const p=await b.newPage({viewport:{width:w,height:h}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',r=>r.fulfill({path:'/home/claude/sim/three.min.js',contentType:'application/javascript'}));
await p.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
await p.setContent('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync('bench.html','utf8')+'</body></html>',{waitUntil:'load'});
await p.waitForTimeout(500); await p.click('#key'); await p.evaluate(()=>{const l=document.getElementById('lever'); l.value=0.75; l.dispatchEvent(new Event('input'))});
await p.waitForTimeout(9000); await p.evaluate(()=>document.querySelector('[data-mode=exploded]').click()); await p.waitForTimeout(1500); await p.screenshot({path:'C_'+n+'_exp.png',fullPage:n==='m'});
await p.evaluate(()=>document.querySelector('[data-mode=flow]').click()); await p.waitForTimeout(1500); await p.screenshot({path:'C_'+n+'_flow.png'});
console.log(n,'errors',errs.slice(0,3),'sw',await p.evaluate(()=>document.documentElement.scrollWidth));
}
await b.close();})();
