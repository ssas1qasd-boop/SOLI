const { chromium } = require('playwright');
(async () => {
  const [,, page, prog, out] = process.argv;
  const b = await chromium.launch({args:['--use-gl=swiftshader']});
  const p = await b.newPage({viewport:{width:412, height:900}, colorScheme:'dark', deviceScaleFactor:2});
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'}));
  await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/' + page + '#' + prog); await p.waitForTimeout(1000);
  await p.click('#stoBtn'); await p.waitForTimeout(400);
  const y = await p.evaluate(() => { const c = document.querySelectorAll('.chap')[1]; return c.offsetTop; });
  await p.evaluate(y => document.getElementById('story2').scrollTop = y - 60, y); await p.waitForTimeout(200);
  await p.screenshot({path: out});
  console.log(await p.evaluate(() => document.querySelector('.brk') && document.querySelector('.brk').innerText));
  await p.locator('.cl li button').nth(2).click(); await p.waitForTimeout(300);
  console.log('go ->', await p.evaluate(() => document.getElementById('stepOut').textContent), 'ERR', errs);
  await b.close(); })();
