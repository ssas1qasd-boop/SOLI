const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:900}, colorScheme:'dark', deviceScaleFactor:2});
  const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  for (const [pg,id] of [['bench_day1.html','d1_cam'],['bench_day3.html','d3_l2'],['bench_day2.html','d2_va1']]){
    await p.goto('file:///home/claude/bench2/'+pg+'#'+id); await p.waitForTimeout(800); await p.click('#stoBtn'); await p.waitForTimeout(300);
    console.log(id, await p.evaluate(() => [...document.querySelectorAll('.sto .words dt')].map(x => x.innerText).join(' | ')));
    await p.click('#stoX'); }
  await p.goto('file:///home/claude/bench2/bench_day3.html#d3_l2'); await p.waitForTimeout(800); await p.click('#stoBtn'); await p.waitForTimeout(300);
  await (await p.$('.sto .words')).screenshot({path:'/tmp/claude-0/w3.png'}); console.log(errs); await b.close(); })();
