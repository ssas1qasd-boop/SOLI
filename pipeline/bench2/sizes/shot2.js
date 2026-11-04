const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1500,height:950}});
  await p.route(/fonts\.g/, r => r.abort()); await p.goto('file:///home/claude/bench2/sizes/bytes.html'); await p.waitForTimeout(300);
  for (const [sel, o] of [['.gpu', '/tmp/claude-0/bt3.png'], ['td.exe', '/tmp/claude-0/bt4.png']]){
    await p.evaluate(sel => { const s = document.querySelector('.scroller'); const c = document.querySelector('tbody ' + sel); s.scrollIntoView(); const r = c.getBoundingClientRect(), sr = s.getBoundingClientRect(); s.scrollLeft += (r.right - sr.right) + 180; window.scrollBy(0, 40); }, sel);
    await p.waitForTimeout(200); await p.screenshot({path:o}); }
  await b.close(); })();
