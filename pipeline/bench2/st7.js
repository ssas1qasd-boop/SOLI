const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:900}, colorScheme:'dark', deviceScaleFactor:2});
  const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  for (const [pg,ids] of [['bench_day1.html',['d1_u1','d1_u2','d1_cam']],['bench_day2.html',['d2_va1','d2_va2']],['bench_day3.html',['d3_s1','d3_l1','d3_l2']],['bench_day4.html',['d4_e1','d4_e2','d4_v1','d4_v2']]]) for (const id of ids){
    await p.goto('file:///home/claude/bench2/'+pg+'#'+id); await p.waitForTimeout(700); await p.click('#stoBtn'); await p.waitForTimeout(250);
    console.log(id, await p.evaluate(() => { const r=[...document.querySelectorAll('.drvt tbody tr')]; return r.length+' rows, gears='+document.querySelectorAll('#code div.drv').length+' | '+r.slice(4,7).map(x=>x.innerText.replace(/\s+/g,' ').slice(0,160)).join(' || '); }));
    if (id==='d3_l2'){ await (await p.$('.drvt')).screenshot({path:'/tmp/claude-0/drv.png'}); await p.click('#stoX'); await (await p.$('#code')).screenshot({path:'/tmp/claude-0/code.png'}); }
    else await p.click('#stoX'); }
  console.log(errs); await b.close(); })();
