const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--use-gl=swiftshader']}); const ctx = await b.newContext({viewport:{width:412,height:900}}); await ctx.route(/^https?:/, r => r.abort()); const p = await ctx.newPage(); const errs=[]; p.on('pageerror', e => errs.push(e.message));
  for (const f of ['bench_day6_prog_compiler','bench_day6_draw_animated_colors','bench_day6_math_dot_length','bench_day6_cad_refactoring','bench_day6']){
    await p.goto('file:///home/claude/bench2/offline/'+f+'.html'); await p.waitForTimeout(1200);
    console.log(f, await p.evaluate(() => [document.getElementById('ptitle').textContent, document.getElementById('stepOut').textContent, !!document.querySelector('canvas#gl')]));
  }
  console.log('ERR', errs); await b.close(); })();
