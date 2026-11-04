const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:900}, colorScheme:'dark', deviceScaleFactor:2});
  const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day4.html#d4_e2'); await p.waitForTimeout(800); await p.click('#stoBtn'); await p.waitForTimeout(300);
  console.log(await p.evaluate(() => [...document.querySelectorAll('.sto details.sec>summary')].map(x=>x.innerText).join(' | ')));
  await (await p.$('#story2')).screenshot({path:'/tmp/claude-0/sec.png'});
  await p.evaluate(() => [...document.querySelectorAll('.sto details.sec')].find(d => d.querySelector('.drvt')).open = true);
  console.log(await p.evaluate(() => [...document.querySelectorAll('.drvt tbody tr')].map(x=>x.innerText.replace(/\s+/g,' ')).join('\n')));
  // click a go button inside closed->open section
  await p.click('.drvt button'); await p.waitForTimeout(300); console.log('story hidden after go:', await p.evaluate(()=>document.getElementById('story2').hidden));
  console.log(errs); await b.close(); })();
