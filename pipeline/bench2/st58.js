const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage();
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1200); await p.evaluate(() => __bench.load('d7_r2'));
  console.log(await p.evaluate(() => { const A = window.__agent.AG; window.__agent.ask('x'); A.learnFromClaude('المثلث بيتحول لبكسلات ازاي', 'شرح تجريبي خطوة 76'); 
    return JSON.stringify(JSON.parse(localStorage.getItem('benchHelperFromClaude')).slice(-1)) + '\n' + window.__agent.ask('الكارت بيحول المثلث بكسلات ازاي').html.slice(0, 200); }));
  await b.close(); })();
