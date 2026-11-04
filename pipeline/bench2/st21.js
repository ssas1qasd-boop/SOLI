const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}, colorScheme:'dark', deviceScaleFactor:2}); const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day5.html#d5_c2'); await p.waitForTimeout(900); await p.click('#stoBtn'); await p.waitForTimeout(300);
  await p.evaluate(() => document.querySelectorAll('.sto details.sec').forEach(d => d.open = true));
  console.log(await p.evaluate(() => [...document.querySelectorAll('.sto .words dt')].map(x=>x.innerText).join(' | ')));
  console.log(await p.evaluate(() => [...document.querySelectorAll('.sto .chain .row')].map(x=>x.innerText.replace(/\s+/g,' ')).join('\n')));
  console.log(await p.evaluate(() => [...document.querySelectorAll('.sto .chap p')].map(x=>x.innerText).find(t => /الكيبورد/.test(t)) || 'no kb in chapters'));
  console.log(errs); await b.close(); })();
