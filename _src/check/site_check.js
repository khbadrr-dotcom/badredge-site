// Weekly site check. Opens every page in sitemap.xml at phone and desktop width, in dark and light,
// and reports: script errors, missing files, broken pictures, sideways scroll, dead internal links,
// and share cards that do not exist.
//
//   node _src/check/site_check.js                 check the repo copy (served locally)
//   node _src/check/site_check.js --base https://badredge.com   check the live site
//   node _src/check/site_check.js --shots out/    also save a screenshot of every view
//
// Exit code 0 = clean, 1 = something needs a look. Needs Playwright.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const arg = n => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : null; };
const VIEWS = [['phone', 390, 844], ['desktop', 1280, 800]], THEMES = ['dark', 'light'];
const TYPES = { html: 'text/html', css: 'text/css', js: 'text/javascript', json: 'application/json', svg: 'image/svg+xml', webp: 'image/webp', jpg: 'image/jpeg', png: 'image/png', xml: 'text/xml', txt: 'text/plain', mp4: 'video/mp4', webm: 'video/webm' };

function resolveFile(urlPath) {
  let p = path.join(ROOT, decodeURIComponent(urlPath.split('?')[0].split('#')[0]));
  if (!p.startsWith(ROOT)) return null;
  if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
  return fs.existsSync(p) ? p : null;
}
function serve() {
  return new Promise(res => {
    const s = http.createServer((q, r) => {
      const f = resolveFile(q.url);
      if (!f) { r.writeHead(404, { 'content-type': 'text/html' }); return r.end(fs.readFileSync(path.join(ROOT, '404.html'))); }
      r.writeHead(200, { 'content-type': TYPES[f.split('.').pop()] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
    }).listen(0, '127.0.0.1', () => res(s));
  });
}

(async () => {
  const live = arg('--base'), shots = arg('--shots');
  const server = live ? null : await serve();
  const base = live ? live.replace(/\/$/, '') : `http://127.0.0.1:${server.address().port}`;
  const pages = [...fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8').matchAll(/<loc>https:\/\/badredge\.com([^<]*)<\/loc>/g)].map(m => m[1]);
  const redirects = fs.existsSync(path.join(ROOT, '_redirects')) ? fs.readFileSync(path.join(ROOT, '_redirects'), 'utf8').split('\n').map(l => l.split(' ')[0]) : [];
  if (shots) fs.mkdirSync(shots, { recursive: true });
  const browser = await chromium.launch();
  const issues = [], seenLinks = new Set(); let views = 0, slowest = [0, ''];
  const add = (page, view, what) => issues.push({ page, view, what });

  for (const [vname, w, h] of VIEWS) for (const theme of THEMES) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, colorScheme: theme, reducedMotion: 'reduce' });
    await ctx.addInitScript(t => { try { localStorage.setItem('be-theme', t); } catch (e) {} }, theme);
    const p = await ctx.newPage(); let cur = '', view = `${vname} ${theme}`;
    p.on('pageerror', e => add(cur, view, 'Script error: ' + String(e.message).slice(0, 140)));
    p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|net::ERR/.test(m.text())) add(cur, view, 'Console error: ' + m.text().slice(0, 140)); });
    p.on('response', r => { if (r.url().startsWith(base) && r.status() >= 400) add(cur, view, `Missing file (${r.status()}): ` + r.url().slice(base.length)); });
    for (const url of pages) {
      cur = url; views++;
      const t0 = Date.now();
      try { await p.goto(base + url, { waitUntil: 'load', timeout: 30000 }); } catch (e) { add(url, view, 'Did not load: ' + String(e.message).slice(0, 100)); continue; }
      const ms = Date.now() - t0; if (ms > slowest[0]) slowest = [ms, `${url} (${view})`];
      await p.waitForTimeout(250);
      const r = await p.evaluate(() => ({
        over: document.documentElement.scrollWidth - window.innerWidth,
        imgs: [...document.images].filter(i => i.complete && !i.naturalWidth && i.loading !== 'lazy').map(i => i.getAttribute('src')),
        links: [...document.querySelectorAll('a[href^="/"]')].map(a => a.getAttribute('href')),
        og: (document.querySelector('meta[property="og:image"]') || {}).content || '',
        title: document.title, h1: document.querySelectorAll('h1').length,
      }));
      if (r.over > 1) add(url, view, `Scrolls sideways by ${r.over}px`);
      r.imgs.forEach(s => add(url, view, 'Broken picture: ' + s));
      if (!r.title) add(url, view, 'No page title');
      if (vname === 'phone' && theme === 'dark') {       // content checks once per page
        if (!r.og) add(url, 'all', 'No share card set');
        else if (!live && !resolveFile(r.og.replace('https://badredge.com', ''))) add(url, 'all', 'Share card file missing: ' + r.og);
        if (!live) for (const l of r.links) {
          const k = l.split('#')[0].split('?')[0]; if (seenLinks.has(k)) continue; seenLinks.add(k);
          if (!resolveFile(k) && !redirects.includes(k)) add(url, 'all', 'Dead link: ' + l);
        }
      }
      if (shots) await p.screenshot({ path: path.join(shots, `${(url.replace(/\//g, '_') || '_home')}-${vname}-${theme}.jpg`), type: 'jpeg', quality: 60 });
    }
    await ctx.close();
  }
  await browser.close(); if (server) server.close();

  const uniq = [...new Map(issues.map(i => [i.page + i.view + i.what, i])).values()];
  console.log(`Site check: ${pages.length} pages, ${views} views (${live ? 'live site' : 'repo copy'}). Slowest load ${slowest[0]} ms on ${slowest[1]}.`);
  if (!uniq.length) { console.log('All clear.'); process.exit(0); }
  console.log(`${uniq.length} to look at:`);
  for (const i of uniq) console.log(`- ${i.page} [${i.view}] ${i.what}`);
  fs.writeFileSync(path.join(__dirname, 'last-report.json'), JSON.stringify(uniq, null, 1));
  process.exit(1);
})();
