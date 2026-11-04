const { chromium } = require('playwright');
(async () => {
  const [,, page, prog, w, h, step, out, theme] = process.argv;
  const b = await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
  const p = await b.newPage({viewport:{width:+w, height:+h}, colorScheme: theme});
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'}));
  await p.route('https://fonts.googleapis.com/**', r => r.abort()); await p.route('https://fonts.gstatic.com/**', r => r.abort());
  await p.goto('file:///home/claude/bench2/' + page + '#' + prog); await p.waitForTimeout(1200);
  await p.evaluate(k => { const s = document.getElementById('seek'); s.value = k; s.dispatchEvent(new Event('input')); }, +step); await p.waitForTimeout(800);
  console.log('hidden before', await p.evaluate(() => document.getElementById('legend').hidden));
  await p.click('#legBtn'); await p.waitForTimeout(2500);
  await p.screenshot({path: out});
  console.log('imgs', await p.evaluate(() => [...document.querySelectorAll('#legList img')].filter(i => i.src.startsWith('data:image/png')).length));
  await p.click('#legBtn'); await p.waitForTimeout(300);
  console.log('hidden after', await p.evaluate(() => document.getElementById('legend').hidden), 'ERR', errs);
  await b.close();
})();
