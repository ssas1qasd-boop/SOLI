const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:412,height:915}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_days.html'); await p.waitForTimeout(900);
  const out = await p.evaluate(() => { const B = window.__bench, R = []; let nul = 0, tot = 0;
    for (const q of B.progs()){ B.load(q.id); const ST = B.st();
      for (let k = 0; k < ST.length; k++){ let U; try { U = B.uses(k); } catch(e){ R.push('ERR ' + q.id + ' ' + e.message); continue; }
        if (!U || !U.uses.length) continue;
        for (const u of U.uses){ tot++; let r; try { r = B.role(U.v, u.j); } catch(e){ R.push('ERR ' + q.id + ' ' + e.message); continue; }
          if (!r) nul++; if (/^d7_r2|^d1_p4|^d2_c2/.test(q.id)) R.push(q.id + ' | ' + U.v + ' | ' + u.t + ' => ' + (r || '-').replace(/<[^>]+>/g, '')); } } }
    return 'total ' + tot + ' null ' + nul + '\n' + R.join('\n'); });
  console.log(errs.join('\n')); console.log(out); await b.close(); })();
