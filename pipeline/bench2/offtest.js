const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']}); const p = await b.newPage({viewport:{width:412,height:900}});
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); await p.route(/^https?:/, r => r.abort());
  await p.goto('file:///home/claude/bench2/offline/bench_day3__d3_l1.html'); await p.waitForTimeout(2500);
  await p.evaluate(() => document.getElementById('stage').scrollIntoView()); await p.waitForTimeout(1500);
  await p.screenshot({path:'/tmp/claude-0/off.png'}); console.log('ERR', errs, await p.evaluate(() => document.getElementById('stepOut').textContent)); await b.close(); })();
