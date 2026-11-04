const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const errs=[]; const p = await b.newPage({viewport:{width:412,height:915}, colorScheme:'dark', deviceScaleFactor:2}); p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  for (const id of ['d5_c2','d5_p2','d5_n2','d5_c1','d5_r1']){
    await p.goto('file:///home/claude/bench2/bench_day5.html#'+id); await p.waitForTimeout(800); await p.click('#cmdBtn'); await p.waitForTimeout(300);
    console.log(id, await p.evaluate(() => [...document.querySelectorAll('#cmdBody table')].map(t => [...t.querySelectorAll('tr')].map(r => r.innerText.replace(/\s+/g,' ')).join(' / ')).join('\n   ')));
    if (id==='d5_c2'){ await p.screenshot({path:'/tmp/claude-0/cmd2a.png'}); await p.evaluate(() => document.getElementById('cmdSheet').scrollTop = 700); await p.waitForTimeout(200); await p.screenshot({path:'/tmp/claude-0/cmd2b.png'}); }
    await p.click('#cmdX'); }
  console.log(errs); await b.close(); })();
