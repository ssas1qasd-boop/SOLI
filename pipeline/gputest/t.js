const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({args:['--enable-unsafe-webgpu','--use-angle=swiftshader','--enable-features=Vulkan']}); const p = await b.newPage({viewport:{width:412,height:915}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message)); await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/gputest/gpu_check.html'); await p.waitForTimeout(8000);
  console.log((await p.innerText('main')).replace(/\s+/g,' ').slice(0, 900)); console.log(errs); await b.close(); })();
