const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const errs=[]; const p = await b.newPage({viewport:{width:412,height:915}, colorScheme:'dark', deviceScaleFactor:2}); p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day4.html#d4_v1'); await p.waitForTimeout(1000);
  await p.fill('#goN','6'); await p.click('#goStep button[type=submit]'); await p.waitForTimeout(300);
  await p.click('#stepsBtn'); await p.waitForTimeout(500);
  console.log(await p.evaluate(() => [document.querySelectorAll('#stList li').length, document.querySelector('#stList li.now').id, document.getElementById('stSub').textContent]));
  await p.screenshot({path:'/tmp/claude-0/steps1.png'});
  await p.fill('#stq','glDrawArrays'); await p.waitForTimeout(200); console.log('filtered', await p.evaluate(() => [...document.querySelectorAll('#stList li')].filter(l=>!l.hidden).length));
  await p.fill('#stq',''); await p.click('#stp40 [data-go]'); await p.waitForTimeout(400); console.log('after go', await p.textContent('#stepOut'), 'hidden', await p.evaluate(()=>document.getElementById('stepsSheet').hidden));
  await p.click('#glossBtn'); await p.click('#stepsBtn'); await p.waitForTimeout(200); console.log('gloss hidden', await p.evaluate(()=>document.getElementById('gloss').hidden));
  // switch program while open
  console.log(errs); await b.close(); })();
