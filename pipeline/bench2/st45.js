const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1200);
  console.log(await p.evaluate(() => { __bench.load('d7_r2'); const A = window.__agent.AG; return JSON.stringify([A.toks('ليه عملت 3 صناديق؟'), A.toks('كام VAO؟'), A.norm('كام VAO؟'), Object.keys(A.facts().bufs), Object.keys(A.facts().vaos)]); }));
  await b.close(); })();
