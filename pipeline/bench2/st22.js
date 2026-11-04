const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}, colorScheme:'dark', deviceScaleFactor:2}); const errs=[]; p.on('pageerror', e => errs.push(e.message+' @'+(e.stack||'').split('\n')[1]));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  for (const id of ['d5_p1','d5_p2','d5_n1','d5_n2','d5_c1']){
    await p.goto('file:///home/claude/bench2/bench_day5.html#'+id); await p.waitForTimeout(900);
    await p.fill('#goN','10'); await p.click('#goStep button[type=submit]'); await p.waitForTimeout(1200);
    await p.click('#stoBtn'); await p.waitForTimeout(200); await p.click('#stoX'); await p.click('#stepsBtn'); await p.waitForTimeout(200); await p.click('#stX');
    console.log(id, await p.textContent('#stepOut'), '|', await p.textContent('#pdeck'), '|', (await p.textContent('#story')).slice(0,90));
  }
  await p.goto('file:///home/claude/bench2/bench_day5.html#d5_c1'); await p.waitForTimeout(900); await p.fill('#goN','17'); await p.click('#goStep button[type=submit]'); await p.waitForTimeout(1500);
  await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300); await p.screenshot({path:'/tmp/claude-0/c1a.png'});
  await p.evaluate(() => document.getElementById('ramList').scrollIntoView({block:'center'})); await p.waitForTimeout(300); await p.screenshot({path:'/tmp/claude-0/c1b.png'});
  console.log(errs.slice(0,5)); await b.close(); })();
