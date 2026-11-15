/* Badr Edge results tracker: renders equity, drawdown and day stats from derived daily results. */
(() => {
  const tag = document.getElementById('trk-data');
  if (!tag) return;
  const D = JSON.parse(tag.textContent), FZ = D.freeze;
  const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let gid = 0;

  function combine(ss) {
    const m = new Map();
    ss.forEach(s => s.days.forEach(([d, p, n, w, gw, gl]) => {
      const a = m.get(d) || [0, 0, 0, 0, 0];
      a[0] += p; a[1] += n; a[2] += w; a[3] += gw; a[4] += gl; m.set(d, a);
    }));
    return [...m.keys()].sort().map(d => [d, ...m.get(d)]);
  }
  function stats(days) {
    let eq = 0, pk = 0, mdd = 0, g = 0, r = 0, cg = 0, cr = 0, mg = 0, mr = 0, n = 0, w = 0, gw = 0, gl = 0;
    days.forEach(([, p, tn, tw, a, b]) => {
      eq += p; pk = Math.max(pk, eq); mdd = Math.min(mdd, eq - pk);
      n += tn; w += tw; gw += a; gl += b;
      if (p > 0) { g++; cg++; cr = 0; } else { r++; cr++; cg = 0; }
      mg = Math.max(mg, cg); mr = Math.max(mr, cr);
    });
    return { net: eq, dd: -mdd, pf: gl ? gw / gl : null, wr: n ? 100 * w / n : 0, tr: n, g, r, mg, mr };
  }
  const usd = v => (v < 0 ? '−' : '+') + '$' + Math.abs(Math.round(v)).toLocaleString('en-US');
  const fmt = {
    net: usd, dd: v => '$' + Math.round(v).toLocaleString('en-US'), pf: v => v == null ? '—' : v.toFixed(2),
    wr: v => v.toFixed(1) + '%', tr: v => v.toLocaleString('en-US'), g: v => '' + v, r: v => '' + v,
    mg: v => v + (v === 1 ? ' day' : ' days'), mr: v => v + (v === 1 ? ' day' : ' days'),
  };

  function chart(days, w = 900, h = 250) {
    const id = 'gEq' + (gid++);
    const eq = [0]; days.forEach(d => eq.push(eq[eq.length - 1] + d[1]));
    let pk = -1e18; const dd = eq.map(v => (pk = Math.max(pk, v), v - pk));
    const N = eq.length - 1 || 1, hi = Math.max(...eq), lo = Math.min(0, ...eq), mdd = Math.min(...dd) || -1;
    const top = 8, eqH = h * .72 - 14, ddTop = top + eqH + 10, ddh = h * .28 - 14;
    const X = i => i / N * w, Y = v => top + (hi - v) / (hi - lo || 1) * eqH, YD = v => ddTop + v / mdd * ddh;
    let nIn = days.findIndex(d => d[0] >= FZ); if (nIn < 0) nIn = days.length;
    const path = (a, o) => a.map((v, i) => `${i ? 'L' : 'M'}${X(i + o).toFixed(1)},${Y(v).toFixed(1)}`).join('');
    const inEq = eq.slice(0, nIn + 1), outEq = eq.slice(nIn);
    let s = `<svg class="ch" viewBox="0 0 ${w} ${h + 16}" preserveAspectRatio="none" role="img"><defs><linearGradient id="${id}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="var(--accent)" stop-opacity=".24"/><stop offset="1" stop-color="var(--accent)" stop-opacity="0"/></linearGradient></defs>`;
    if (outEq.length > 1) s += `<rect class="fwz" x="${X(nIn)}" y="1" width="${w - X(nIn)}" height="${h - 2}" rx="6"/>`;
    s += `<path fill="url(#${id})" d="${path(inEq, 0)}L${X(nIn)},${Y(lo)}L0,${Y(lo)}Z"/><path class="eq" d="${path(inEq, 0)}"/>`;
    if (outEq.length > 1) s += `<path class="fw" d="${path(outEq, nIn)}"/>`;
    s += `<line class="base" x1="0" x2="${w}" y1="${ddTop}" y2="${ddTop}"/>`;
    s += `<path class="dd" d="M0,${ddTop}${dd.map((v, i) => `L${X(i).toFixed(1)},${YD(v).toFixed(1)}`).join('')}L${w},${ddTop}Z"/>`;
    const f = outEq.length > 1 ? ' f' : '', tx = X(N), ty = Y(eq[N]);
    s += `<circle class="tipring${f}" cx="${tx}" cy="${ty}" r="4"/><circle class="tip${f}" cx="${tx}" cy="${ty}" r="3.5"/>`;
    let lastM = '';
    days.forEach((d, i) => { const m = d[0].slice(0, 7); if (m !== lastM) { lastM = m; const x = X(i + 1), mi = +d[0].slice(5, 7); if (x < w - 30 && (w >= 600 || mi % 2)) s += `<text x="${x}" y="${h + 13}">${MON[+d[0].slice(5, 7) - 1]}</text>`; } });
    return s + '</svg>';
  }

  function countUp(el, v, f) {
    if (reduce || typeof v !== 'number') { el.textContent = f(v); return; }
    const t0 = performance.now(), T = 1000, dec = f === fmt.pf || f === fmt.wr;
    const step = t => { const k = Math.max(0, Math.min(1, (t - t0) / T)), e = 1 - Math.pow(1 - k, 3); el.textContent = f(dec ? v * e : Math.round(v * e)); if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
    setTimeout(() => { el.textContent = f(v); }, T + 150);
  }
  function setRow(row, st, animate) {
    row.querySelectorAll('[data-s]').forEach(dd => {
      const k = dd.dataset.s, v = st[k], box = dd.parentElement;
      box.querySelectorAll('.meter,.pips,.split').forEach(x => x.remove());
      dd.className = ''; box.className = '';
      if (k === 'net') { dd.classList.add('big'); box.classList.add('t-gold'); }
      if (k === 'wr') { dd.classList.add('up'); box.classList.add('t-up'); box.insertAdjacentHTML('beforeend', `<div class="meter"><b data-w="${v}"></b></div>`); }
      if (k === 'pf' && v != null) box.insertAdjacentHTML('beforeend', `<div class="meter gold"><b data-w="${Math.min(100, v / 5 * 100)}"></b></div>`);
      if (k === 'g') { dd.classList.add('up'); box.classList.add('t-up'); box.insertAdjacentHTML('beforeend', `<div class="split"><span style="flex:${st.g};background:var(--t-up)"></span><span style="flex:${st.r};background:var(--t-dn)"></span></div>`); }
      if (k === 'r') { dd.classList.add('dn'); box.classList.add('t-dn'); }
      if (k === 'mg' || k === 'mr') { dd.classList.add(k === 'mg' ? 'up' : 'dn'); box.insertAdjacentHTML('beforeend', `<div class="pips${k === 'mr' ? ' dn' : ''}">${'<i></i>'.repeat(Math.min(v, 14))}</div>`); }
      animate ? countUp(dd, v, fmt[k]) : (dd.textContent = fmt[k](v));
    });
    requestAnimationFrame(() => requestAnimationFrame(() => row.querySelectorAll('.meter b').forEach(b => b.style.width = b.dataset.w + '%')));
  }

  document.querySelectorAll('.trk').forEach(sec => {
    const fam = sec.dataset.family;
    const pool = D.strategies.filter(s => !fam || s.slug === fam);
    const keyOf = s => fam ? s.name : s.mkt;
    const keys = [...new Set(pool.map(keyOf))];
    const chips = sec.querySelector('.chips');
    let seen = false;
    function render(k, animate) {
      const sel = k === '*' ? pool : pool.filter(s => keyOf(s) === k);
      const days = combine(sel), ins = days.filter(d => d[0] < FZ), out = days.filter(d => d[0] >= FZ);
      const box = sec.querySelector('.trk-chart'), cw = Math.max(300, box.clientWidth || 900);
      box.innerHTML = chart(days, cw, cw < 600 ? Math.round(cw * .62) : 250);
      sec.querySelector('.trk-sel').textContent = sel.length === 1 ? sel[0].name : (k === '*' ? `${sel.length} strategies combined` : `${k} · ${sel.length} strategies`);
      setRow(sec.querySelector('.isk'), stats(ins), animate);
      const hasOut = out.length > 0;
      sec.querySelector('.fwk').hidden = sec.querySelector('.sec-t.f').hidden = !hasOut;
      if (hasOut) setRow(sec.querySelector('.fwk'), stats(out), animate);
    }
    if (chips) {
      chips.innerHTML = ['*', ...keys].map(k => `<button type="button" class="chip${k === '*' ? ' on' : ''}" data-k="${k.replace(/"/g, '&quot;')}" aria-pressed="${k === '*'}"></button>`).join('');
      chips.querySelectorAll('.chip').forEach(c => {
        const k = c.dataset.k;
        c.textContent = k === '*' ? `All ${pool.length}` : k;
        c.onclick = () => { chips.querySelectorAll('.chip').forEach(x => { x.classList.toggle('on', x === c); x.setAttribute('aria-pressed', x === c); }); render(k, true); };
      });
    }
    render('*', false);
    if ('IntersectionObserver' in window && !reduce) {
      const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting && !seen) { seen = true; io.disconnect(); render(sec.querySelector('.chip.on')?.dataset.k || '*', true); } }), { rootMargin: '0px 0px -10% 0px' });
      io.observe(sec);
    }
  });
})();
