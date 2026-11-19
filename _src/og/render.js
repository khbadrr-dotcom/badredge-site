// Renders the share cards (from the repo root, with Playwright installed):
//   node _src/og/render.js          per-page cards listed in cards.json -> assets/og/
//   node _src/og/render.js sections  the three section cards -> assets/og-*.jpg
// cards.json is written by build.py (og_cards), so run the build first.
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const SECTIONS = [
  { file: '../og-home.jpg',     h: 'Patience is',  g: 'a position.',  e: 'Day trader toolkit' },
  { file: '../og-tools.jpg',    h: 'Free prop',    g: 'simulators.',  e: 'Pass odds · payouts · sizing' },
  { file: '../og-research.jpg', h: 'Research,',    g: 'in the open.', e: 'Tested after costs' },
];
const CARDS = process.argv[2] === 'sections' ? SECTIONS : JSON.parse(fs.readFileSync(path.resolve(__dirname, 'cards.json'), 'utf8'));
(async () => {
  const out = path.resolve(__dirname, '../../assets/og'); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  const base = 'file://' + path.resolve(__dirname, 'card.html');
  for (const c of CARDS) {
    const q = new URLSearchParams({ h: c.h, g: c.g, e: c.e, f: c.f || '' });
    await p.goto(`${base}?${q}`);
    await p.waitForLoadState('networkidle'); await p.waitForSelector('body[data-ready]');
    await p.screenshot({ path: path.resolve(out, c.file), type: 'jpeg', quality: 86 });
  }
  console.log('wrote', CARDS.length, 'cards');
  await b.close();
})();
