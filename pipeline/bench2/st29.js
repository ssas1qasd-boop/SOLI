const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}});
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_days.html'); await p.waitForTimeout(900);
  console.log(await p.evaluate(() => PROGS.map(q => { loadProgram(q.id); const s = cmdStats(); const fam = Object.values(s.fam).reduce((a, b) => a + b, 0), g = (s['CPU→GPU']||0) + (s.GPU||0), cpu = Object.values(s.cpu).reduce((a,b)=>a+b,0);
     const miss = ST.filter(x => x.u !== 'CPU' && !FAM.some(([,,,re]) => re.test(gfn(stepText(x)) || ''))).map(x => stepText(x)).slice(0,3);
     return (fam !== g || cpu !== (s.CPU||0)) ? `${q.id}: fam ${fam} vs ${g}, cpu ${cpu} vs ${s.CPU} ${JSON.stringify(miss)}` : null; }).filter(Boolean).join('\n') || 'all sums match'));
  await b.close(); })();
