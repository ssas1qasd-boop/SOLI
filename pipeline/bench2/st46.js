const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']});
  for (const [w,h,n] of [[412,915,'m'],[1400,900,'d']]){
  const p = await b.newPage({viewport:{width:w,height:h}});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1500);
  await p.evaluate(() => __bench.load('d7_r2'));
  await p.evaluate(() => document.getElementById('stage').scrollIntoView({block:'start'})); await p.waitForTimeout(800);
  await p.screenshot({path:`/tmp/claude-0/rb_${n}1.png`});
  await p.fill('#agQ', 'ليه عملت 3 صناديق؟'); await p.click('#agForm button[type=submit]'); await p.waitForTimeout(2500);
  await p.evaluate(() => document.getElementById('askbot').scrollIntoView({block:'start'})); await p.waitForTimeout(400);
  await p.screenshot({path:`/tmp/claude-0/rb_${n}2.png`}); await p.close(); }
  await b.close(); })();
