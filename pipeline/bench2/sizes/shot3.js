const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:412,height:900}, colorScheme:'dark', deviceScaleFactor:2});
  await p.route(/fonts\.g/, r => r.abort()); await p.goto('file:///home/claude/bench2/sizes/bytes.html'); await p.waitForTimeout(300);
  for (const [sel, o] of [['td.res-gpu', '/tmp/claude-0/m1.png'], ['td.res-exe', '/tmp/claude-0/m2.png']]){
    await p.evaluate(sel => { const s = document.querySelector('.scroller'); const c = document.querySelector('tbody ' + sel); s.scrollIntoView(); const r = c.getBoundingClientRect(), sr = s.getBoundingClientRect(); const st = document.querySelector('tbody th[scope=row]').getBoundingClientRect(); s.scrollLeft += (r.right - st.left) + 2; window.scrollBy(0, -170); }, sel);
    await p.waitForTimeout(200); await p.screenshot({path:o}); }
  console.log(await p.evaluate(() => { const bad = []; document.querySelectorAll('td').forEach(td => { if (td.scrollWidth > td.clientWidth + 2) bad.push(td.className); }); return bad.slice(0, 10); }));
  await b.close(); })();
