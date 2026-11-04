const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:412,height:915}});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_days.html'); await p.waitForTimeout(900);
  await p.evaluate(() => { __bench.load('d7_r2'); document.getElementById('stoBtn').click(); });
  await p.waitForTimeout(400);
  console.log(await p.evaluate(() => { const e=[...document.querySelectorAll('#story2 b[dir]')].find(e=>e.textContent==='(-0.3, 0.15, 0)'); e.scrollIntoView(); const t=e.firstChild; const r=document.createRange(); const out=[];
    for (let i=0;i<t.length;i++){ r.setStart(t,i); r.setEnd(t,i+1); out.push([t.data[i], Math.round(r.getBoundingClientRect().x)]); } const c=getComputedStyle(e); return c.display+' '+c.direction+' '+JSON.stringify(out); }));
  await b.close(); })();
