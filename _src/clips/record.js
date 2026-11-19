// Records the "See it run" clips for the three simulators, with the tools' own example inputs.
//   node _src/clips/record.js [pass|payout|sizing]     (from the repo root; needs Playwright and ffmpeg)
// Output: assets/clips/<tool>.mp4 and <tool>.jpg (poster). Captions are drawn into the page while recording.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path'), os = require('os');
const ROOT = path.resolve(__dirname, '../..'), OUT = path.join(ROOT, 'assets/clips');
const TYPES = { html: 'text/html', css: 'text/css', js: 'text/javascript', svg: 'image/svg+xml', webp: 'image/webp', jpg: 'image/jpeg', png: 'image/png' };
const W = 1280, H = 720;

const OVERLAY = () => {
  const add = () => {
    const c = document.createElement('div'); c.id = 'rec-cur';
    c.style.cssText = 'position:fixed;left:0;top:0;width:22px;height:22px;margin:-11px 0 0 -11px;border-radius:50%;background:rgba(217,180,108,.35);box-shadow:0 0 0 2px #d9b46c;z-index:99999;pointer-events:none;transform:translate(640px,360px);transition:box-shadow .15s';
    const k = document.createElement('div'); k.id = 'rec-cap';
    k.style.cssText = 'position:fixed;left:50%;bottom:34px;transform:translateX(-50%);z-index:99998;pointer-events:none;padding:14px 26px;border-radius:14px;background:rgba(7,8,10,.92);box-shadow:0 0 0 1.5px rgba(217,180,108,.55),0 18px 50px rgba(0,0,0,.6);color:#ece8df;font:600 26px/1.2 Manrope,system-ui,sans-serif;white-space:nowrap;opacity:0;transition:opacity .3s';
    document.body.append(c, k);
    addEventListener('mousemove', e => { c.style.transform = `translate(${e.clientX}px,${e.clientY}px)`; }, true);
    addEventListener('mousedown', () => { c.style.boxShadow = '0 0 0 10px rgba(217,180,108,.45)'; setTimeout(() => c.style.boxShadow = '0 0 0 2px #d9b46c', 220); }, true);
  };
  document.body ? add() : addEventListener('DOMContentLoaded', add);
};

function helpers(p) {
  let mx = W / 2, my = H / 2;
  const wait = ms => p.waitForTimeout(ms);
  const cap = async (n, text) => { await p.evaluate(([n, t]) => { const k = document.getElementById('rec-cap'); k.innerHTML = (n ? `<span style="color:#d9b46c;font-family:'IBM Plex Mono',monospace;margin-right:14px">${n}</span>` : '') + t; k.style.opacity = 1; }, [n, text]); await wait(500); };
  const glide = async (x, y, ms = 700) => { const n = Math.round(ms / 16); for (let i = 1; i <= n; i++) { const t = i / n, e = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; await p.mouse.move(mx + (x - mx) * e, my + (y - my) * e); await wait(16); } mx = x; my = y; };
  const scroll = async (y, ms = 900) => { await p.evaluate(([y, ms]) => new Promise(r => { const y0 = scrollY, t0 = performance.now(); (function f(t) { const k = Math.min(1, (t - t0) / ms), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; scrollTo(0, y0 + (y - y0) * e); k < 1 ? requestAnimationFrame(f) : r(); })(t0); }), [y, ms]); await wait(150); };
  const to = async (sel, ms) => { const el = p.locator(sel).first(); const top = await el.evaluate(e => e.getBoundingClientRect().top + scrollY); const cur = await p.evaluate(() => scrollY); if (top - cur < 110 || top - cur > H - 230) await scroll(Math.max(0, top - 300)); const b = await el.boundingBox(); await glide(b.x + Math.min(b.width / 2, 120), b.y + b.height / 2, ms); return el; };
  const type = async (sel, val) => { const el = await to(sel); await el.click({ clickCount: 3 }); await wait(200); await p.keyboard.type(String(val), { delay: 130 }); await el.evaluate(e => e.blur()); await wait(450); };
  const pick = async (sel, val) => { const el = await to(sel); await p.mouse.down(); await p.mouse.up(); await wait(250); await el.selectOption(val); await wait(900); };
  const click = async sel => { await to(sel); await wait(250); await p.mouse.down(); await p.mouse.up(); };
  return { wait, cap, glide, scroll, to, type, pick, click };
}

const CLIPS = {
  async pass(p, h) {
    await h.cap('', 'Prop Pass Simulator · example inputs'); await h.wait(1300);
    await h.cap('1', 'Set the account rules'); await h.pick('#preset', 'a100'); await h.type('#maxDays', 45);
    await h.cap('2', "Enter your strategy's numbers"); await h.type('#wr', 55); await h.type('#aw', 10);
    await h.cap('3', 'Run thousands of attempts'); await h.click('#runBtn'); await h.wait(900);
    await h.scroll(150, 1100); await h.cap('4', 'Read the pass odds, the size and the days');
    await h.glide(480, 330, 900); await h.wait(900); await h.glide(980, 300, 900); await h.wait(700);
    await h.scroll(560, 1600); await h.glide(820, 330, 800); await h.wait(1600);
  },
  async payout(p, h) {
    await h.cap('', 'Payout Simulator · example inputs'); await h.wait(1300);
    await h.cap('1', 'Set the funded account and payout rules'); await h.type('#mll', 1200); await h.type('#cap', 1500);
    await h.cap('2', "Enter your strategy's numbers"); await h.type('#wr', 52); await h.type('#tpd', 1);
    await h.cap('3', 'Run thousands of attempts'); await h.click('#runBtn'); await h.wait(900);
    await h.scroll(130, 1100); await h.cap('4', 'Read the first-payout odds and the timing');
    await h.glide(480, 330, 900); await h.wait(900); await h.glide(900, 330, 900); await h.wait(700);
    await h.scroll(540, 1600); await h.glide(820, 330, 800); await h.wait(1600);
  },
  async sizing(p, h) {
    await h.wait(3500);   // the page runs the examples once on load
    await h.cap('', 'Contract Sizing Simulator · example data'); await h.wait(1300);
    await h.cap('1', 'Load your trade lists'); await h.glide(190, 335, 800); await h.wait(700); await h.glide(190, 560, 700); await h.wait(600);
    await h.cap('2', "Enter today's balance"); await h.type('#a-bal', 51400); await h.type('#a-peak', 51400);
    await h.cap('3', 'Run the simulation'); await h.click('#btn-run'); await h.wait(3600);
    await h.cap('4', 'Read the size for each strategy'); await h.glide(520, 425, 800); await h.wait(700); await h.glide(980, 425, 1100); await h.wait(700);
    await h.scroll(420, 1600); await h.glide(820, 300, 800); await h.wait(1600);
  },
};

(async () => {
  const names = process.argv[2] ? [process.argv[2]] : Object.keys(CLIPS);
  fs.mkdirSync(OUT, { recursive: true });
  const srv = http.createServer((q, r) => { let f = path.join(ROOT, q.url.split('?')[0]); if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html'); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': TYPES[f.split('.').pop()] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); });
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const b = await chromium.launch();
  for (const name of names) {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'clip-'));
    const ctx = await b.newContext({ viewport: { width: W, height: H }, colorScheme: 'dark', recordVideo: { dir: tmp, size: { width: W, height: H } } });
    await ctx.addInitScript(() => { try { localStorage.clear(); localStorage.setItem('be-theme', 'dark'); } catch (e) {} });
    await ctx.addInitScript(OVERLAY);
    const p = await ctx.newPage(); const t0 = Date.now();
    await p.goto(`http://127.0.0.1:${srv.address().port}/tools/${name}/`, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(700);
    const lead = (Date.now() - t0) / 1000;
    await CLIPS[name](p, helpers(p));
    await p.evaluate(() => document.getElementById('rec-cap').style.opacity = 0); await p.waitForTimeout(500);
    const dur = (Date.now() - t0) / 1000 - lead;
    await ctx.close();
    const webm = path.join(tmp, fs.readdirSync(tmp)[0]), mp4 = path.join(OUT, name + '.mp4');
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', lead.toFixed(2), '-i', webm, '-t', dur.toFixed(2), '-an', '-vf', 'fps=24,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '30', '-movflags', '+faststart', mp4]);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-sseof', '-1.2', '-i', mp4, '-frames:v', '1', '-q:v', '4', path.join(OUT, name + '.jpg')]);
    console.log(name, dur.toFixed(1) + 's', (fs.statSync(mp4).size / 1024).toFixed(0) + ' KB');
  }
  await b.close(); srv.close();
})();
