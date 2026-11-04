const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage();
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1200); await p.evaluate(() => __bench.load('d7_r2'));
  for (const q of process.argv.slice(2)) console.log(q, await p.evaluate(q => { const A = window.__agent.AG; window.__agent.ask('x'); const w = A.qweights(q);
    return JSON.stringify([[...w].map(([t, v]) => t + ':' + v.toFixed(2)).join(' '), A.search(q, {n: 5}).map(x => [x.s.toFixed(2), x.d.code || x.d.title, x.d.len.toFixed(0)])]); }, q));
  await b.close(); })();
