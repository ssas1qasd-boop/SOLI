const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const errs=[]; const p = await b.newPage({viewport:{width:412,height:915}}); p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  const ids = JSON.parse(require('fs').readFileSync('progs.json')).programs.map(p=>[p.id,p.day]);
  for (const [id,d] of ids){
    await p.goto(`file:///home/claude/bench2/bench_day${d}.html#${id}`); await p.waitForTimeout(600); await p.click('#cmdBtn'); await p.waitForTimeout(150);
    const r = await p.evaluate(() => { const T=[...document.querySelectorAll('#cmdBody table')]; const tot = t => [...t.querySelectorAll('tr.tot td')].map(x=>x.innerText).join('/'); return T.map(tot).join(' | '); });
    console.log(id, r); await p.click('#cmdX'); }
  await p.goto('file:///home/claude/bench2/bench_days.html#d1_cam'); await p.waitForTimeout(700); console.log('combined btn', await p.evaluate(()=>!document.getElementById('cmdBtn').hidden));
  console.log(errs); await b.close(); })();
