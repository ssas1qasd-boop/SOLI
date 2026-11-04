const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}, colorScheme:'dark', deviceScaleFactor:2}); const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day4.html#d4_v2'); await p.waitForTimeout(1000);
  await p.evaluate(() => { const c = document.getElementById('code'); c.scrollTop = document.getElementById('L23').offsetTop - 30; }); await p.waitForTimeout(300);
  await (await p.$('#codeFig')).screenshot({path:'/tmp/claude-0/cf2.png'}); console.log(errs); await b.close(); })();
