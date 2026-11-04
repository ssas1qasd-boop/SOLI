const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage();
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_days.html'); await p.waitForTimeout(2000);
  console.log(await p.evaluate(() => { const t = performance.now(); window.__agent.AG.build(); return 'index build ms ' + Math.round(performance.now() - t); }));
  await b.close(); })();
