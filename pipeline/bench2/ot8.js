const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const ctx = await b.newContext({viewport:{width:412,height:900}}); await ctx.route(/^https?:/, r => r.abort()); const p = await ctx.newPage(); const errs=[]; p.on('pageerror', e => errs.push(e.message));
  for (const f of ['bench_day7_prog_pointers_review','bench_day7_draw_vertex_arrays','bench_day7_math_cross_quiz','bench_day7_cad_commit_id','bench_day7']){
    await p.goto('file:///home/claude/bench2/offline/'+f+'.html'); await p.waitForTimeout(1200);
    console.log(f, await p.evaluate(() => [document.getElementById('ptitle').textContent, document.getElementById('stepOut').textContent, !!document.querySelector('canvas#gl')]));
  }
  console.log('ERR', errs); await b.close(); })();
