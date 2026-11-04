const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage();
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); await p.route(/^https?:/, r => r.abort());
  for (const f of ['bench_day1_cam','bench_day3_l1','bench_day4_v1','bench_day1']){ await p.addInitScript(() => { try { localStorage.clear(); } catch(e){} });
    await p.goto('file:///home/claude/bench2/offline/' + f + '.html'); await p.waitForTimeout(1200);
    console.log(f, await p.evaluate(() => document.getElementById('ptitle').textContent)); }
  console.log('ERR', errs); await b.close(); })();
