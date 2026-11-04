const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']});
  for (const [page, prog, w, theme, out] of [['bench_day1.html','d1_cam',412,'dark','/tmp/claude-0/by1.png'],['bench_days.html','d4_v1',1400,'light','/tmp/claude-0/by2.png']]){
  const p = await b.newPage({viewport:{width:w,height:900}, colorScheme:theme, deviceScaleFactor: w<500?2:1});
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/' + page + '#' + prog); await p.waitForTimeout(1000);
  console.log('hidden', await p.evaluate(() => document.getElementById('bytesSheet').hidden));
  await p.click('#bytBtn'); await p.waitForTimeout(400); await p.screenshot({path: out});
  console.log(await p.evaluate(() => [document.querySelector('#bytesSheet tr.cur th').innerText, document.querySelectorAll('#bytesSheet tbody tr').length, document.documentElement.scrollWidth]));
  await p.click('#bytX'); await p.click('#stoBtn'); await p.waitForTimeout(200);
  console.log('after story', await p.evaluate(() => [document.getElementById('bytesSheet').hidden, document.getElementById('story2').hidden]), errs);
  await p.close(); }
  await b.close(); })();
