const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}, colorScheme:'dark', deviceScaleFactor:2}); const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  for (const id of ['d5_c1','d5_n2','d5_c2']){
  await p.goto('file:///home/claude/bench2/bench_day5.html#'+id); await p.waitForTimeout(900); await p.click('#stoBtn'); await p.waitForTimeout(300);
  await p.evaluate(() => document.querySelectorAll('.sto details.sec').forEach((d,k) => d.open = k < 4));
  console.log(id, await p.evaluate(() => [...document.querySelectorAll('.sto .chain .row')].map(x=>x.innerText.replace(/\s+/g,' ')).join(' / ')));
  if (id==='d5_c1') await (await p.$('#story2')).screenshot({path:'/tmp/claude-0/sto_c1.png'});
  await p.click('#stoX'); }
  await p.goto('file:///home/claude/bench2/bench_day5.html#d5_c1'); await p.waitForTimeout(900); await p.fill('#goN','21'); await p.click('#goStep button[type=submit]'); await p.waitForTimeout(1500);
  await p.evaluate(() => document.getElementById('ramList').scrollIntoView({block:'center'})); await p.waitForTimeout(300); await p.screenshot({path:'/tmp/claude-0/c1c.png'});
  console.log(errs); await b.close(); })();
