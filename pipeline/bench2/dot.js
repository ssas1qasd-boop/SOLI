const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:900}, colorScheme:'dark', deviceScaleFactor:2});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day4.html#d4_v2'); await p.waitForTimeout(800);
  await p.click('#stoBtn'); await p.waitForTimeout(300);
  console.log(await p.evaluate(() => { const d = document.querySelector('.cl .d'); const cs = getComputedStyle(d); return [d.innerText, d.textContent.slice(0,120), cs.whiteSpace, cs.overflow, cs.textOverflow, cs.display, cs.webkitLineClamp, getComputedStyle(d.parentElement).cssText.slice(0,10)]; }));
  const el = await p.$('.cl'); await el.screenshot({path:'/tmp/claude-0/dot.png'});
  await b.close(); })();
