// Renders the share cards: node _src/og/render.js (from the repo root, with Playwright installed).
const { chromium } = require('playwright');
const path = require('path');
const CARDS = [
  { file: 'og-home.jpg',     h: 'Patience is',  g: 'a position.',  e: 'Day trader toolkit' },
  { file: 'og-tools.jpg',    h: 'Free prop',    g: 'simulators.',  e: 'Pass odds · payouts · sizing' },
  { file: 'og-research.jpg', h: 'Research,',    g: 'in the open.', e: 'Tested after costs' },
];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  const base = 'file://' + path.resolve(__dirname, 'card.html');
  for (const c of CARDS) {
    const q = new URLSearchParams({ h: c.h, g: c.g, e: c.e });
    await p.goto(`${base}?${q}`);
    await p.waitForLoadState('networkidle'); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.resolve(__dirname, '../../assets', c.file), type: 'jpeg', quality: 90 });
    console.log('wrote', c.file);
  }
  await b.close();
})();
