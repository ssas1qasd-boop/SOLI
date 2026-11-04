const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const errs=[];
 for (const [w,cs] of [[412,'dark'],[1280,'light']]){ const p = await b.newPage({viewport:{width:w,height:915}, colorScheme:cs, deviceScaleFactor:2}); p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day4.html#d4_v2'); await p.waitForTimeout(1000);
  await p.fill('#goN','6'); await p.click('#goStep button[type=submit]'); await p.waitForTimeout(1200);
  const n = await p.evaluate(() => document.querySelectorAll('#live .lc').length + ' visible=' + [...document.querySelectorAll('#live .lc')].filter(d=>d.style.display!=='none').length);
  console.log(w, 'callouts', n);
  await p.evaluate(() => document.getElementById('stage').scrollIntoView({block:'start'})); await p.waitForTimeout(500); console.log(w, 'lc rect', await p.evaluate(() => { const d=[...document.querySelectorAll('#live .lc')].find(d=>d.style.display!=='none'); const r=d.getBoundingClientRect(); return [Math.round(r.left),Math.round(r.top),innerHeight].join(','); })); await p.locator('#live .lc >> visible=true').first().click(); await p.waitForTimeout(900);
  console.log(w, 'after click: codeFig top', await p.evaluate(() => Math.round(document.getElementById('codeFig').getBoundingClientRect().top)), 'flash', await p.evaluate(() => !!document.querySelector('#code div.flash')));
  // gear alignment: compare gear top vs row top
  console.log(w, 'align', await p.evaluate(() => [...document.querySelectorAll('#drvGutIn b')].slice(0,4).map(g => { const r = document.getElementById('L'+g.dataset.v).getBoundingClientRect(), q = g.getBoundingClientRect(); return Math.round(q.top - r.top) + '/' + Math.round(q.height - r.height); }).join(' ')));
  await p.waitForTimeout(400); await (await p.$('#codeFig')).screenshot({path:`/tmp/claude-0/cf${w}.png`});
  // copy test: selection text of code box contains no gear
  console.log(w, 'gear in code text:', await p.evaluate(() => document.getElementById('code').innerText.includes('⚙')));
  // gear click goes to step
  await p.evaluate(() => { const c = document.getElementById('code'); c.scrollTop = 0; c.dispatchEvent(new Event('scroll')); });
  await p.evaluate(() => document.querySelector('#drvGutIn b').click()); await p.waitForTimeout(300); console.log(w, 'gear->', await p.textContent('#stepOut'));
  await p.close(); }
 console.log(errs); await b.close(); })();
