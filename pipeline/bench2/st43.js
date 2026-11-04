const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1500);
  await p.evaluate(() => { __bench.load('d7_r2'); const ST = __bench.st(); const k = ST.findIndex(s => s.an === 'new' && /Buffer 3/.test(JSON.stringify(s.lv))); window.__k = k; __bench.go(k); });
  await p.waitForTimeout(150); const a = await p.evaluate(() => __bench.scale());
  await p.evaluate(() => __bench.go(window.__k + 1)); await p.waitForTimeout(800); const c = await p.evaluate(() => __bench.scale());
  console.log('during new', JSON.stringify(a), 'next step', JSON.stringify(c), 'errors', errs); await b.close(); })();
