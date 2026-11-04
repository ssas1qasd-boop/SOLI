const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:860}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('http://127.0.0.1:8765/index.html'); await p.waitForFunction(() => !document.getElementById('bootMsg'), null, {timeout: 60000}); await p.waitForTimeout(1500);
  const r = await p.evaluate(async () => { const ids = window.__bench.progs().filter(x => x.day == 11).map(x => x.id); const out = [];
    for (const id of ids){ window.__bench.load(id); await new Promise(r => setTimeout(r, 300)); const st = window.__bench.st(); window.__bench.go(Math.min(5, st.length - 1)); out.push([id, st.length, window.__bench.text(Math.min(5, st.length - 1)).slice(0, 80)]); }
    return out; });
  console.log(JSON.stringify(r, null, 1), errs); await b.close(); })();
