const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
  const p = await b.newPage({viewport:{width:1400, height:900}});
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'}));
  await p.route('https://fonts.googleapis.com/**', r => r.abort()); await p.route('https://fonts.gstatic.com/**', r => r.abort());
  await p.goto('file:///home/claude/bench2/' + (process.env.PAGE||'bench_days.html') + '');
  await p.waitForTimeout(1500);
  const ids = await p.evaluate(() => [...document.querySelectorAll('#picker button')].map(b => b.dataset.id));
  for (const id of ids){
    await p.click(`#picker button[data-id="${id}"]`); await p.waitForTimeout(300);
    const n = await p.evaluate(() => +document.getElementById('seek').max + 1);
    for (let k = 0; k < n; k += Math.max(1, Math.floor(n / 40))){ await p.evaluate(k => { const s = document.getElementById('seek'); s.value = k; s.dispatchEvent(new Event('input')); }, k); await p.waitForTimeout(40); }
    await p.evaluate(k => { const s = document.getElementById('seek'); s.value = k; s.dispatchEvent(new Event('input')); }, n - 1); await p.waitForTimeout(100);
    console.log(id, n, 'title=', await p.evaluate(() => document.getElementById('ptitle').textContent), 'errs', errs.length);
  }
  // overlays
  await p.click('#reftoggle'); await p.waitForTimeout(300); await p.click('#refthumb'); await p.waitForTimeout(500);
  await p.screenshot({path:'/tmp/claude-0/ref.png'}); await p.click('#refclose');
  await p.click('#glossBtn'); await p.fill('#glq', 'Callback'); await p.waitForTimeout(300); await p.screenshot({path:'/tmp/claude-0/gloss.png'});
  console.log('gloss items', await p.evaluate(() => document.querySelectorAll('#glList dt').length));
  console.log('ERRS', errs.slice(0, 5));
  await b.close();
})();
