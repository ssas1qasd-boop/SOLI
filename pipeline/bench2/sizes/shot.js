const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); 
  for (const [w,h,t,o] of [[1400,900,'light','/tmp/claude-0/bt1.png'],[412,900,'dark','/tmp/claude-0/bt2.png']]){
  const p = await b.newPage({viewport:{width:w,height:h}, colorScheme:t, deviceScaleFactor: w<500?2:1});
  await p.route(/fonts\.g/, r => r.abort());
  await p.goto('file:///home/claude/bench2/sizes/bytes.html'); await p.waitForTimeout(400);
  if (w < 500) await p.evaluate(() => { const s = document.querySelector('.scroller'); s.scrollIntoView(); });
  else await p.evaluate(() => { document.querySelector('.scroller').scrollIntoView(); });
  await p.screenshot({path:o});
  console.log(await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]));
  }
  await b.close(); })();
