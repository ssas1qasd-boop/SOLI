const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const ctx = await b.newContext({viewport:{width:412,height:900}}); await ctx.route(/^https?:/, r => r.abort()); const p = await ctx.newPage(); const errs=[]; p.on('pageerror', e => errs.push(e.message));
  for (const f of ['bench_day1_prog_pointers','bench_day1_math_dot','bench_day2_prog_c','bench_day2_math_dot_length','bench_day2_cad_vector_points','bench_day3_prog_references','bench_day3_math_cross','bench_day4_prog_static_const','bench_day4_math_cross_khan']){
    await p.goto('file:///home/claude/bench2/offline/'+f+'.html'); await p.waitForTimeout(900);
    console.log(f, await p.evaluate(() => [document.getElementById('ptitle').textContent, document.getElementById('stepOut').textContent, document.body.classList.contains('nogl')]));
  }
  console.log('ERR', errs); await b.close(); })();
