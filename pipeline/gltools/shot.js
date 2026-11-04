const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:412,height:900}});await p.route(/^https?:/,r=>r.abort());
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.setContent('<!doctype html><meta charset=utf-8>'+require('fs').readFileSync('gl_tools.html','utf8'));await p.waitForTimeout(500);
await p.screenshot({path:'/tmp/claude-0/g1.png',fullPage:true});console.log(errs, await p.evaluate(()=>document.documentElement.scrollWidth));await b.close();})();
