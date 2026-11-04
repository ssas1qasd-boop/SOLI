const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const errs=[];
  for (const [day, id, w, scheme] of [[7,'d7-r2',412,'dark'],[5,'d5-n1',412,'light'],[1,'d1-cam',1100,'light']]) {
    const p = await b.newPage({viewport:{width:w,height:1400}, colorScheme:scheme}); p.on('pageerror',e=>errs.push(e.message)); await p.route(/fonts\.g/, r => r.abort());
    await p.goto(`file:///home/claude/maps/out/day${day}.html#${id}`); await p.waitForTimeout(400);
    await p.evaluate(i=>{const f=document.querySelector('#'+i+' .frame'); f.style.overflow='visible'; f.closest('main').style.maxWidth='none'; document.body.style.width='880px';}, id); const el = await p.$('#'+id+' .frame svg'); await el.screenshot({path:`/tmp/claude-0/m_${id}.png`});
    console.log(id, 'scrollW', await p.evaluate(()=>document.documentElement.scrollWidth));
    await p.close(); }
  console.log(errs); await b.close(); })();
