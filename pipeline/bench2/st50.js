const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1500); await p.evaluate(() => __bench.load('d7_r2'));
  for (const q of process.argv.slice(2)){ const r = await p.evaluate(q => { const r = __bench.agent(q); const d = document.createElement('div'); d.innerHTML = r ? r.html : ''; return r ? d.innerText.replace(/\s+/g,' ').slice(0, 420) : 'NULL'; }, q); console.log('Q:', q, '\n  ', r); }
  console.log('errors', errs); await b.close(); })();
