const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']});
  for (const [pg, prog, o] of [['bench_day4.html','d4_v2','/tmp/claude-0/rf1.png'],['bench_day1.html','d1_cam','/tmp/claude-0/rf2.png']]){
  const p = await b.newPage({viewport:{width:1400,height:900}}); const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/' + pg + '#' + prog); await p.waitForTimeout(800);
  await p.click('#reftoggle'); await p.waitForTimeout(300);
  const d = await p.evaluate(() => document.getElementById('refthumb').toDataURL()); require('fs').writeFileSync(o, Buffer.from(d.split(',')[1], 'base64')); console.log(o, errs); await p.close(); }
  await b.close(); })();
