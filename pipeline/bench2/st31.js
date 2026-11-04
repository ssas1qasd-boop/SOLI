const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:412,height:915}});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_days.html'); await p.waitForTimeout(900);
  await p.evaluate(() => { __bench.load('d7_r2'); document.getElementById('stoBtn').click(); });
  await p.waitForTimeout(400);
  console.log(await p.evaluate(() => { const e=[...document.querySelectorAll('#story2 span[dir]')].find(e=>/6 × 4/.test(e.textContent)); if(!e) return 'none'; const c=getComputedStyle(e); return [e.outerHTML, e.parentElement.className, c.display, c.unicodeBidi, c.direction].join(' | '); }));
  await b.close(); })();
