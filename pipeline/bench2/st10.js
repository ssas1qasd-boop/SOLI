const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:900}, colorScheme:'dark', deviceScaleFactor:2});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day4.html#d4_v1'); await p.waitForTimeout(1000);
  await p.evaluate(() => document.getElementById('goN').scrollIntoView({block:'center'})); await p.waitForTimeout(300);
  await p.screenshot({path:'/tmp/claude-0/go2.png'});
  console.log(await p.evaluate(() => { const r = document.getElementById('goN').getBoundingClientRect(); return document.elementsFromPoint(r.x+r.width/2, r.y+r.height-4).slice(0,4).map(e => e.tagName+'#'+e.id+'.'+e.className).join(' > '); }));
  await b.close(); })();
