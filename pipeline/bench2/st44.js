const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1500);
  await p.evaluate(() => __bench.load('d7_r2'));
  const qs = ['ليه عملت 3 صناديق؟','كام VAO؟','إيه الفرق بين الطريقتين؟','squareBuffer اتعمل فين؟','قيمة triangleVao في خطوة 40','الخطوة دي بتعمل إيه؟','يعني إيه EBO؟','النتيجة طلعت إيه؟','كام أمر رسم في اللفة؟','ليه بنعمل لوب؟','glVertexAttribPointer بيعمل إيه','روح لسطر 98','طب والمثلث؟','إيه علاقة الماوس بالبرنامج'];
  for (const q of qs){ const r = await p.evaluate(q => { const r = __bench.agent(q); const d = document.createElement('div'); d.innerHTML = r ? r.html : ''; return r ? (r.conf.toFixed(2) + ' | ' + d.innerText.replace(/\s+/g,' ').slice(0, 330)) : 'NULL'; }, q); console.log('Q:', q, '\n  ', r); }
  console.log('errors', errs); await b.close(); })();
