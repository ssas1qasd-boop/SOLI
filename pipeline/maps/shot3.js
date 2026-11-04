const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:800,height:800}, colorScheme: process.argv[2]});
  await p.goto('file:///tmp/claude-0/svgtest.html'); await p.waitForTimeout(200); await (await p.$('svg')).screenshot({path: process.argv[3]}); await b.close(); })();
