const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1500);
  const r = await p.evaluate(() => { const B = window.__bench, out = []; B.load('d7_r2'); const n = B.st().length;
    out.push('start ' + JSON.stringify(B.dyn())); B.go(n - 1); out.push('end ' + JSON.stringify(B.dyn())); B.go(0); out.push('back to 1 ' + JSON.stringify(B.dyn()));
    B.go(Math.floor(n / 2)); out.push('middle ' + JSON.stringify(B.dyn())); B.go(n - 1); out.push('end again ' + JSON.stringify(B.dyn())); return out.join('\n'); });
  console.log(r); console.log('errors', errs); await b.close(); })();
