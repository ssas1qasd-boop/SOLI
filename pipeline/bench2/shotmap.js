const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1100,height:1300}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message)); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///tmp/claude-0/map/code_map_day7.html'); await p.waitForTimeout(500);
  await p.screenshot({path:'/tmp/claude-0/map/s1.png'}); console.log(errs); await b.close(); })();
