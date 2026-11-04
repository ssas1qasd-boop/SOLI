const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:1300,height:900}});
  const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  for (const [pg, id, o] of [['bench_day4.html','d4_v2','/tmp/claude-0/r1.png'],['bench_day1.html','d1_cam','/tmp/claude-0/r2.png']]){
    await p.goto('file:///home/claude/bench2/' + pg + '#' + id); await p.waitForTimeout(900);
    await p.click('#reftoggle'); await p.waitForTimeout(300);
    const d = await p.evaluate(() => document.getElementById('refthumb').toDataURL('image/png')); require('fs').writeFileSync(o, Buffer.from(d.split(',')[1], 'base64')); }
  console.log(errs); await b.close(); })();
