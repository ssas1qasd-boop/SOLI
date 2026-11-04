const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const ctx = await b.newContext({viewport:{width:412,height:900}}); await ctx.route(/^https?:/, r => r.abort()); const p = await ctx.newPage(); const errs=[]; p.on('pageerror', e => errs.push(e.message));
  for (const f of ['bench_day5_draw_shader_edit','bench_day5_cad_delete_last_line','bench_day5_prog_swap','bench_day5_math_numpy','bench_day5']){
    await p.goto('file:///home/claude/bench2/offline/'+f+'.html'); await p.waitForTimeout(1200);
    console.log(f, await p.evaluate(() => [document.getElementById('ptitle').textContent, document.getElementById('stepOut').textContent, !!document.querySelector('canvas#gl')]));
  }
  console.log('ERR', errs); await b.close(); })();
