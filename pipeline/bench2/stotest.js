const { chromium } = require('playwright');
(async () => {
  const [,, page, prog, w, h, out, theme] = process.argv;
  const b = await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
  const p = await b.newPage({viewport:{width:+w, height:+h}, colorScheme: theme});
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'}));
  await p.route('https://fonts.googleapis.com/**', r => r.abort()); await p.route('https://fonts.gstatic.com/**', r => r.abort());
  await p.goto('file:///home/claude/bench2/' + page + '#' + prog); await p.waitForTimeout(1200);
  console.log('hidden', await p.evaluate(() => document.getElementById('story2').hidden));
  await p.click('#stoBtn'); await p.waitForTimeout(600);
  console.log(await p.evaluate(() => [...document.querySelectorAll('.chap h5')].map(x => x.innerText.replace(/\n/g,' ')).join('\n')));
  await p.screenshot({path: out});
  await p.evaluate(() => document.getElementById('story2').scrollTop = 900); await p.waitForTimeout(200); await p.screenshot({path: out.replace('.png','b.png')});
  await p.locator('[data-go]').nth(3).click(); await p.waitForTimeout(400);
  console.log('after go', await p.evaluate(() => [document.getElementById('story2').hidden, document.getElementById('stepOut').textContent]), 'ERR', errs);
  await b.close();
})();
