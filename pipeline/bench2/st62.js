const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage();
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1200); await p.evaluate(() => __bench.load('d7_r2'));
  const t = await p.evaluate(() => { window.__agent.ask('x'); const c = window.__agent.AG.context('الطريقتين VAO Buffer'); const lines = c.split('\n'); const k = lines.indexOf('أقرب السطور للسؤال (من البنش):'); return lines.slice(0, k).join('\n'); });
  fs.writeFileSync('/tmp/claude-0/facts_d7r2.txt', t); console.log(t.length); await b.close(); })();
