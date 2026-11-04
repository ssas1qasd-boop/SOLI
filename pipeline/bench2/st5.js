const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:900}, colorScheme:'dark', deviceScaleFactor:2});
  const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day4.html#d4_v2'); await p.waitForTimeout(900);
  await p.click('#stoBtn'); await p.waitForTimeout(300);
  const w = await p.$('.sto .words'); await w.screenshot({path:'/tmp/claude-0/w1.png'});
  const c = await p.$$('.chap'); await (await c[1].$('p')).screenshot({path:'/tmp/claude-0/w2.png'});
  console.log(await p.evaluate(() => document.querySelectorAll('.chap')[1].querySelector('.brk').innerText), errs); await b.close(); })();
