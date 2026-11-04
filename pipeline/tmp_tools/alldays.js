const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
  for (let d = 1; d <= 11; d++){ const p = await b.newPage({viewport:{width:412,height:860}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message)); await p.route(/fonts\.g/, r => r.abort());
    await p.goto(`file:///home/claude/maps/out/day${d}.html`); await p.waitForTimeout(300);
    const r = await p.evaluate(async () => { const out = []; for (const sec of document.querySelectorAll('.prog')){ sec.querySelector('.pd').open = true;
      const pl = sec.querySelector('.npl'), go = sec.querySelector('.ngo[data-k="step"]'), inp = sec.querySelector('.ni[data-k="step"]');
      if (go){ inp.value = 3; go.click(); out.push(sec.querySelectorAll('.blk.glow').length); } } return out; });
    console.log(d, JSON.stringify(r), errs); await p.close(); }
  await b.close(); })();
