const { chromium } = require('playwright');
(async () => {
  const [,, prog, w, h, code] = process.argv;
  const b = await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
  const p = await b.newPage({viewport:{width:+w, height:+h}});
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'}));
  await p.route('https://fonts.googleapis.com/**', r => r.abort()); await p.route('https://fonts.gstatic.com/**', r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_days.html#' + prog);
  await p.waitForTimeout(1200);
  console.log(await p.evaluate(code));
  console.log('ERR', errs);
  await b.close();
})();
