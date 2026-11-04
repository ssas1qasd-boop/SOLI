const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const errs=[];
 for (const [w,cs] of [[412,'dark'],[1280,'light']]){ const p = await b.newPage({viewport:{width:w,height:900}, colorScheme:cs, deviceScaleFactor:2}); p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day4.html#d4_e2'); await p.waitForTimeout(800);
  await p.fill('#goN','150'); await p.click('#goStep button'); await p.waitForTimeout(400); console.log(w, await p.textContent('#stepOut'));
  await p.fill('#goN','37'); await p.press('#goN','Enter'); await p.waitForTimeout(400); console.log(w, await p.textContent('#stepOut'));
  await p.fill('#goN','9999'); await p.click('#goStep button'); await p.waitForTimeout(200); console.log(w, 'bad:', await p.$eval('#goN', x => x.className), await p.textContent('#stepOut'));
  await p.waitForTimeout(1300); await (await p.$('.btns')).screenshot({path:`/tmp/claude-0/go${w}.png`}); await p.close(); }
 console.log(errs); await b.close(); })();
