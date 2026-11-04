const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']});
  const p = await b.newPage({viewport:{width:1400,height:900}, deviceScaleFactor:3});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1500);
  await p.evaluate(() => __bench.load('d7_r2')); await p.waitForTimeout(300);
  console.log(await p.evaluate(() => [...document.querySelectorAll('.agsug')].map(b => b.textContent).join(' | ')));
  await p.waitForTimeout(900);
  await p.screenshot({path:'/tmp/claude-0/rz.png'}); await b.close(); })();
