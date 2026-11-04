const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']});
  for (const [w,h,n] of [[412,915,'m'],[1400,900,'d']]){
  const p = await b.newPage({viewport:{width:w,height:h}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1500); await p.evaluate(() => __bench.load('d7_r2'));
  await p.evaluate(() => document.getElementById('stage').scrollIntoView({block:'start'})); await p.waitForTimeout(500);
  await p.screenshot({path:`/tmp/claude-0/ch_${n}1.png`});
  await p.click('#agFab'); await p.waitForTimeout(300); await p.fill('#agQ', 'ايه ال EBO'); await p.press('#agQ', 'Enter'); await p.waitForTimeout(900);
  await p.fill('#agQ', 'ليه عملت 3 صناديق؟'); await p.press('#agQ', 'Enter'); await p.waitForTimeout(900);
  await p.screenshot({path:`/tmp/claude-0/ch_${n}2.png`}); console.log(n, errs); await p.close(); }
  await b.close(); })();
