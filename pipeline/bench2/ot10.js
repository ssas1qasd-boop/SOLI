const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const ctx = await b.newContext({viewport:{width:412,height:900}}); await ctx.route(/^https?:/, r => r.abort()); const p = await ctx.newPage(); const errs=[]; p.on('pageerror', e => errs.push(e.message));
  for (const f of ['bench_week3_day2_prog_struct_class','bench_week3_day2_draw_stb_image','bench_week3_day2_math_transformations','bench_week3_day2_cad_triangle_mesh','bench_week3_day2','bench_day7']){
    await p.goto('file:///home/claude/bench2/offline/'+f+'.html'); await p.waitForTimeout(1200);
    console.log(f, await p.evaluate(() => [document.getElementById('ptitle').textContent, document.getElementById('stepOut').textContent, !!document.querySelector('canvas#gl')]));
  }
  console.log('ERR', errs); await b.close(); })();
