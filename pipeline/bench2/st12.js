const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}, colorScheme:'dark', deviceScaleFactor:2});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_days.html#d3_l2'); await p.waitForTimeout(1200);
  await p.fill('#goN','56'); await p.click('#goStep button[type=submit]'); await p.waitForTimeout(1500);
  await p.screenshot({path:'/tmp/claude-0/pos.png'}); await b.close(); })();
