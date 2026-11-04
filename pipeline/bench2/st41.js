const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day9.html'); await p.waitForTimeout(1500);
  const r = await p.evaluate(async () => { const B = window.__bench, out = [];
    for (const q of B.progs()){ B.load(q.id); const ST = B.st(); let w = 0; for (let k = 0; k < ST.length; k++){ try { B.why(k); } catch(e){ w++; } }
      out.push(q.id + ' steps ' + ST.length + ' whyErr ' + w + ' goal ' + (document.body.innerHTML.includes('السؤال') ? 'y' : '?')); }
    return out.join('\n'); });
  console.log(r); console.log('errors', errs);
  await p.screenshot({path:'/tmp/claude-0/b8.png'}); await b.close(); })();
