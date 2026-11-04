const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:420,height:900}});
p.on('pageerror',e=>console.log('ERR',e.stack));
await p.setContent('<!doctype html><html><head><meta charset=utf-8></head><body>'+require('fs').readFileSync('gpu_sim.html','utf8')+'</body></html>');
await p.evaluate(()=>{const s=document.getElementById('seek');s.value=128;s.dispatchEvent(new Event('input'))});
for(let k=0;k<6;k++){await p.waitForTimeout(400); console.log(await p.evaluate(()=>JSON.stringify(A)));}
await b.close();})();
