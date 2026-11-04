const { chromium } = require('playwright');
(async () => {
  const [,, prog, w, h, step, out, theme, sel] = process.argv;
  const b = await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
  const p = await b.newPage({viewport:{width:+w, height:+h}, colorScheme: theme || 'light', deviceScaleFactor: 1});
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'}));
  await p.route('https://fonts.googleapis.com/**', r => r.abort()); await p.route('https://fonts.gstatic.com/**', r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day3.html#' + prog);
  await p.waitForTimeout(1200);
  await p.evaluate(k => { const s = document.getElementById('seek'); s.value = k; s.dispatchEvent(new Event('input')); }, +step);
  await p.evaluate(sel => document.querySelector(sel).scrollIntoView({block:'start'}), sel || '#stage');
  await p.waitForTimeout(+(process.env.WAIT || 3000));
  await p.screenshot({path: out});
  console.log('ERRORS', JSON.stringify(errs));
  await b.close();
})();
