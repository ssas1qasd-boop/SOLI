const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const p = await b.newPage({viewport:{width:412,height:915}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('**/three.min.js', r => r.fulfill({path:'/home/claude/sim/three.min.js', contentType:'application/javascript'})); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/bench_day7.html'); await p.waitForTimeout(1500); await p.evaluate(() => __bench.load('d7_r2'));
  const last = async () => (await p.$$eval('.agmsg.bot', els => els.map(e => e.innerText.replace(/\s+/g,' ')))).pop().slice(0, 170);
  await p.click('#agFab');
  // teach: "الحاجة اللي بتعرض الصورة" -> glfwSwapBuffers
  await p.fill('#agQ', 'انهي سطر بيظهّر الرسمة للمستخدم'); await p.press('#agQ', 'Enter'); await p.waitForTimeout(500); console.log('1st:', await last());
  await p.click('.agmsg.bot:last-of-type .agdown'); await p.waitForTimeout(200);
  const alts = await p.$$eval('.agmsg.bot:last-of-type .agpick', els => els.map(e => e.innerText.replace(/\s+/g,' ').slice(0, 60))); console.log('alts:', alts);
  const n = alts.findIndex(a => /SwapBuffers/.test(a)); console.log('pick', n);
  await p.fill('.agmsg.bot:last-of-type .agline input', '179'); await p.press('.agmsg.bot:last-of-type .agline input', 'Enter'); await p.waitForTimeout(200); console.log('taught:', await last());
  for (const q2 of ['الرسمة بتظهر للمستخدم امتي', 'امتي المستخدم بيشوف الرسمة']){ await p.fill('#agQ', q2); await p.press('#agQ', 'Enter'); await p.waitForTimeout(500); console.log(q2, '=>', await last()); }
  await p.fill('#agQ', 'الرسمة بتظهر للمستخدم امتي'); await p.press('#agQ', 'Enter'); await p.waitForTimeout(500); console.log('after:', await last());
  for (const q2 of ['انهي سطر بيرسم المثلث', 'كام أمر رسم في اللفة؟', 'المستخدم بيقفل الشباك ازاي']){ await p.fill('#agQ', q2); await p.press('#agQ', 'Enter'); await p.waitForTimeout(500); console.log(q2, '=>', await last()); }
  await p.click('#agBrain'); await p.waitForTimeout(200); console.log('brain:', await last());
  const exp = await p.evaluate(() => window.__agent.AG.exportModel().length); console.log('export chars', exp);
  console.log(errs); await b.close(); })();
