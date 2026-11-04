const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:412,height:915}});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_days.html'); await p.waitForTimeout(900);
  await p.evaluate(() => { __bench.load('d7_r2'); document.getElementById('stoBtn').click(); });
  await p.waitForTimeout(400);
  console.log(await p.evaluate(() => [...document.querySelectorAll('#story2 .brk bdi')].filter(e=>/Buffer|VAO/.test(e.textContent)).slice(0,4).filter(e=>e.querySelector('code')).slice(0,4).map(e => { const c=e.querySelector('code'), r=e.getBoundingClientRect(); return e.textContent+' bdi '+Math.round(r.x)+'-'+Math.round(r.right)+' code '+Math.round(c.getBoundingClientRect().x); }).join('\n')));
  await b.close(); })();
