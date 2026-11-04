const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_days.html'); await p.waitForTimeout(2500);
  const r = await p.evaluate(() => { const out = []; const qs = ['كام Buffer؟', 'كام VAO؟', 'ليه بنعمل لوب؟', 'النتيجة طلعت إيه؟', 'الخطوة دي بتعمل إيه؟', 'كام خطوة؟', 'Texture يعني إيه؟', 'ليه الـ class فيه public؟', 'إيه الفرق بين struct و class؟', 'alpha طلعت كام؟'];
    for (const q of __bench.progs()){ __bench.load(q.id); const t0 = performance.now(); const L = qs.map(x => { const a = __bench.agent(x); const d = document.createElement('div'); d.innerHTML = a ? a.html : ''; return (a && a.low ? '∅' : '✓') + d.innerText.replace(/\s+/g, ' ').slice(0, 70); }); out.push(q.id + ' (' + Math.round(performance.now() - t0) + 'ms)\n   ' + L.join('\n   ')); }
    return out.join('\n'); });
  console.log(r); console.log('errors', errs); await b.close(); })();
