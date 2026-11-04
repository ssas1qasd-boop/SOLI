const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}}); const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  for (const id of ['d1_cam','d3_l2','d4_v2','d5_c2','d5_n2','d5_p1']){
  await p.goto('file:///home/claude/bench2/bench_days.html#'+id); await p.waitForTimeout(800); await p.click('#stoBtn'); await p.waitForTimeout(300);
  console.log(id, '|', await p.evaluate(() => [...document.querySelectorAll('.sto .words dt')].map(x=>x.textContent).join(' , ')));
  await p.click('#stoX'); }
  console.log(errs); await b.close(); })();
