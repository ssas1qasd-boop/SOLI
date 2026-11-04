const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const errs=[];
 for (const [w,cs] of [[412,'dark'],[1280,'light']]){ const p = await b.newPage({viewport:{width:w,height:900}, colorScheme:cs, deviceScaleFactor:2}); p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day4.html#d4_v1'); await p.waitForTimeout(900);
  const s = async () => (await p.textContent('#stepOut')) + ' box=' + (await p.inputValue('#goN')) + ' decDis=' + (await p.$eval('#goDec', x => x.disabled));
  console.log(w, 'start', await s());
  await p.click('#goInc'); await p.click('#goInc'); await p.waitForTimeout(200); console.log(w, '+2', await s());
  await p.click('#goDec'); await p.waitForTimeout(200); console.log(w, '-1', await s());
  await p.fill('#goN','40'); await p.click('#goStep button[type=submit]'); await p.waitForTimeout(300); await p.click('#goInc'); await p.waitForTimeout(200); console.log(w, '40+1', await s());
  await p.evaluate(() => document.getElementById('goN').scrollIntoView({block:'center'})); await p.waitForTimeout(300);
  const bb = await (await p.$('#goStep')).boundingBox(); await p.screenshot({path:`/tmp/claude-0/ar${w}.png`, clip:{x:Math.max(0,bb.x-20), y:bb.y-90, width:Math.min(w, bb.width+40), height:bb.height+110}}); await p.close(); }
 console.log(errs); await b.close(); })();
