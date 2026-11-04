const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const errs=[];
 for (const [w,cs] of [[412,'dark'],[1280,'light']]){ const p = await b.newPage({viewport:{width:w,height:915}, colorScheme:cs, deviceScaleFactor:2}); p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day5.html#d5_c2'); await p.waitForTimeout(900);
  await p.click('#cmdBtn'); await p.waitForTimeout(400);
  if (w===412) console.log(await p.evaluate(() => [...document.querySelectorAll('#cmdBody table')].map(t => t.textContent.length+' chars: '+t.innerText.slice(0,0)+t.querySelectorAll('tr').length+' rows'.replace(/\t/g,' | ')).join('\n=====\n')));
  await p.screenshot({path:`/tmp/claude-0/cmd${w}.png`, fullPage:false});
  await p.evaluate(() => document.getElementById('cmdSheet').scrollTop = 900); await p.waitForTimeout(200); await p.screenshot({path:`/tmp/claude-0/cmd${w}b.png`});
  const fb = p.locator('#cmdBody .fn >> visible=true').first(); const t = await fb.textContent(); await fb.click(); await p.waitForTimeout(500); console.log(w, 'clicked', t, '->', await p.textContent('#stepOut'), await p.evaluate(()=>document.getElementById('cmdSheet').hidden));
  await p.close(); }
 const p = await b.newPage(); await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'}));
 await p.goto('file:///home/claude/bench2/bench_day4.html'); await p.waitForTimeout(700); console.log('day4 cmdBtn hidden:', await p.evaluate(()=>document.getElementById('cmdBtn').hidden));
 console.log(errs); await b.close(); })();
