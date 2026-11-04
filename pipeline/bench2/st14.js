const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const errs=[]; const p = await b.newPage({viewport:{width:412,height:915}}); p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  for (const id of JSON.parse(require('fs').readFileSync('progs.json')).programs.map(p=>p.id)){
    await p.goto('file:///home/claude/bench2/bench_days.html#'+id); await p.waitForTimeout(600); await p.click('#stepsBtn'); await p.waitForTimeout(200);
    console.log(id, await p.evaluate(() => document.querySelectorAll('#stList li').length + ' / ' + document.getElementById('stepOut').textContent + ' emptyEx=' + [...document.querySelectorAll('#stList .ex')].filter(x=>!x.textContent.trim()).length + ' dots=' + [...document.querySelectorAll('#stList .ex')].filter(x=>/…/.test(x.textContent)).length)); }
  console.log(errs); await b.close(); })();
