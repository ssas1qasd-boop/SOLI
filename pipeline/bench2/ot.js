const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage();
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); await p.route(/^https?:/, r => r.abort());
  await p.goto('file:///home/claude/bench2/offline/bench_day3_cad_line.html'); await p.waitForTimeout(1500);
  await p.click('#stoBtn'); await p.waitForTimeout(400);
  console.log(await p.evaluate(() => [document.getElementById('ptitle').textContent, document.querySelectorAll('.chap').length]), 'ERR', errs); await b.close(); })();
