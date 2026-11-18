/* Badr Edge theme toggle. The inline script in <head> sets html[data-theme]
   before paint (saved choice, else the system setting); this file wires the
   .theme-btn buttons, saves the visitor's choice and follows system changes
   until the visitor picks a theme. */
(() => {
  const root = document.documentElement, KEY = 'be-theme';
  const saved = () => { try { return localStorage.getItem(KEY); } catch (e) { return null; } };
  const apply = (t, save) => {
    root.setAttribute('data-theme', t);
    const m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute('content', t === 'light' ? '#f7f4ee' : '#07080a');
    document.querySelectorAll('.theme-btn').forEach(b => {
      const label = t === 'light' ? 'Switch to dark theme' : 'Switch to light theme';
      b.setAttribute('aria-label', label); b.setAttribute('title', label);
    });
    if (save) { try { localStorage.setItem(KEY, t); } catch (e) {} }
  };
  apply(root.getAttribute('data-theme') === 'light' ? 'light' : 'dark');
  document.addEventListener('click', e => {
    if (e.target.closest && e.target.closest('.theme-btn')) apply(root.getAttribute('data-theme') === 'light' ? 'dark' : 'light', true);
  });
  try {
    matchMedia('(prefers-color-scheme: light)').addEventListener('change', e => {
      const s = saved(); if (s !== 'light' && s !== 'dark') apply(e.matches ? 'light' : 'dark');
    });
  } catch (e) {}
})();

// Hero candles: each orbiting candle ticks like a live bar. Price wanders,
// the body follows open-to-close, wicks keep the session high and low, and
// the colour flips when price crosses the open. A new bar starts every ~12s.
(function () {
  var els = document.querySelectorAll('.cdl');
  if (!els.length) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var pct = function (v) { return (50 - v * 46).toFixed(1) + '%'; };   // price -1..1 -> top %
  var bars = Array.prototype.map.call(els, function (el, i) {
    return { el: el, o: 0, c: 0, h: 0, l: 0, n: 0, len: 0, bias: 0, seed: i };
  });
  function newBar(b) {
    b.o = b.c = b.h = b.l = (Math.random() - .5) * .5;
    b.n = 0; b.len = 14 + Math.floor(Math.random() * 10);           // ticks per bar
    b.bias = (Math.random() < .6 ? 1 : -1) * (.06 + Math.random() * .06);
  }
  function draw(b) {
    var top = Math.max(b.o, b.c), bot = Math.min(b.o, b.c);
    var m = (top + bot) / 2, half = .3;                               // keep the body tall enough to read
    if (top - bot < half * 2) { top = Math.min(1, m + half); bot = Math.max(-1, m - half); }
    var s = b.el.style;
    var wh = Math.min(1, Math.max(b.h, top) + .24), wl = Math.max(-1, Math.min(b.l, bot) - .24);   // a short tail beyond the extremes
    s.setProperty('--wt', pct(wh)); s.setProperty('--wb', (100 - parseFloat(pct(wl))).toFixed(1) + '%');
    s.setProperty('--bt', pct(top)); s.setProperty('--bb', (100 - parseFloat(pct(bot))).toFixed(1) + '%');
    b.el.classList.toggle('up', b.c >= b.o); b.el.classList.toggle('dn', b.c < b.o);
  }
  function tick() {
    if (document.hidden) return;
    bars.forEach(function (b) {
      if (b.n >= b.len) newBar(b);
      if (Math.random() < .1) b.bias = -b.bias * (.6 + Math.random() * .6);   // pullbacks and reversals
      b.c = Math.max(-1, Math.min(1, b.c + b.bias + (Math.random() - .5) * .3));
      b.n++;
    });
    // Always one green and one red: the second bar runs opposite to the first
    if (bars.length === 2) {
      var a = bars[0], z = bars[1], up = a.c >= a.o, d = Math.max(Math.abs(z.c - z.o), .06);
      z.c = Math.max(-1, Math.min(1, z.o + (up ? -d : d)));
    }
    bars.forEach(function (b) { b.h = Math.max(b.h, b.c); b.l = Math.min(b.l, b.c); draw(b); });
  }
  bars.forEach(function (b) { newBar(b); b.n = Math.floor(Math.random() * 8); });
  tick();
  setInterval(tick, 550);
})();

// Rise-in order and the Strategy Lab table entrance (visual review, Nov 18).
// Panels that appear together rise one after another; table rows rise in,
// their bars fill and the net figure counts up once, when first seen.
(function () {
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.reveal').forEach(function (el) {
    var i = 0, p = el.previousElementSibling;
    while (p && i < 5) { if (p.classList.contains('reveal')) i++; p = p.previousElementSibling; }
    if (i) el.style.setProperty('--ri', i);
  });
  var wrap = document.querySelector('.pk-wrap');
  if (!wrap) return;
  wrap.addEventListener('pointermove', function (e) {
    var row = e.target.closest && e.target.closest('.pk'); if (!row) return;
    var r = row.getBoundingClientRect();
    row.style.setProperty('--mx', (e.clientX - r.left) + 'px'); row.style.setProperty('--my', (e.clientY - r.top) + 'px');
  });
  if (still || !('IntersectionObserver' in window)) return;
  function play() {
    wrap.querySelectorAll('.pk').forEach(function (row, i) {
      row.style.setProperty('--i', i);
      var el = row.querySelector('summary .pk-net'); if (!el) return;
      var txt = el.textContent, m = txt.match(/^([^0-9]*)([0-9][0-9,]*)(.*)$/); if (!m) return;
      var end = +m[2].replace(/,/g, ''), t0 = null, delay = i * 55 + 150;
      el.style.minWidth = el.offsetWidth + 'px'; el.style.textAlign = 'right';
      function step(t) {
        if (t0 === null) t0 = t;
        var k = Math.min(1, Math.max(0, (t - t0 - delay) / 900));
        el.textContent = k < 1 ? m[1] + Math.round(end * (1 - Math.pow(1 - k, 3))).toLocaleString('en-US') + m[3] : txt;
        if (k < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
    wrap.classList.add('play');
  }
  var io = new IntersectionObserver(function (es) {
    if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); play(); }
  }, { rootMargin: '0px 0px -10% 0px' });
  io.observe(wrap);
})();
