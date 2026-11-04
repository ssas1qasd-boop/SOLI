const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day9.html'); await p.waitForTimeout(1500);
  await p.screenshot({path:'/tmp/claude-0/b9a.png'});
  await p.evaluate(() => { __bench.load('d9_t1'); const n = __bench.st().length; __bench.go(n - 1); }); await p.waitForTimeout(1200);
  await p.screenshot({path:'/tmp/claude-0/b9b.png', fullPage:false});
  await p.evaluate(() => window.scrollTo(0, 900)); await p.waitForTimeout(500); await p.screenshot({path:'/tmp/claude-0/b9c.png'});
  await b.close(); })();
