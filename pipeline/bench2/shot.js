const { chromium } = require('playwright');
(async () => {
  const [,, prog, w, h, steps, out, theme] = process.argv;
  const b = await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
  const p = await b.newPage({viewport:{width:+w, height:+h}, colorScheme: theme || 'light'});
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'}));
  await p.route('https://fonts.googleapis.com/**', r => r.abort()); await p.route('https://fonts.gstatic.com/**', r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_days.html#' + prog);
  await p.waitForTimeout(1500);
  for (const k of steps.split(',')) {
    await p.evaluate(k => { const s = document.getElementById('seek'); s.value = k; s.dispatchEvent(new Event('input')); }, +k);
    await p.waitForTimeout(+(process.env.WAIT||2500));
  }
  await p.screenshot({path: out, fullPage: true});
  console.log('ERRORS', JSON.stringify(errs));
  console.log(await p.evaluate(() => document.getElementById('story').innerText.slice(0, 400)));
  await b.close();
})();
