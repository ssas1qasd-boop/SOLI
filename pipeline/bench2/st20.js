const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const errs=[]; const p = await b.newPage({viewport:{width:412,height:915}, colorScheme:'dark', deviceScaleFactor:2}); p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  for (const id of ['d5_r1','d5_r2','d5_c2']){
    await p.goto('file:///home/claude/bench2/bench_day5.html#'+id); await p.waitForTimeout(900);
    console.log(id, await p.textContent('#stepOut'), await p.evaluate(() => document.getElementById('ptitle').textContent));
    await p.click('#stoBtn'); await p.waitForTimeout(200); await p.click('#stoX');
    await p.click('#stepsBtn'); await p.waitForTimeout(200); await p.click('#stX');
  }
  // keyboard step
  await p.fill('#goN','292'); await p.click('#goStep button[type=submit]'); await p.waitForTimeout(1600);
  console.log('story:', (await p.textContent('#story')).slice(0,200));
  await p.evaluate(() => scrollTo(0,0)); await p.waitForTimeout(400); await p.screenshot({path:'/tmp/claude-0/b5key.png'});
  await p.goto('file:///home/claude/bench2/bench_days.html#d5_c2'); await p.waitForTimeout(900);
  console.log('combined picker:', await p.evaluate(() => [...document.querySelectorAll('#picker button, #picker a')].map(x=>x.textContent.trim()).slice(-5).join(' | ')));
  console.log(errs); await b.close(); })();
