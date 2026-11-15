#!/usr/bin/env python3
"""Builds the static pages of badredge.com.

Run:  python3 _src/build.py
It writes the HTML files at their published paths. The tools under /tools/<name>/ are
standalone pages and are not touched, except /tools/index.html, which is built here.
"""
import os, re, random, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import research
import tracker
import guide_viz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://badredge.com"
YEAR = datetime.date.today().year
UPDATED = "November 2026"  # legal pages only; not shown on the homepage or footer

# The Badr Edge logo: the full moon (badr), drawn in CSS (.moon in assets/site.css).
MARK = '<span class="moon" aria-hidden="true"></span>'
BRAND = f'<a class="brand" href="/" aria-label="Badr Edge home">{MARK}<span class="wm">Badr <span class="word-2">Edge</span></span></a>'

# Payout figure on /about/. Off until the lawyer call clears dollar figures on the site.
SHOW_PAYOUT_FIGURE = False
PAYOUT_FIGURE = "$250,000+"
PAYOUT_PROOF_URL = ""  # link to the payout records page or PDF, once it exists

NAV = [("/research/backtested/", "Strategy Lab"), ("/research/", "Research"), ("/pine/", 'Private Pine Scripts<small class="nav-soon">Opening soon</small>'), ("/about/", "Who is Badr")]

ICONS = {
    "trail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 14l4-4 3 2 4-5 7-3"/><path d="M3 20h5v-3h5v-3h8" stroke-dasharray="2.2 2.6"/></svg>',
    "flag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21V3.5"/><path d="M5 4h13l-2.5 4L18 12H5"/><path d="M9 4v8M13 4v8" stroke-width="1.2" opacity=".6"/></svg>',
    "ladder": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20h18"/><path d="M5 20v-4h4v4M10 20v-8h4v8M15 20V8h4v12"/></svg>',
    "breakout": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="10" height="8" rx="1.5" stroke-dasharray="2.2 2.2"/><path d="M6 17v-4M10 16v-3"/><path d="M12 12l8-8M15 4h5v5"/></svg>',
    "ib": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M3 18h18" stroke-dasharray="2.2 2.6"/><path d="M8 4v16M16 8v10"/><rect x="6" y="8" width="4" height="7" rx="1"/><rect x="14" y="10" width="4" height="5" rx="1"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/></svg>',
    "coins": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 7v5c0 1.7 2.7 3 6 3s6-1.3 6-3V7"/><path d="M9 15v2c0 1.7 2.7 3 6 3s6-1.3 6-3v-5c0-1.7-2.7-3-6-3"/></svg>',
    "scale": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M5 21h14M6 7h12M6 7l-3 7a3 3 0 0 0 6 0L6 7zm12 0l-3 7a3 3 0 0 0 6 0l-3-7z"/></svg>',
    "code": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5z"/><path d="M4 19a2 2 0 0 1 2-2h13"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>',
}

DISCLAIMER_SHORT = ("Badr Edge publishes educational tools and articles only. Nothing on this site is investment advice, "
                    "a recommendation to buy or sell any instrument, or an offer of any financial service. Simulations are "
                    "hypothetical, rely on the inputs you provide and do not predict future results. Trading futures and "
                    "leveraged products involves substantial risk of loss and is not suitable for everyone.")


THEME_INIT = ("<script>(function(){var t;try{t=localStorage.getItem('be-theme')}catch(e){}"
              "if(t!=='light'&&t!=='dark')t=window.matchMedia&&matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';"
              "document.documentElement.setAttribute('data-theme',t)})();</script>")

THEME_BTN = ('<button class="theme-btn" type="button" aria-label="Switch theme" title="Switch theme">'
             '<svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'
             '<svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/></svg></button>')



OG_VERSION = "2"


def og_image(path):
    """Share card per section; the version query makes chat apps fetch the new image."""
    name = "tools" if path.startswith("/tools") else "research" if path.startswith("/research") else "home"
    return f"{SITE}/assets/og-{name}.jpg?v={OG_VERSION}"


def og_tags(title, desc, path):
    img = og_image(path)
    t = "Badr Edge · Day trader toolkit" if path == "/" else title
    return f"""<meta property="og:title" content="{t}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Badr Edge: a gold moon with orbiting tickers and candles">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">"""

def head(title, desc, path, extra=""):
    full = title if title == "Badr Edge" else f"{title} · Badr Edge"
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{THEME_INIT}
<title>{full}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#07080a">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Badr Edge">
<meta property="og:url" content="{SITE}{path}">
{og_tags(full, desc, path)}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400..800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/theme.js" defer></script>
{extra}</head>
<body>
<div class="sky" aria-hidden="true"><i class="sky-stars"></i><i class="sky-stars s2"></i><i class="sky-aurora a1"></i><i class="sky-aurora a2"></i><i class="sky-aurora a3"></i><svg class="sky-orbits" viewBox="0 0 1200 1200" preserveAspectRatio="xMidYMid slice"><g><ellipse cx="600" cy="600" rx="560" ry="170" transform="rotate(-14 600 600)"/><ellipse cx="600" cy="600" rx="430" ry="128" transform="rotate(20 600 600)"/><ellipse cx="600" cy="600" rx="720" ry="230" transform="rotate(4 600 600)"/></g></svg><svg class="sky-chart" viewBox="0 0 800 800"><g><circle cx="400" cy="400" r="380" class="c1"/><circle cx="400" cy="400" r="372" class="tk"/><circle cx="400" cy="400" r="300" class="c2"/><circle cx="400" cy="400" r="210" class="c2"/><line x1="400" y1="10" x2="400" y2="790"/><line x1="10" y1="400" x2="790" y2="400"/></g></svg></div>
"""

# Nav icon: only Strategy Lab has one (fine-line flask; the teal bubbling liquid is the "live" signal).
ICON_LAB = ('<svg class="nav-ico ico-lab" viewBox="0 0 24 24" aria-hidden="true">'
            '<path class="liq" d="M6.6 14.5h10.8l1.8 3.1a2 2 0 0 1-1.7 3H6.5a2 2 0 0 1-1.7-3z"/>'
            '<circle class="bub b1" cx="10.2" cy="17.4" r="1"/><circle class="bub b2" cx="13.6" cy="18" r=".8"/><circle class="bub b3" cx="12" cy="17" r=".65"/>'
            '<path class="gl" d="M9 3h6M10 3v5.5L4.8 17.6a2 2 0 0 0 1.7 3h11a2 2 0 0 0 1.7-3L14 8.5V3"/></svg>')


def header(active):
    links = "".join(
        f'<a href="{href}"{" class=\"nav-hl\"" if href == NAV[0][0] else ""}{" aria-current=\"page\"" if href == active else ""}>'
        f'{ICON_LAB if href == NAV[0][0] else ""}{label}</a>' for href, label in NAV)
    cta = '<a class="cta" href="/tools/"><i class="hl-dot"></i>Open the tools</a>'  # only Strategy Lab keeps an icon
    first = links.index("</a>") + 4  # menu order: Strategy Lab, Open the tools, then the rest
    links = links[:first] + cta + links[first:]
    return f"""<header class="site-head">
  <div class="wrap">
    {BRAND}
    <nav class="nav" id="nav" aria-label="Main">{links}</nav>
    <div class="head-actions">{THEME_BTN}<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button></div>
  </div>
</header>
<main>
"""


def footer():
    return f"""</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        {BRAND}
        <p class="foot-about">An independent futures research desk. Free tools, guides and a public research record.</p>
        <a class="foot-mail" href="mailto:hello@badredge.com">hello@badredge.com</a>
      </div>
      <div><h4>Tools</h4><ul>
        <li><a href="/tools/pass/">Prop Pass Simulator</a></li>
        <li><a href="/tools/payout/">Payout Simulator</a></li>
        <li><a href="/tools/sizing/">Contract Sizing</a></li>
        <li><a href="/tools/">All tools</a></li>
      </ul></div>
      <div><h4>Learn</h4><ul>
        <li><a href="/guides/trailing-drawdown/">Trailing drawdown</a></li>
        <li><a href="/guides/prop-evaluation-math/">Evaluation math</a></li>
        <li><a href="/guides/contract-sizing/">Contract sizing</a></li>
        <li><a href="/guides/opening-range-breakout/">Opening range breakout</a></li>
        <li><a href="/guides/initial-balance/">Initial balance</a></li>
        <li><a href="/guides/">All guides</a></li>
      </ul></div>
      <div><h4>Badr Edge</h4><ul>
        <li><a href="/about/">Who is Badr</a></li>
        <li><a href="/research/backtested/">Strategy Lab</a></li>
        <li><a href="/research/">Research</a></li>
        <li><a href="/pine/">Private Pine Scripts</a></li>
        <li><a href="/legal/disclaimer/">Disclaimer</a></li>
        <li><a href="/legal/privacy/">Privacy</a></li>
      </ul></div>
    </div>
    <div class="foot-legal">
      <p><strong>Educational only.</strong> {DISCLAIMER_SHORT}</p>
      <p>Prop firm names are used only to describe rule styles. Badr Edge is not affiliated with or endorsed by any firm, broker or exchange.</p>
    </div>
    <div class="foot-bar">
      <div>&copy; {YEAR} Badr Edge<span class="sep"></span>All rights reserved<span class="sep"></span><a href="/legal/disclaimer/">Disclaimer</a><span class="sep"></span><a href="/legal/privacy/">Privacy</a></div>
    </div>
  </div>
</footer>
<script>
(() => {{
  const b = document.querySelector('.menu-btn'), n = document.getElementById('nav');
  if (b) b.addEventListener('click', () => {{ const o = n.classList.toggle('open'); b.setAttribute('aria-expanded', o); b.textContent = o ? 'Close' : 'Menu'; }});
  const els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {{
    const io = new IntersectionObserver(es => es.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }}), {{ rootMargin: '0px 0px -8% 0px' }});
    els.forEach(el => io.observe(el));
  }} else els.forEach(el => el.classList.add('in'));
}})();
</script>
</body>
</html>
"""


def page(path, title, desc, active, body, extra=""):
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.strip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(head(title, desc, path, extra) + header(active) + body + footer())
    return path


# ───────────────────────── Hero illustration ─────────────────────────
def hero_svg():
    """An illustrative account path with a trailing end-of-day floor that locks at the start balance."""
    rnd = random.Random(11)
    start, mll, days = 0.0, 2000.0, 34
    bal, peak, floor = start, start, start - mll
    pts_b, pts_f = [(0, bal)], [(0, floor)]
    moves = [180, -120, 260, 90, -210, 310, -90, 150, 240, -330, 120, 200, -60, 280, -150, 90, 330, -240,
             160, 210, -110, 70, 260, -190, 140, 220, -80, 300, -270, 120, 190, 80, -130, 240]
    for d in range(1, days + 1):
        bal += moves[d - 1]
        peak = max(peak, bal)
        floor = min(peak - mll, start)
        pts_b.append((d, bal))
        pts_f.append((d, floor))
    W, H, L, R, T, B = 520, 280, 46, 12, 14, 26
    lo, hi = -2300, max(b for _, b in pts_b) + 400
    x = lambda d: L + d / days * (W - L - R)
    y = lambda v: T + (hi - v) / (hi - lo) * (H - T - B)
    path = lambda pts: " ".join(("M" if i == 0 else "L") + f"{x(d):.1f},{y(v):.1f}" for i, (d, v) in enumerate(pts))
    area = path(pts_b) + f" L{x(days):.1f},{y(lo):.1f} L{x(0):.1f},{y(lo):.1f} Z"
    grid = ""
    for v, lab in [(0, "start"), (-2000, "−$2,000"), (2000, "+$2,000"), (4000, "+$4,000")]:
        if lo <= v <= hi:
            grid += f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="rgba(255,255,255,.08)" stroke-dasharray="{"0" if v == 0 else "3 4"}"/>'
            grid += f'<text x="{L-6}" y="{y(v)+4:.1f}" text-anchor="end" fill="#5e636c" font-size="10" font-family="JetBrains Mono,ui-monospace,Menlo,monospace">{lab}</text>'
    return f"""<svg viewBox="0 0 {W} {H}" role="img" aria-label="Illustration: an account balance rising while its trailing loss floor follows it up and then locks at the starting balance">
  <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9b46c" stop-opacity=".28"/><stop offset="1" stop-color="#d9b46c" stop-opacity="0"/></linearGradient></defs>
  {grid}
  <path d="{area}" fill="url(#g)"/>
  <path d="{path(pts_f)}" fill="none" stroke="#e07a6c" stroke-width="2" stroke-linejoin="round"/>
  <path d="{path(pts_b)}" fill="none" stroke="#d9b46c" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="{x(days):.1f}" cy="{y(pts_b[-1][1]):.1f}" r="4" fill="#f3deb0"/>
</svg>"""


# ───────────────────────── Hero chart ─────────────────────────
def desk_chart():
    """Illustrative 5-minute session: an opening range, a false break lower, the breakout and a retest.
    Deterministic, drawn with CSS classes so it follows the light/dark theme."""
    rnd = random.Random(7)
    # target closes for each bar: range, sweep below, breakout, retest of range high, continuation
    path = ([101.6, 102.8, 101.2, 103.4, 102.1, 103.0] + [101.0, 99.9, 100.6, 102.4, 103.6, 104.9, 106.2, 105.4,
            107.1, 108.3, 107.0, 105.6, 104.7, 105.3, 106.6, 108.0, 109.2, 108.6, 110.1, 111.4, 110.7, 112.0,
            112.9, 112.2, 113.6, 114.1, 113.2, 114.6])
    bars, prev = [], 102.2
    for c in path:
        c += rnd.uniform(-.25, .25)
        o = prev + rnd.uniform(-.3, .3)
        hi = max(o, c) + rnd.uniform(.2, .9)
        lo = min(o, c) - rnd.uniform(.2, .9)
        bars.append((o, hi, lo, c)); prev = c
    n = len(bars)
    W, H, L, R, T, B = 560, 236, 4, 58, 10, 18
    lo_p, hi_p = 98.0, 116.0
    bw = (W - L - R) / n
    x = lambda i: L + (i + .5) * bw
    y = lambda v: T + (hi_p - v) / (hi_p - lo_p) * (H - T - B)
    out = []
    last = bars[-1][3]
    for v in range(98, 117, 3):
        if abs(y(v) - y(last)) < 13: 
            out.append(f'<line class="ch-grid" x1="{L}" x2="{W-R+6}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>'); continue
        out.append(f'<line class="ch-grid" x1="{L}" x2="{W-R+6}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>'
                   f'<text class="ch-axis" x="{W-R+12}" y="{y(v)+3:.1f}">{2380+v*1.0:.1f}</text>')
    for i in range(0, n, 6):
        out.append(f'<line class="ch-grid" x1="{x(i):.1f}" x2="{x(i):.1f}" y1="{T}" y2="{H-B}"/>')
    t0 = 9 * 60 + 30
    for i in range(0, n, 6):
        m = t0 + i * 5
        out.append(f'<text class="ch-axis" x="{x(i):.1f}" y="{H-4}" text-anchor="middle">{m//60:02d}:{m%60:02d}</text>')
    orh = max(b[1] for b in bars[:6]); orl = min(b[2] for b in bars[:6])
    out.append(f'<rect class="ch-or" x="{L}" y="{y(orh):.1f}" width="{x(5)+bw/2-L:.1f}" height="{y(orl)-y(orh):.1f}"/>')
    for v, lab in [(orh, "OR HIGH"), (orl, "OR LOW")]:
        out.append(f'<line class="ch-orl" x1="{L}" x2="{W-R+6}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>'
                   f'<text class="ch-orlab" x="{W-R-2}" text-anchor="end" y="{y(v)-5 if lab == "OR HIGH" else y(v)+12:.1f}">{lab}</text>')
    # session average line
    acc, vw = 0, []
    for i, (o, h, l, c) in enumerate(bars):
        acc += (h + l + c) / 3; vw.append((i, acc / (i + 1)))
    out.append('<path class="ch-vw" d="' + " ".join(("M" if i == 0 else "L") + f"{x(i):.1f},{y(v):.1f}" for i, v in vw) + '"/>')
    for i, (o, h, l, c) in enumerate(bars):
        up = c >= o
        k = "up" if up else "dn"
        top, bot = y(max(o, c)), y(min(o, c))
        out.append(f'<line class="ch-wick-{k}" x1="{x(i):.1f}" x2="{x(i):.1f}" y1="{y(h):.1f}" y2="{y(l):.1f}"/>'
                   f'<rect class="ch-{k}" x="{x(i)-bw*.32:.1f}" y="{top:.1f}" width="{bw*.64:.1f}" height="{max(bot-top, 1):.1f}"/>')
    last = bars[-1][3]
    out.append(f'<line class="ch-lastl" x1="{x(n-1):.1f}" x2="{W-R+6}" y1="{y(last):.1f}" y2="{y(last):.1f}"/>'
               f'<rect class="ch-last" x="{W-R+6}" y="{y(last)-8:.1f}" width="{R-4}" height="16" rx="2"/>'
               f'<text class="ch-lastt" x="{W-R+12}" y="{y(last)+3.5:.1f}">{2380+last:.1f}</text>')
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Illustration: a five-minute futures chart with an opening range, '
            f'a false break below it, a breakout above and a retest">' + "".join(out) + "</svg>")


# ───────────────────────── Pages ─────────────────────────
TOOLS = [
    ("/tools/pass/", "target", "Prop Pass Simulator",
     "Thousands of simulated evaluation attempts with your numbers and a firm's rules: trailing max loss, daily limit, best-day consistency and minimum days.",
     ["Pass and fail odds by contract size", "Median days to pass", "Why attempts fail", "TradingView CSV import"]),
    ("/tools/payout/", "coins", "Payout Simulator",
     "Models the funded account after you pass: winning-day rules, buffers, splits and caps, so you know how long a first payout takes.",
     ["Odds of reaching a first payout", "Days to payout and to the cap", "Compare firm-style rule sets", "Portfolio of strategies"]),
    ("/tools/sizing/", "scale", "Contract Sizing",
     "Finds the contract size that keeps a trailing max loss safe, scales it as your buffer grows, and stress-tests the ladder eight ways.",
     ["Size for today's buffer", "Short-term forecast fan", "Stress and out-of-sample tests", "CSV and Excel import"]),
]

GUIDES = [
    ("/guides/trailing-drawdown/", "Trailing drawdown, explained with numbers",
     "End-of-day, intraday and static drawdown, when the floor locks, and the mistakes that end accounts.", "8 min read"),
    ("/guides/prop-evaluation-math/", "The math of passing a prop evaluation",
     "Why the target-to-max-loss ratio, your loss per trade and your give-up date decide the outcome more than win rate.", "9 min read"),
    ("/guides/contract-sizing/", "Sizing contracts against a trailing max loss",
     "Micros vs minis, dollars per point, and a simple buffer ladder that grows size only when the account can afford it.", "8 min read"),
    ("/guides/opening-range-breakout/", "Opening range breakout (ORB), for beginners",
     "What the opening range is, what counts as a breakout, where the risk sits and why many breakouts fail.", "6 min read"),
    ("/guides/initial-balance/", "The initial balance (IB), for beginners",
     "The first hour's high and low, range extensions, and how traders use the IB as a map for the rest of the day.", "6 min read"),
]


def tool_cards():
    out = []
    for href, icon, name, desc, bullets in TOOLS:
        lis = "".join(f"<li>{b}</li>" for b in bullets)
        out.append(f"""<a class="card reveal" href="{href}">
        <div class="icon">{ICONS[icon]}</div>
        <span class="tagline">Free</span>
        <h3>{name}</h3>
        <p>{desc}</p>
        <ul>{lis}</ul>
        <span class="go">Open tool &rarr;</span>
      </a>""")
    return "\n      ".join(out)


GUIDE_ICONS = {"/guides/trailing-drawdown/": "trail", "/guides/prop-evaluation-math/": "flag", "/guides/contract-sizing/": "ladder",
               "/guides/opening-range-breakout/": "breakout", "/guides/initial-balance/": "ib"}


def guide_cards():
    return "\n      ".join(f"""<a class="card reveal" href="{h}">
        <div class="icon">{ICONS[GUIDE_ICONS.get(h, 'book')]}</div>
        <h3>{t}</h3>
        <p>{d}</p>
        <span class="go">{m} &rarr;</span>
      </a>""" for h, t, d, m in GUIDES)


SESSIONS = [  # key, name, IANA zone, open, close (local exchange time, Mon-Fri). Forex week: Sun 17:00 to Fri 17:00 New York.
    ("sydney", "Sydney", "Australia/Sydney", "07:00", "16:00"),
    ("tokyo", "Tokyo", "Asia/Tokyo", "09:00", "18:00"),
    ("london", "London", "Europe/London", "08:00", "17:00"),
    ("ny", "New York", "America/New_York", "08:00", "17:00"),
]


def market_board():
    import json
    cal = json.load(open(os.path.join(os.path.dirname(__file__), "calendar.json")))
    ses = "".join(
        f'<div class="fx-row" data-k="{k}" data-tz="{tz}" data-o="{o}" data-c="{c}">'
        f'<div class="fx-id"><b>{n}</b><span class="fx-clock">--:--</span><span class="fx-st"><i></i><em>&nbsp;</em></span></div>'
        f'<div class="fx-track"></div></div>'
        for k, n, tz, o, c in SESSIONS)
    ticks = "".join(f'<span style="left:{h / 24 * 100:.4f}%"{" class=minor" if h % 6 else ""}>{h:02d}</span>' for h in range(0, 25, 3))
    ev = "".join(
        f'<div class="ev-row" data-t="{t}" hidden><span class="ev-when"><b class="ev-day"></b><small class="ev-time"></small></span>'
        f'<span class="ev-name"><b>{title}</b><small>USD · {per}</small></span>'
        f'<span class="ev-src">{src}</span>'
        f'<span class="ev-imp" aria-label="High impact"><i></i><i></i><i></i></span></div>'
        for t, title, per, src in cal["events"])
    return f'''    <div class="term board reveal">
      <div class="term-bar"><div class="mb-tabs" role="tablist"><button role="tab" aria-selected="true" data-tab="mk">Sessions</button><button role="tab" aria-selected="false" data-tab="ev">High impact</button></div><span class="term-tag ss-tz">Your time</span></div>
      <div class="mb-pane" data-pane="mk"><div class="fx-head"><div class="fx-now-time"><b class="fx-clock-main">--:--</b><span class="fx-date">&nbsp;</span></div><div class="fx-status"><i></i><span>&nbsp;</span></div></div><div class="fx-body"><div class="fx-axis"><span class="fx-axis-l">Sessions</span><div class="fx-ticks">{ticks}</div></div>{ses}<div class="fx-row fx-flow-row"><div class="fx-id"><b>Overlap</b><span class="fx-clock">Sessions open</span></div><svg class="fx-flow" viewBox="0 0 960 40" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="fxg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".45"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient></defs><path class="fx-area" d=""/><path class="fx-line" d=""/></svg></div><div class="fx-plot" aria-hidden="true"><i class="fx-now"><em>--:--</em></i></div></div><p class="ev-src-note">Forex session hours in your time zone, detected from your browser. The market trades Sunday 17:00 to Friday 17:00 New York. Holidays are not shown.</p></div>
      <div class="mb-pane" data-pane="ev" hidden><div class="ev-next"><span class="dot"></span><span class="ev-next-txt">Next release</span></div>{ev}<p class="ev-src-note">US high-impact releases from the official BLS, BEA, Census and Fed schedules. Shown in your time.</p></div>
    </div>
    <script>(function(){{var b=document.querySelector('.board');if(!b)return;
b.querySelectorAll('[data-tab]').forEach(function(t){{t.onclick=function(){{b.querySelectorAll('[data-tab]').forEach(function(x){{x.setAttribute('aria-selected',x===t)}});b.querySelectorAll('[data-pane]').forEach(function(p){{p.hidden=p.dataset.pane!==t.dataset.tab}})}}}});
function off(tz,d){{var p={{}};new Intl.DateTimeFormat('en-US',{{timeZone:tz,hourCycle:'h23',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit'}}).formatToParts(d).forEach(function(x){{p[x.type]=+x.value}});return Date.UTC(p.year,p.month-1,p.day,p.hour%24,p.minute,p.second)-Math.floor(d/1000)*1000}}
function zt(tz,y,m,d,hm){{var g=Date.UTC(y,m,d,+hm.slice(0,2),+hm.slice(3));return g-off(tz,new Date(g-off(tz,new Date(g))))}}
function ymd(tz,d){{var p={{}};new Intl.DateTimeFormat('en-US',{{timeZone:tz,year:'numeric',month:'2-digit',day:'2-digit',weekday:'short'}}).formatToParts(d).forEach(function(x){{p[x.type]=x.value}});return [+p.year,+p.month-1,+p.day,p.weekday]}}
function spans(r,from){{var tz=r.dataset.tz,out=[];for(var i=-2;i<9;i++){{var t=ymd(tz,new Date(from+i*864e5));if(t[3]==='Sat'||t[3]==='Sun')continue;var x=[zt(tz,t[0],t[1],t[2],r.dataset.o),zt(tz,t[0],t[1],t[2],r.dataset.c)];if(!out.some(function(y){{return y[0]===x[0]}}))out.push(x)}}return out.sort(function(a,b){{return a[0]-b[0]}})}}
function wk(t){{var d=ymd('America/New_York',new Date(t)),w=d[3],h=+new Intl.DateTimeFormat('en-US',{{timeZone:'America/New_York',hourCycle:'h23',hour:'2-digit'}}).format(new Date(t));return w==='Sat'||(w==='Fri'&&h>=17)||(w==='Sun'&&h<17)}}
function wkEnd(t){{for(var i=0;i<4;i++){{var d=ymd('America/New_York',new Date(t+i*864e5));if(d[3]==='Sun')return zt('America/New_York',d[0],d[1],d[2],'17:00')}}return t}}
function hm(t,tz){{var o={{hour:'2-digit',minute:'2-digit',hourCycle:'h23'}};if(tz)o.timeZone=tz;return new Date(t).toLocaleTimeString([],o)}}
function dur(ms){{var m=Math.max(0,Math.round(ms/6e4)),d=Math.floor(m/1440),h=Math.floor(m%1440/60);return (d?d+'d ':'')+(h?h+'h ':'')+(d?'':(m%60)+'m')}}
var rws=[].slice.call(b.querySelectorAll('.fx-row[data-k]'));
function tick(){{var n=Date.now(),d0=new Date();d0.setHours(0,0,0,0);d0=+d0;var d1=new Date(d0);d1.setDate(d1.getDate()+1);d1=+d1;var L=d1-d0,we=wk(n),open=[],all=[];
b.querySelector('.fx-clock-main').textContent=hm(n);b.querySelector('.fx-date').textContent=new Date(n).toLocaleDateString(undefined,{{weekday:'long',day:'numeric',month:'long'}});
rws.forEach(function(r){{var sp=spans(r,n).map(function(x){{return wk(x[0])?[wkEnd(x[0]),x[1]]:x}}).filter(function(x){{return x[1]>x[0]}}),cur=null,nx=null;all.push(sp);
sp.forEach(function(x){{if(x[0]<=n&&n<x[1])cur=x;else if(x[0]>n&&!nx)nx=x}});if(cur)open.push(r.querySelector('b').textContent);
r.classList.toggle('open',!!cur);r.querySelector('.fx-clock').textContent=hm(n,r.dataset.tz)+' local';
r.querySelector('.fx-st em').textContent=cur?'Open · '+dur(cur[1]-n)+' left':(nx?'Opens in '+dur(nx[0]-n):'Closed');
var tr=r.querySelector('.fx-track');tr.innerHTML='';sp.forEach(function(x){{var a=Math.max(x[0],d0),z=Math.min(x[1],d1);if(z<=a)return;var i=document.createElement('i');i.style.left=((a-d0)/L*100)+'%';i.style.width=((z-a)/L*100)+'%';if(x===cur)i.className='on';if((z-a)/L>.12){{var e=document.createElement('em');e.textContent=hm(x[0])+' – '+hm(x[1]);i.appendChild(e)}}tr.appendChild(i)}})}});
var pts=[],N=96;for(var k=0;k<=N;k++){{var t=d0+L*k/N,c=0;all.forEach(function(sp){{sp.forEach(function(x){{if(x[0]<=t&&t<x[1])c++}})}});pts.push(c)}}
var sm=pts.map(function(v,k){{var s=0,w=0;for(var j=-2;j<=2;j++){{var q=pts[k+j];if(q!==undefined){{var f=3-Math.abs(j);s+=q*f;w+=f}}}}return s/w}});
var line=sm.map(function(v,k){{return (k?'L':'M')+(k/N*960).toFixed(1)+' '+(38-v/3*34).toFixed(1)}}).join('');
b.querySelector('.fx-line').setAttribute('d',line);b.querySelector('.fx-area').setAttribute('d',line+'L960 40L0 40Z');
var st=b.querySelector('.fx-status');st.classList.toggle('live',open.length>0);
st.querySelector('span').textContent=we?'Forex weekend · opens in '+dur(wkEnd(n)-n):open.length>1?open.join(' + ')+' overlap':open.length?open[0]+' session open':'Between sessions';
var nw=b.querySelector('.fx-now'),px=(n-d0)/L;nw.style.left=(px*100)+'%';nw.className='fx-now'+(px<.06?' lo':px>.94?' hi':'');nw.querySelector('em').textContent=hm(n)}}
try{{var tzn=Intl.DateTimeFormat().resolvedOptions().timeZone;b.querySelector('.ss-tz').textContent=tzn.split('/').pop().replace(/_/g,' ')+' time'}}catch(e){{}}
tick();setInterval(tick,30000);
var now=Date.now(),rows=[].slice.call(b.querySelectorAll('.ev-row')),past=null,shown=0,next=null;
rows.forEach(function(r){{var d=new Date(r.dataset.t);
r.querySelector('.ev-day').textContent=d.toLocaleDateString(undefined,{{weekday:'short',day:'numeric',month:'short'}});
r.querySelector('.ev-time').textContent=d.toLocaleTimeString([], {{hour:'2-digit',minute:'2-digit'}});
if(d<now){{past=r;return}}if(shown<6){{r.hidden=false;shown++;if(!next){{next=d;r.classList.add('next')}}}}}});
if(past){{past.hidden=false;past.classList.add('past')}}
if(next){{var m=Math.round((next-now)/60000),dd=Math.floor(m/1440),h=Math.floor(m%1440/60);b.querySelector('.ev-next-txt').textContent='Next release in '+(dd?dd+'d ':'')+(h?h+'h ':'')+(dd?'':(m%60)+'m')}}
}})();</script>
'''



def door_art(kind):
    """Small illustrations for the three toolkit cards on the homepage."""
    W, H = 320, 104
    grid = ''.join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in (26, 52, 78))
    grid = f'<g class="da-grid">{grid}</g>'
    pts = lambda P: ' '.join(f'{x:.1f},{y:.1f}' for x, y in P)
    if kind == 'tools':
        # Monte Carlo fan: many attempts from one start, a target above, the max loss below
        rnd = random.Random(7)
        top, floor, x0, y0 = 18, 88, 14, 58
        paths = []
        for i in range(9):
            y, P = y0, [(x0, y0)]
            drift = (-0.55, 0.5, -0.25, 0.1, -0.4, 0.35, -0.15, 0.2, -0.7)[i]
            for x in range(x0 + 12, W - 10, 12):
                y = min(max(y + drift + rnd.uniform(-5.5, 5.5), top - 4), floor + 2)
                P.append((x, y))
                if y <= top or y >= floor: break
            paths.append(P)
        win = [(x0, y0)]; y = y0
        for k, x in enumerate(range(x0 + 12, 238, 12)):
            y = max(y - 2.3 + (4.5 if k % 3 == 1 else -1.2), top); win.append((x, y))
        win.append((238, top))
        lose = [(x0, y0)]; y = y0
        for k, x in enumerate(range(x0 + 12, 170, 12)):
            y = min(y + 2.2 + (-4 if k % 3 == 2 else 1), floor); lose.append((x, y))
        lose.append((170, floor))
        body = (f'<line class="da-target" x1="{x0}" y1="{top}" x2="{W - 8}" y2="{top}"/>'
                f'<line class="da-floor" x1="{x0}" y1="{floor}" x2="{W - 8}" y2="{floor}"/>'
                + ''.join(f'<polyline class="da-faint" points="{pts(P)}"/>' for P in paths)
                + f'<polyline class="da-down" points="{pts(lose)}"/><circle class="da-dot-down" cx="170" cy="{floor}" r="2.6"/>'
                + f'<polyline class="da-gold" points="{pts(win)}"/><circle class="da-dot-gold" cx="238" cy="{top}" r="3"/>'
                + f'<circle class="da-start" cx="{x0}" cy="{y0}" r="2.6"/>'
                + f'<text class="da-lbl live" x="{x0}" y="{top - 6}">target</text>'
                + f'<text class="da-lbl down" x="{x0}" y="{floor + 12}">max loss</text>')
    elif kind == 'research':
        # Equity curve: in-sample in gold, then a dashed split and the forward test in teal
        rnd = random.Random(3)
        split, y, P = 214, 84, []
        for x in range(12, split + 1, 6):
            y = y - 1.55 + rnd.uniform(-3.4, 3.4); P.append((x, y))
        F = [P[-1]]; y = P[-1][1]
        for x in range(split + 6, W - 8, 6):
            y = y - 0.55 + rnd.uniform(-3.6, 3.6); F.append((x, y))
        area = pts(P) + f' {split},{H - 6} 12,{H - 6}'
        body = (f'<polygon class="da-area" points="{area}"/>'
                f'<line class="da-split" x1="{split}" y1="6" x2="{split}" y2="{H - 6}"/>'
                f'<polyline class="da-gold" points="{pts(P)}"/>'
                f'<polyline class="da-live" points="{pts(F)}"/>'
                f'<circle class="da-dot-gold" cx="{split}" cy="{P[-1][1]:.1f}" r="3"/>'
                f'<text class="da-lbl" x="18" y="16">in-sample</text>'
                f'<text class="da-lbl live" x="{split + 8}" y="16">forward</text>')
    else:
        # Pine Script: a strategy on the chart, with entry, stop and target levels
        # Pullback, a tight base, then a breakout that the strategy enters
        oc = [(40, 48), (48, 44), (44, 56), (56, 64), (64, 60), (60, 70), (70, 66), (66, 72),
              (72, 64), (64, 70), (70, 58), (58, 50), (50, 40), (40, 34)]
        cs, x = [], 26
        for k, (o, c) in enumerate(oc):
            hi = min(o, c) - (3 + (k * 7) % 4); lo = max(o, c) + (3 + (k * 5) % 4)
            cs.append((x, o, c, hi, lo)); x += 21
        cs[10] = (cs[10][0], 70, 58, 55, 72)
        entry_x, entry_y = cs[10][0], 62
        bars = ''.join(
            f'<g class="{"da-up" if c < o else "da-dn"}"><line x1="{x}" y1="{hi:.1f}" x2="{x}" y2="{lo:.1f}"/>'
            f'<rect x="{x - 5}" y="{min(o, c):.1f}" width="10" height="{max(abs(c - o), 1.5):.1f}" rx="1.5"/></g>'
            for x, o, c, hi, lo in cs)
        body = (f'<line class="da-target" x1="{entry_x}" y1="{entry_y - 36:.1f}" x2="{W - 8}" y2="{entry_y - 36:.1f}"/>'
                f'<line class="da-entry" x1="{entry_x}" y1="{entry_y:.1f}" x2="{W - 8}" y2="{entry_y:.1f}"/>'
                f'<line class="da-floor" x1="{entry_x}" y1="{entry_y + 18:.1f}" x2="{W - 8}" y2="{entry_y + 18:.1f}"/>'
                + bars
                + f'<path class="da-mark" d="M{entry_x - 5},{entry_y + 30:.1f} l5,-7 l5,7z"/>'
                + f'<text class="da-lbl code" x="12" y="16">//@version=6</text>')
    return (f'<div class="door-art" aria-hidden="true"><svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet">'
            f'{grid}{body}</svg></div>')


def test_art(kind):
    """Illustrations of the tests behind the research. Shapes only, not results."""
    W, H = 320, 104
    grid = '<g class="da-grid">' + ''.join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in (26, 52, 78)) + '</g>'
    pts = lambda P: ' '.join(f'{x:.1f},{y:.1f}' for x, y in P)
    xs = list(range(14, W - 12, 8))
    if kind == 'mc':
        # Many reshuffled trade orders: faint paths, a 5-95% band and the median
        rnd = random.Random(21)
        paths = []
        for _ in range(40):
            y, P = 84.0, []
            for x in xs:
                P.append((x, y)); y += -1.15 + rnd.gauss(0, 3.4)
            paths.append(P)
        q = lambda col, f: sorted(col)[int(f * (len(col) - 1))]
        cols = [[P[i][1] for P in paths] for i in range(len(xs))]
        lo = [(xs[i], q(c, .95)) for i, c in enumerate(cols)]
        hi = [(xs[i], q(c, .05)) for i, c in enumerate(cols)]
        med = [(xs[i], q(c, .5)) for i, c in enumerate(cols)]
        band = pts(hi) + ' ' + pts(lo[::-1])
        body = (f'<polygon class="da-band" points="{band}"/>'
                + ''.join(f'<polyline class="da-faint thin" points="{pts(P)}"/>' for P in paths[:14])
                + f'<polyline class="da-gold" points="{pts(med)}"/>'
                + f'<text class="da-lbl" x="14" y="16">5–95% range</text>'
                + f'<text class="da-lbl gold" x="{W - 12}" y="{med[-1][1] - 8:.1f}" text-anchor="end">median</text>')
    elif kind == 'null':
        # Random-direction null: the real pick must sit beyond 95% of random picks
        import math
        n, x0, bw = 22, 18, 10
        bars = ''
        for i in range(n):
            h = 66 * math.exp(-((i - 8.5) ** 2) / 22) + 3
            bars += f'<rect class="da-hist" x="{x0 + i * bw:.1f}" y="{92 - h:.1f}" width="{bw - 2}" height="{h:.1f}" rx="1.5"/>'
        p95 = x0 + 14.5 * bw
        real = W - 34
        body = (bars
                + f'<line class="da-split" x1="{p95}" y1="14" x2="{p95}" y2="96"/>'
                + f'<text class="da-lbl" x="{p95 - 6}" y="16" text-anchor="end">95%</text>'
                + f'<line class="da-real" x1="{real}" y1="30" x2="{real}" y2="92"/><circle class="da-dot-gold" cx="{real}" cy="30" r="3.4"/>'
                + f'<text class="da-lbl gold" x="{real}" y="18" text-anchor="middle">real pick</text>'
                + f'<text class="da-lbl" x="{x0}" y="16">random picks</text>')
    elif kind == 'stress':
        # Same trades at 1x, 2x and 3x slippage
        rnd = random.Random(5)
        noise = [rnd.gauss(0, 2.2) for _ in xs]
        curves = []
        for slope in (-1.75, -0.85, 0.05):
            y, P = 82.0, []
            for i, x in enumerate(xs):
                P.append((x, y)); y += slope + noise[i]
            curves.append(P)
        body = (f'<polyline class="da-down" points="{pts(curves[2])}"/>'
                f'<polyline class="da-muted" points="{pts(curves[1])}"/>'
                f'<polyline class="da-gold" points="{pts(curves[0])}"/>'
                + ''.join(f'<text class="da-lbl {c}" x="{W - 4}" y="{P[-1][1] + 3:.1f}" text-anchor="end">{t}</text>'
                          for P, t, c in zip(curves, ('1x', '2x', '3x'), ('gold', '', 'down')))
                + f'<text class="da-lbl" x="14" y="16">slippage</text>')
    else:
        # Frozen rules, run once on four unseen years, after a year of exploring
        hs = (34, 22, 46, 28, 58)
        bars, bw, x0 = '', 44, 26
        for i, h in enumerate(hs):
            cls = 'da-yr-live' if i < 4 else 'da-yr-gold'
            bars += f'<rect class="{cls}" x="{x0 + i * (bw + 12)}" y="{88 - h}" width="{bw}" height="{h}" rx="3"/>'
        split = x0 + 4 * (bw + 12) - 6
        body = (f'<line class="da-split" x1="{split}" y1="8" x2="{split}" y2="96"/>' + bars
                + f'<line class="da-base" x1="14" y1="88" x2="{W - 10}" y2="88"/>'
                + f'<text class="da-lbl live" x="{x0}" y="16">unseen years · run once</text>'
                + f'<text class="da-lbl gold" x="{split + 8}" y="16">explore</text>')
    return (f'<div class="door-art" aria-hidden="true"><svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet">'
            f'{grid}{body}</svg></div>')


def research_art(kind):
    """Small illustrations for the three Research cards. Shapes only, not results."""
    W, H = 320, 104
    grid = '<g class="da-grid">' + ''.join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in (26, 52, 78)) + '</g>'
    pts = lambda P: ' '.join(f'{x:.1f},{y:.1f}' for x, y in P)
    if kind == 'method':
        # The pipeline: explore, cheap checks, freeze, frozen test, gate
        steps = ('explore', 'checks', 'freeze', 'test', 'gate')
        xs = [34 + i * 63 for i in range(5)]
        body = f'<line class="da-rail" x1="{xs[0]}" y1="52" x2="{xs[-1]}" y2="52"/>'
        body += f'<line class="da-rail-on" x1="{xs[0]}" y1="52" x2="{xs[2]}" y2="52"/>'
        for i, (x, t) in enumerate(zip(xs, steps)):
            cls = 'da-node on' if i <= 2 else 'da-node'
            body += f'<circle class="{cls}" cx="{x}" cy="52" r="{7 if i == 2 else 5}"/>'
            body += f'<text class="da-lbl{" gold" if i == 2 else ""}" x="{x}" y="80" text-anchor="middle">{t}</text>'
            body += f'<text class="da-lbl" x="{x}" y="30" text-anchor="middle">0{i + 1}</text>'
        body += f'<path class="da-lock" d="M{xs[2] - 2.5},51 v-2 a2.5,2.5 0 0 1 5,0 v2 M{xs[2] - 3.5},51 h7 v4 h-7 z"/>'
    elif kind == 'backtested':
        # Several strategy families on one chart, each after costs
        rnd = random.Random(17)
        lines = []
        for k in range(6):
            y, P = 66 + rnd.uniform(-14, 14), []
            slope = rnd.uniform(-.45, .55) if k else .6
            for x in range(14, W - 10, 8):
                P.append((x, y)); y = min(max(y - slope + rnd.gauss(0, 2.4), 22), 96)
            lines.append(P)
        body = ''.join(f'<polyline class="da-faint" points="{pts(P)}"/>' for P in lines[1:])
        body += f'<polyline class="da-gold" points="{pts(lines[0])}"/>'
        body += '<text class="da-lbl" x="14" y="16">strategy families · after costs</text>'
    else:
        # Forward test: settings frozen, then new data only
        rnd = random.Random(29)
        start, y, P = 92, 70, []
        for x in range(start, W - 14, 7):
            P.append((x, y)); y = y - .35 + rnd.gauss(0, 2.6)
        body = (f'<line class="da-split" x1="{start}" y1="10" x2="{start}" y2="96"/>'
                f'<rect class="da-shade" x="14" y="10" width="{start - 14}" height="86" rx="3"/>'
                f'<text class="da-lbl" x="22" y="56">frozen</text>'
                f'<polyline class="da-live" points="{pts(P)}"/>'
                f'<circle class="da-pulse" cx="{P[-1][0]:.1f}" cy="{P[-1][1]:.1f}" r="3.2"/>'
                f'<text class="da-lbl live" x="{start + 8}" y="16">new data · no changes</text>')
    return (f'<div class="door-art" aria-hidden="true"><svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet">'
            f'{grid}{body}</svg></div>')

def home():
    body = f"""
<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="eyebrow">Independent futures research desk</span>
      <h1>Patience is <span class="gold">a position.</span></h1>
      <p class="lede">A day trader toolkit: free tools to plan risk before the open, and an open record of how trading ideas get tested after costs. Built by a working futures trader.</p>
      <div class="hero-actions">
        <a class="btn primary" href="/tools/">Explore the tools</a>
        <a class="btn" href="/research/">See the research</a>
      </div>
      <dl class="hero-meta"><div><dt>Access</dt><dd>Free, no sign-up</dd></div><div><dt>Built by</dt><dd>Moves freight by day, trades the open</dd></div><div><dt>Signals</dt><dd>Never offered</dd></div></dl>
    </div>
    <div class="hero-visual">
    <div class="moon-stage" aria-hidden="true">
      <svg class="orbit-lines back" viewBox="0 0 540 540"><g mask="url(#orb-back)"><ellipse cx="270" cy="270" rx="258" ry="80" transform="rotate(-12 270 270)"/><ellipse cx="270" cy="270" rx="206" ry="62" transform="rotate(18 270 270)"/></g><defs><mask id="orb-back"><rect width="540" height="270" fill="#fff"/></mask></defs></svg>
      <img class="big-moon" src="/assets/moon.webp" alt="" width="1024" height="1024" decoding="async" fetchpriority="high">
      <svg class="orbit-lines front" viewBox="0 0 540 540"><g mask="url(#orb-front)"><ellipse cx="270" cy="270" rx="258" ry="80" transform="rotate(-12 270 270)"/><ellipse cx="270" cy="270" rx="206" ry="62" transform="rotate(18 270 270)"/></g><defs><mask id="orb-front"><rect y="270" width="540" height="270" fill="#fff"/></mask></defs></svg>
      <span class="rider r1 cdl up" style="--d:0"></span>
      <span class="rider r1 tk" style="--d:-33.3"><b>GC</b></span>
      <span class="rider r1 tk" style="--d:-66.6"><b>NQ</b></span>
      <span class="rider r2 cdl dn" style="--d:-16"></span>
      <span class="rider r2 tk" style="--d:-50"><b>ES</b></span>
      <span class="rider r2 tk" style="--d:-83"><b>YM</b></span>
    </div>
{market_board()}
    </div>
    </div>
  </div>
</section>

<div class="specbar"><div class="wrap"><dl>
  <div><dt>Markets</dt><dd>Indices <span>·</span> Metals</dd></div>
  <div><dt>Sessions</dt><dd>Asia · London · New York</dd></div>
  <div><dt>Research</dt><dd>{len(research.FAMILIES)} families <span>·</span> forward testing</dd></div>
  <div><dt>Tools</dt><dd>3 simulators <span>·</span> in-browser</dd></div>
</dl></div></div>
{tracker.two_ways()}
<section class="band" id="desk">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Day trader toolkit</span>
      <h2>Built for the <span class="gold">trading day.</span></h2>
      <p class="lede">Tools to plan risk before the open, research to check an idea after costs, and private Pine Scripts for TradingView. Free, and it runs in your browser.</p>
    </div>
    <div class="grid-3 doors">
      <a class="card reveal" href="/tools/">
        {door_art('tools')}<span class="tagline">Live</span>
        <h3>Tools</h3>
        <p>Free simulators for risk, position size and account planning. Put in your own numbers or a TradingView trade list and see the range of outcomes.</p>
        <span class="go">Explore the tools &rarr;</span>
      </a>
      <a class="card reveal" href="/research/">
        {door_art('research')}<span class="tagline">Live</span>
        <h3>Research</h3>
        <p>A public log of how trading ideas are built, frozen and stress-tested, with last year's results after costs.</p>
        <span class="go">Open the research &rarr;</span>
      </a>
      <a class="card reveal" href="/pine/">
        {door_art('pine')}<span class="tagline">Soon</span>
        <h3>Private Pine Scripts</h3>
        <p>Invite-only TradingView strategies in Pine Script v6. Opening soon.</p>
        <span class="go">Join the waitlist &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section class="band never-band">
  <div class="wrap">
    <div class="never reveal">
      <span class="eyebrow">Never offered</span>
      <ul>
        <li><b>Signals</b><span>No trade calls or alerts.</span></li>
        <li><b>Promised returns</b><span>No win-rate or profit claims.</span></li>
        <li><b>Uploads</b><span>Tools run in your browser.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Research</span><h2>Research, tested <span class="gold">in the open.</span></h2>
      <p class="lede">A public log of a futures research desk: the method, every strategy family tested and last year's results after costs. All of it is research and requires forward testing.</p></div>
    <div class="grid-3">
      <a class="card reveal" href="/research/method/">{research_art('method')}<h3>Method</h3><p>Explore, freeze, validate. Random-direction nulls, unseen years and real costs.</p><span class="go">Read the method</span></a>
      <a class="card reveal" href="/research/backtested/">{research_art('backtested')}<h3>Strategy Lab</h3><p>Opening ranges, Initial Balance and more, with last year's results after costs.</p><span class="go">See the backtests</span></a>
      <a class="card reveal" href="/research/under-observation/">{research_art('forward')}<h3>In forward testing</h3><p>Noise-area momentum on MNQ, logged on new data with no changes.</p><span class="go">Read the note</span></a>
    </div>
    <h3 class="tests-title">How every idea gets tested <span class="tests-tag">Illustrations, not results</span></h3>
    <div class="grid-4 tests">
      <div class="card test reveal">{test_art('mc')}<h3>Monte Carlo</h3><p>Thousands of reshuffled trade orders show the range of drawdowns, not only the path you got.</p></div>
      <div class="card test reveal">{test_art('null')}<h3>Random-direction null</h3><p>The search is rerun with random trade directions. The real pick has to beat 95% of them.</p></div>
      <div class="card test reveal">{test_art('stress')}<h3>Cost stress</h3><p>Slippage doubled and tripled, fees raised 50%. The idea has to hold up at higher costs.</p></div>
      <div class="card test reveal">{test_art('years')}<h3>Unseen years</h3><p>Rules are frozen, then run once on four earlier years they were never tuned on.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">FAQ</span><h2>Questions traders ask</h2></div>
    <div class="faq">
      <details><summary>What is Badr Edge?</summary><p>The public side of a working futures trader's desk: the tools, guides and testing habits used to plan and review trading, shared for free. It isn't a signal service, a course or a fund.</p></details>
      <details><summary>Is it free?</summary><p>Yes. The tools and guides need no account, no paywall and no trial.</p></details>
      <details><summary>Is my data uploaded anywhere?</summary><p>No. The tools run in your browser. Files you load are read on your device, and settings are saved only in your own browser's storage.</p></details>
      <details><summary>Do you sell signals or courses?</summary><p>No. There are no signals, alerts or courses here. Private Pine Scripts are <a href="/pine/">opening soon</a>.</p></details>
      <details><summary>Is any of this financial advice?</summary><p>No. Everything here is educational. Simulations are hypothetical and rely on the inputs you give them. Your trading decisions are your own.</p></details>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <span class="eyebrow">Start here</span>
    <h2>Start where <span class="gold">you are.</span></h2>
    <p class="lede">Have numbers to test? Open a tool. Want the reasoning first? Start with the research.</p>
    <div class="hero-actions" style="justify-content:center"><a class="btn primary" href="/tools/">Explore the tools</a><a class="btn" href="/research/">See the research</a></div>
  </div>
</section>
"""
    return page("/", "Badr Edge",
                "Free risk tools to plan the trading day, and an open record of how trading ideas get tested after costs. Built by a working futures trader.",
                "/", body)


def tools_index():
    body = f"""
<section class="page-head"><div class="wrap">
  <span class="eyebrow">Free tools</span>
  <h1>Prop-firm simulators</h1>
  <p class="lede">Three Monte Carlo tools for planning evaluations, payouts and position size under trailing drawdown rules. Free, no sign-up, and everything runs in your browser.</p>
</div></section>
<section style="padding-top:24px"><div class="wrap">
  <div class="grid-3">
    {tool_cards()}
  </div>
  <div class="callout" style="margin-top:32px;max-width:820px"><p><strong>Tip:</strong> export your strategy's "List of trades" from the TradingView Strategy Tester and load the CSV. Real trades with real dates keep losing streaks and bad weeks intact, which is where most accounts fail.</p></div>
</div></section>
"""
    return page("/tools/", "Free tools", "Free Monte Carlo simulators for prop futures traders: pass odds, payout timing and contract sizing.", "/tools/", body)


def guides_index():
    body = f"""
<section class="page-head"><div class="wrap">
  <span class="eyebrow">Guides</span>
  <h1>Learn the rules that decide the account</h1>
  <p class="lede">Worked examples with diagrams. Each guide ends with a tool to test the idea on your own numbers.</p>
</div></section>
<section style="padding-top:24px"><div class="wrap"><div class="grid-3">
  {guide_cards()}
</div></div></section>
"""
    return page("/guides/", "Guides", "Beginner guides for futures traders: trailing drawdown, prop evaluation math, contract sizing, opening range breakouts and the initial balance.", "/guides/", body)


def article(path, title, desc, minutes, body_html, tool_href, tool_name, cta=None):
    body_html = re.sub(r"<!--V:(\w+)-->", lambda m: getattr(guide_viz, m.group(1))(), body_html)
    cta = cta or f'The <a href="{tool_href}">{tool_name}</a> runs this on your own win rate, averages or TradingView trade list.'
    body = f"""
<header class="article-head"><div class="wrap">
  <a class="eyebrow" href="/guides/" style="text-decoration:none">&larr; Guides</a>
  <h1>{title}</h1>
  <p class="lede">{desc}</p>
  <p class="meta">{minutes}</p>
</div></header>
<article class="prose">
{body_html}
<div class="callout"><p><strong>Test it on your numbers.</strong> {cta}</p></div>
<p class="note">Educational content only, not investment advice. Rules differ by firm and change often, so always check your firm's current rules. Examples use round numbers for clarity.</p>
</article>
"""
    return page(path, title, desc, "/guides/", body)


ARTICLE_DD = """
<p>The profit target gets all the attention, but the <strong>maximum loss limit</strong> is the rule that ends most prop accounts. On most futures evaluations it doesn't sit still. It <em>trails</em> your balance upward. Knowing when it moves is the difference between a pullback and a closed account.</p>

<h2>The three types</h2>
<h3>1. Static</h3>
<p>The floor is fixed at your starting balance minus the max loss. On a $50,000 account with a $2,000 limit, the floor is $48,000 forever. Profit you make widens your cushion permanently. This is the most forgiving type and the least common on futures evaluations.</p>

<h3>2. Trailing, end of day</h3>
<p>At the end of each session, the firm looks at your closing balance. If it's a new high, the floor moves up to that high minus the max loss. Intraday swings don't move it. Only the close does.</p>
<table>
  <thead><tr><th>Day</th><th>Closing balance</th><th>Highest close</th><th>Floor</th><th>Cushion</th></tr></thead>
  <tbody>
    <tr><td>Start</td><td>$50,000</td><td>$50,000</td><td>$48,000</td><td>$2,000</td></tr>
    <tr><td>1</td><td>$50,600</td><td>$50,600</td><td>$48,600</td><td>$2,000</td></tr>
    <tr><td>2</td><td>$50,200</td><td>$50,600</td><td>$48,600</td><td>$1,600</td></tr>
    <tr><td>3</td><td>$51,300</td><td>$51,300</td><td>$49,300</td><td>$2,000</td></tr>
    <tr><td>4</td><td>$52,100</td><td>$52,100</td><td>$50,000</td><td>$2,100</td></tr>
  </tbody>
</table>
<p>Notice that on day 2 the cushion shrank to $1,600 even though the account is still up $200. <strong>Your cushion is measured from your best close, not from where you started.</strong></p>
<!--V:dd_trailing-->

<h3>3. Trailing, intraday</h3>
<p>The floor follows your highest balance at any moment, including open profit. If a trade runs +$800 and comes back to breakeven, the floor already moved up $800 and stays there. This is the strictest type: letting winners breathe can shrink your cushion even on trades you don't lose.</p>
<!--V:dd_intraday-->

<h2>When the floor stops: the lock</h2>
<p>Most trailing rules stop trailing once the floor reaches a set level, usually the starting balance (sometimes start plus a small amount). In the table above, the floor hit $50,000 on day 4 and <strong>locks there</strong>. From that point on, every dollar of profit above the max loss is real cushion, and the account behaves like a static one.</p>
<div class="callout"><p>Before the lock, you're playing defense against your own high-water mark. After it, you're playing with a buffer. Most blown accounts die <strong>before</strong> the lock.</p></div>

<h2>Four mistakes that end accounts</h2>
<ol>
  <li><strong>Measuring risk from the starting balance.</strong> After a good run, your real cushion is smaller than the headline max loss. Size from the cushion, not the account size.</li>
  <li><strong>Adding size after a winning day.</strong> A new high raises the floor at the same moment you raise risk. The next normal losing day now costs more cushion.</li>
  <li><strong>Holding open profit on an intraday-trailing account.</strong> Open profit that you give back still moved the floor.</li>
  <li><strong>Ignoring the daily loss limit.</strong> Some firms stop you for the day. Others fail the account. Know which one you're trading.</li>
</ol>

<h2>A quick self-check</h2>
<ul>
  <li>What is my floor <em>right now</em>, in dollars?</li>
  <li>How many average losing trades fit between my balance and that floor?</li>
  <li>Does my drawdown trail at the close or intraday, and where does it lock?</li>
</ul>
<p>If you can't answer all three in ten seconds, you're trading blind on the one rule that matters most.</p>
"""

ARTICLE_MATH = """
<p>Most traders ask "what's my win rate?" when they plan an evaluation. A more useful question is: <strong>how many average losses can I take before the max loss, and how many average wins do I need to reach the target?</strong> Those two numbers decide most outcomes.</p>

<h2>Start with the ratio</h2>
<p>A typical evaluation might ask for a <strong>$3,000 target with a $2,000 max loss</strong>. That's a 1.5 : 1 race: you need to make one and a half times what you're allowed to lose, and the loss limit usually trails behind you.</p>
<p>If your edge were a coin flip with equal wins and losses, a race to +3 before −2 would succeed only about 40% of the time. You need a real edge to reach even odds.</p>

<h2>Translate dollars into trades</h2>
<p>Suppose your strategy wins 50% of the time, with an average win of $180 and an average loss of $120 per contract after costs.</p>
<table>
  <thead><tr><th>Contracts</th><th>Avg loss</th><th>Losses to max loss</th><th>Avg win</th><th>Wins to target</th></tr></thead>
  <tbody>
    <tr><td>1</td><td>$120</td><td>16.7</td><td>$180</td><td>16.7</td></tr>
    <tr><td>3</td><td>$360</td><td>5.6</td><td>$540</td><td>5.6</td></tr>
    <tr><td>6</td><td>$720</td><td>2.8</td><td>$1,080</td><td>2.8</td></tr>
  </tbody>
</table>
<p>At 1 contract the account almost never fails, but it also needs about 17 net winning trades, which can take months. At 6 contracts, three losses in a row (common for any 50% strategy) is enough to end the attempt.</p>
<!--V:math_race-->

<h2>Two ways to fail</h2>
<ul>
  <li><strong>Too big:</strong> a normal losing streak hits the floor before the edge has time to show.</li>
  <li><strong>Too small:</strong> the attempt runs out of time or patience. You reset, pay again, or start forcing trades.</li>
</ul>
<p>The best size is usually in the middle, and it's narrower than people expect. That is exactly what a Monte Carlo simulation finds: it replays thousands of attempts at each size and counts how many pass, fail or stall.</p>
<!--V:math_sweet_spot-->

<h2>Losing streaks are normal, not bad luck</h2>
<p>A strategy that wins 50% of the time will produce a run of <strong>six or more losses in a row</strong> fairly often over a few hundred trades. If six average losses fit inside your cushion, you survive it. If they don't, the streak is the end of the attempt, not a rough patch.</p>
<div class="callout"><p>Rule of thumb: size so that your <strong>worst realistic losing streak</strong> costs no more than about half of your cushion. The other half absorbs slippage, a bad day and the trailing floor moving up.</p></div>

<h2>The hidden rules</h2>
<p>Consistency rules (no single day can be more than a set percentage of total profit) and minimum trading days both stretch the attempt. A big winning day can delay a pass, because you need more profit on other days to dilute it. Model these rules, don't hope around them.</p>

<h2>What to do with this</h2>
<ol>
  <li>Use your <strong>after-cost</strong> averages, not gross.</li>
  <li>Find the size where the pass rate peaks, then consider one size smaller for safety.</li>
  <li>Decide in advance how many sessions you'll give the attempt.</li>
  <li>Stress the plan: what happens if winners are 10% smaller than your backtest?</li>
</ol>
"""

ARTICLE_SIZE = """
<p>Choosing between a micro and a mini contract isn't a style preference. It's a risk decision. The same 5-point move on gold is $50 on a micro and $500 on a full contract. Under a $2,000 trailing max loss, that difference is the whole game.</p>
<!--V:size_same_move-->

<h2>Dollars per point</h2>
<table>
  <thead><tr><th>Contract</th><th>Market</th><th>$ per point</th><th>Tick</th><th>$ per tick</th></tr></thead>
  <tbody>
    <tr><td>MGC</td><td>Micro Gold</td><td>$10</td><td>0.10</td><td>$1.00</td></tr>
    <tr><td>GC</td><td>Gold</td><td>$100</td><td>0.10</td><td>$10.00</td></tr>
    <tr><td>MES</td><td>Micro S&amp;P 500</td><td>$5</td><td>0.25</td><td>$1.25</td></tr>
    <tr><td>ES</td><td>E-mini S&amp;P 500</td><td>$50</td><td>0.25</td><td>$12.50</td></tr>
    <tr><td>MNQ</td><td>Micro Nasdaq-100</td><td>$2</td><td>0.25</td><td>$0.50</td></tr>
    <tr><td>NQ</td><td>E-mini Nasdaq-100</td><td>$20</td><td>0.25</td><td>$5.00</td></tr>
    <tr><td>MYM</td><td>Micro Dow</td><td>$0.50</td><td>1</td><td>$0.50</td></tr>
    <tr><td>YM</td><td>E-mini Dow</td><td>$5</td><td>1</td><td>$5.00</td></tr>
  </tbody>
</table>
<p>Contract specs are set by the exchange and can change. Check your broker's specs before trading.</p>

<h2>Size from the stop, not the account</h2>
<p>Work backwards from the dollar loss you can accept on one trade:</p>
<p><strong>Contracts = (risk per trade in $) ÷ (stop in points × $ per point)</strong></p>
<p>Example: you accept $150 of risk on a gold trade with a 6-point stop. On MGC that's 6 × $10 = $60 per contract, so 2 contracts ($120). On GC, one contract would risk $600, four times your limit. On a small account, micros are often the only way to size correctly.</p>

<h2>The buffer ladder</h2>
<p>Under a trailing max loss, the right size changes as your <strong>buffer</strong> (balance minus floor) changes. A simple ladder:</p>
<ol>
  <li>Pick a block size, for example $700 of buffer per contract.</li>
  <li>Each morning, contracts = buffer ÷ block, rounded down, with a minimum of 1.</li>
  <li>When the buffer grows, size grows. After a drawdown, size shrinks automatically.</li>
</ol>
<table>
  <thead><tr><th>Buffer</th><th>Block $700</th><th>Block $500</th></tr></thead>
  <tbody>
    <tr><td>$1,200</td><td>1</td><td>2</td></tr>
    <tr><td>$2,000</td><td>2</td><td>4</td></tr>
    <tr><td>$3,500</td><td>5</td><td>7</td></tr>
  </tbody>
</table>
<!--V:size_ladder-->
<p>The ladder does what discipline often doesn't: it cuts size after losses and only adds it when the account has earned the room.</p>
<div class="callout"><p>The block size is the key number. Too small and a normal losing streak breaches the floor. Too large and the account grows slowly. The Contract Sizing tool searches for the smallest block that keeps your breach chance under a limit you choose.</p></div>

<h2>Don't forget costs</h2>
<p>Commission and slippage are charged per contract, so they scale with size. One tick of slippage on MNQ is $0.50, but over hundreds of trades and several contracts it adds up. Always test your size with costs included.</p>
"""

ARTICLE_ORB = """
<p>The first minutes after a market opens are often the busiest of the session. An <strong>opening range breakout</strong>, or ORB, uses that burst of activity as a map: mark where price traded early, then watch what happens when it leaves that area.</p>

<h2>The opening range</h2>
<p>The opening range is simply the <strong>highest and lowest price of the first few minutes</strong> after a session opens. Common choices are the first 5, 15 or 30 minutes. For US index futures, many traders use the New York stock market open at 9:30 ET.</p>
<p>Once that time is up, the two levels are fixed for the day. Everything after is measured against them.</p>
<!--V:orb_breakout-->

<h2>What counts as a breakout</h2>
<p>A breakout is price moving <strong>outside</strong> the range. Traders define it in one of two ways, and the choice matters:</p>
<ul>
  <li><strong>Touch:</strong> price trades one tick beyond the high or low. Earlier, but it catches more false moves.</li>
  <li><strong>Close:</strong> a candle closes beyond the level. Slower, but it filters some quick spikes.</li>
</ul>
<p>A break above the high is read as buyers in control for now. A break below the low is the mirror image.</p>

<h2>Where the risk sits</h2>
<p>The range also gives a natural place for a stop. Two common references are <strong>the other side of the range</strong> or <strong>its midpoint</strong>.</p>
<p>That makes the range height your risk per contract. In the chart, the range is 40 points. On Micro Nasdaq (MNQ, $2 a point) a stop at the other side costs $80 per contract before costs. On the full contract (NQ, $20 a point) the same stop costs $800. A wide opening range means a wide stop, so size goes down, not up.</p>

<h2>Most of the work is in the false breaks</h2>
<!--V:orb_false-->
<p>Price often pokes out of the range and comes straight back. No rule removes this. What separates one ORB plan from another is how it handles these moments: where the stop sits, whether it trades a second break, and when it stops for the day.</p>

<h2>Decide these before you test</h2>
<ol>
  <li><strong>Market and session.</strong> Gold, Nasdaq and the Dow behave differently, and so do the Asia, London and New York opens.</li>
  <li><strong>Range length.</strong> 5, 15 or 30 minutes.</li>
  <li><strong>Entry trigger.</strong> Touch or close, and which side or both.</li>
  <li><strong>Stop.</strong> Other side, midpoint or a fixed number of points.</li>
  <li><strong>Exit.</strong> A target, a trailing stop or a time of day.</li>
  <li><strong>Cut-off.</strong> The latest time a new trade is allowed.</li>
</ol>
<div class="callout"><p>ORB is a framework, not an edge. Whether any version works depends on the market, the exact rules and costs, and it changes over time. Write the rules down, test them after costs, and forward test before risking money. The desk's own ORB research is in <a href="/research/#families">Research</a>.</p></div>
"""

ARTICLE_IB = """
<p>The <strong>initial balance</strong>, or IB, is the price range of the <strong>first hour</strong> of the main trading session. It comes from market-profile trading and is one of the simplest ways to get a map of the day.</p>

<h2>How to mark it</h2>
<ol>
  <li>Pick the session. For US index futures this is usually 9:30 to 10:30 ET.</li>
  <li>When the hour ends, mark the <strong>IB high</strong> and <strong>IB low</strong>.</li>
  <li>The distance between them is the <strong>IB range</strong>.</li>
</ol>
<!--V:ib_chart-->

<h2>Range extension</h2>
<p>When price trades beyond the IB high or low after the first hour, that is a <strong>range extension</strong>. Some traders also draw lines at <strong>1× or 2× the IB range</strong> beyond the high and low, as reference points for how far the day has stretched. They are reference points, not targets.</p>

<h2>Narrow and wide IBs</h2>
<p>Traders compare today's IB with recent days:</p>
<ul>
  <li><strong>Narrow IB:</strong> the first hour was quiet. Many traders watch these days for an extension later, because little of a normal day's range has been used.</li>
  <li><strong>Wide IB:</strong> the first hour already moved a lot. The stop for a breakout is wider, and a lot of the day's usual range may be spent.</li>
</ul>
<p>Neither one tells you direction. They only describe how much room the day has used.</p>

<h2>Three ways a day can treat the IB</h2>
<!--V:ib_day_types-->
<p>Some days never leave the IB. Some extend in one direction and keep going. Others break one side, fail and run to the other. Seeing these three shapes makes it easier to read a chart without forcing a trade.</p>

<h2>IB and ORB, side by side</h2>
<table>
  <thead><tr><th></th><th>Opening range (ORB)</th><th>Initial balance (IB)</th></tr></thead>
  <tbody>
    <tr><td>Window</td><td>First 5 to 30 min</td><td>First 60 min</td></tr>
    <tr><td>Range size</td><td>Smaller</td><td>Larger</td></tr>
    <tr><td>Stop to the other side</td><td>Tighter</td><td>Wider</td></tr>
    <tr><td>Trades per day</td><td>Earlier, more often</td><td>Later, fewer</td></tr>
  </tbody>
</table>
<p>Both mark early levels and watch for price to leave them. The IB simply waits longer, so its levels hold more of the session's early trading.</p>
<div class="callout"><p>The IB is a way to read the day, not a signal. Any rule built on it needs to be written down, tested after costs and forward tested. The desk's IB research is in <a href="/research/families/initial-balance/">Research</a>.</p></div>
"""


def pine():
    body = """
<section class="page-head pine-soon"><div class="wrap">
  <span class="eyebrow">Opening soon</span>
  <h1>Private <span class="gold">Pine Scripts.</span></h1>
  <p class="lede">Invite-only TradingView strategies in Pine Script v6. Join the waitlist to hear first when it opens.</p>
  <div class="hero-actions">
    <a class="btn primary" href="mailto:hello@badredge.com?subject=Private%20Pine%20Scripts%20waitlist&amp;body=Please%20add%20me%20to%20the%20waitlist.">Join the waitlist</a>
  </div>
  <p class="note">Opens an email to hello@badredge.com. No signals, no promised results. Not financial advice.</p>
</div></section>
"""
    return page("/pine/", "Private Pine Scripts", "Private, invite-only Pine Script v6 strategies for TradingView. Opening soon: join the waitlist.", "/pine/", body)


def about():
    body = f"""
<section class="page-head"><div class="wrap">
  <span class="eyebrow">Who is Badr</span>
  <h1>Who is <span class="gold">Badr.</span></h1>
  <p class="lede">Badr Edge is the independent research desk of Badr, a futures trader with more than three years of live experience across prop firms and personal brokerage accounts.</p>
</div></section>


<article class="prose" style="max-width:820px;padding-top:56px;padding-bottom:0">
  <h2>Experience</h2>
  <p>The work pairs real-market execution with systematic strategy building, quantitative testing and strict risk control. Most of the trading runs through prop firms: passing evaluations, trading funded accounts under each firm's drawdown rules and moving up to live funded accounts at three firms, with selection for a live-capital trading program. Alongside the prop accounts, Badr trades personal CFD brokerage accounts.</p>
  <p>Execution is a discretionary candlestick price-action process, built over two years and traded mostly in gold and US index futures across the Asia, London and New York sessions.</p>

  <h2>The record</h2>
  <p>No P&amp;L screenshots here. The process has been checked by the people with the most reason to doubt it: the firms that pay out on it.</p>
  <div class="record">
    <div class="record-cell record-hero"><span class="record-k">Documented prop-firm payouts</span><b>$250K+</b><span>Paid out by four firms since 2025, passing $250,000 in November 2026. Firm-issued certificates are on file.</span></div>
    <div class="record-cell"><span class="record-k">Live-funded</span><b>3 firms</b><span>Promoted to live accounts at MyFundedFutures, Lucid and Topstep in 2026, and selected for a live-capital program.</span></div>
    <div class="record-cell"><span class="record-k">Payouts received</span><b>4 firms</b><span>Topstep, Lucid, Take Profit Trader and MyFundedFutures.</span></div>
    <div class="record-cell"><span class="record-k">Evaluations passed</span><b>6 firms</b><span>The four above, plus FundedNext and Tradeify.</span></div>
    <div class="record-cell"><span class="record-k">Verification</span><b>Originals on file</b><span>Firm-issued certificates, with personal and account details removed.</span></div>
  </div>
  <p class="note">Prop-firm payouts are paid under each firm's own rules, often from simulated accounts. They are not investment returns, they are not an offer, and they don't predict anyone's future results.</p>

  <h2>Focus</h2>
</article>
<section style="padding:20px 0 0"><div class="wrap" style="max-width:820px">
  <div class="focus">
    <div><b data-n="01">Futures trading</b><span>Gold and index micros, session by session.</span></div>
    <div><b data-n="02">Strategy research</b><span>Systematic ideas, written as rules before they are tested.</span></div>
    <div><b data-n="03">Quantitative analysis</b><span>Random-direction nulls, unseen years, many-tests corrections.</span></div>
    <div><b data-n="04">Backtesting</b><span>Pine Script v6, checked trade by trade against an independent replica.</span></div>
    <div><b data-n="05">Risk management</b><span>Size to the drawdown the account can survive, not the target.</span></div>
    <div><b data-n="06">Execution</b><span>Costs, slippage and fills treated as part of the strategy.</span></div>
  </div>
</div></section>
<article class="prose" style="max-width:820px;padding-top:32px">
  <h2>Why it exists</h2>
  <p>The prop-firm world is loud: screenshots of wins, promises of fast funding, strategies sold on perfect backtests. Little of it answers the questions that decide whether an account survives. How big is my real cushion today? How many losses in a row can this size take? Does my edge still look like the one I planned with?</p>
  <p>Every tool here started as something built for real accounts. The research is published in the open, and all of it requires forward testing.</p>

  <h2>The name</h2>
  <p>Badr is Arabic for the full moon: the night you can see the whole picture. The edge is the process, not a promise of results.</p>

  <h2>Get in touch</h2>
  <p>Feedback, bug reports and tool ideas: <a href="mailto:hello@badredge.com">hello@badredge.com</a>.</p>
  <p class="note">Past payouts and trading results do not predict future results. Badr Edge does not manage money, offer signals or give investment advice. See the <a href="/legal/disclaimer/">disclaimer</a>.</p>
</article>
"""
    return page("/about/", "Who is Badr", "Who is Badr: the independent futures research desk behind Badr Edge, built on more than three years of live trading and $250K+ in documented prop-firm payouts.", "/about/", body)


def legal_disclaimer():
    body = f"""
<header class="article-head"><div class="wrap"><span class="eyebrow">Legal</span><h1>Disclaimer</h1><p class="meta">Updated {UPDATED}</p></div></header>
<article class="prose">
<h2>Educational purposes only</h2>
<p>All content on badredge.com, including tools, simulations, articles, code examples and any other material, is provided for general educational and informational purposes only. It is not investment, financial, legal or tax advice, and it is not a recommendation or solicitation to buy, sell or hold any security, futures contract, currency or other instrument.</p>
<h2>No offer of financial services</h2>
<p>Badr Edge does not manage money, execute trades, provide signals or offer personalised advice. Nothing on this site should be read as an offer of any regulated financial service in any jurisdiction.</p>
<h2>Hypothetical results</h2>
<p>Simulations and examples are hypothetical. They are based on inputs and assumptions that you or the author provide, and they have inherent limitations. They do not reflect real trading, do not account for every market condition, and cannot predict future results. Hypothetical performance is not indicative of future performance.</p>
<h2>Risk</h2>
<p>Trading futures, options, CFDs and other leveraged products involves substantial risk of loss and is not suitable for every investor. You can lose more than your initial deposit. Only trade with capital you can afford to lose, and consider seeking advice from a licensed professional.</p>
<h2>Third parties</h2>
<p>Names of prop firms, brokers, exchanges and platforms are used only to describe rule styles or compatibility. Badr Edge is not affiliated with, endorsed by or sponsored by any of them. Firm rules change often, and presets may be out of date. Always check the firm's current rules.</p>
<h2>No warranty</h2>
<p>The tools are provided "as is" without warranty of any kind. They may contain errors. You are solely responsible for your trading decisions and for verifying any output before relying on it.</p>
<h2>Contact</h2>
<p><a href="mailto:hello@badredge.com">hello@badredge.com</a></p>
</article>
"""
    return page("/legal/disclaimer/", "Disclaimer", "Badr Edge disclaimer: educational content only, not investment advice; hypothetical simulations.", "", body)


def legal_privacy():
    body = f"""
<header class="article-head"><div class="wrap"><span class="eyebrow">Legal</span><h1>Privacy</h1><p class="meta">Updated {UPDATED}</p></div></header>
<article class="prose">
<h2>The short version</h2>
<p>Badr Edge doesn't ask you to create an account, doesn't use advertising trackers and doesn't sell data.</p>
<h2>Files you load into the tools</h2>
<p>Trade lists (CSV, Excel or pasted text) are processed entirely in your browser. They are not uploaded to any server.</p>
<h2>Browser storage</h2>
<p>The tools save your settings and loaded trade lists in your own browser's local storage so they're there next time. This stays on your device. You can clear it at any time through your browser settings.</p>
<h2>Hosting</h2>
<p>The site is hosted on Cloudflare. Like any web host, Cloudflare processes basic technical data (such as IP addresses) to deliver pages and protect the site from abuse. See Cloudflare's privacy policy for details.</p>
<h2>Third-party resources</h2>
<p>Some tool pages load fonts from Google Fonts and code libraries from a public CDN (cdnjs). Those providers receive standard request data when your browser fetches them.</p>
<h2>Email</h2>
<p>If you email hello@badredge.com, your message is used only to reply to you.</p>
<h2>Contact</h2>
<p><a href="mailto:hello@badredge.com">hello@badredge.com</a></p>
</article>
"""
    return page("/legal/privacy/", "Privacy", "Badr Edge privacy: no accounts, no ad trackers; tool data stays in your browser.", "", body)


def not_found():
    body = """
<section class="page-head" style="padding:120px 0"><div class="wrap" style="align-items:flex-start">
  <span class="eyebrow">404</span>
  <h1>This page is <span class="gold">off the chart.</span></h1>
  <p class="lede">The page you're looking for doesn't exist or has moved.</p>
  <div class="hero-actions"><a class="btn primary" href="/">Back to home</a><a class="btn" href="/tools/">Open the tools</a></div>
</div></section>
"""
    path = "/404.html"
    out = os.path.join(ROOT, "404.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(head("Page not found", "Page not found.", "/404.html") + header("") + body + footer())
    return None


def statics(paths):
    urls = [p for p in paths if p] + ["/tools/pass/", "/tools/payout/", "/tools/sizing/"]
    today = datetime.date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    sm += "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
    # Old /research/graveyard/ URLs: server-side 301s, plus stub pages in case _redirects is not applied.
    open(os.path.join(ROOT, "_redirects"), "w").write(
        "/research/graveyard /research/backtested/ 301\n/research/graveyard/ /research/backtested/ 301\n/research/graveyard/* /research/backtested/:splat 301\n/research/lessons /research/ 301\n/research/lessons/ /research/ 301\n"
        + "".join(f"/research/backtested/{f['slug']}/ {research.family_url(f['slug'])} 301\n" for f in research.FAMILIES if not research.has_results(f["slug"])))
    fam_new = lambda sl: f"/research/backtested/{sl}/" if research.has_results(sl) else research.family_url(sl)
    stubs = [("graveyard/", "/research/backtested/")] + [("graveyard/" + f["slug"] + "/", fam_new(f["slug"])) for f in research.FAMILIES]
    # Families without results moved from Backtested to Research
    stubs += [("backtested/" + f["slug"] + "/", research.family_url(f["slug"])) for f in research.FAMILIES if not research.has_results(f["slug"])]
    stubs.append(("lessons/", "/research/"))
    for old_sub, new in stubs:
        d = os.path.join(ROOT, "research", old_sub)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(
            f'<!doctype html><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{SITE}{new}">'
            f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={new}"><a href="{new}">This page has moved.</a>\n')
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "favicon.svg"), "w").write(
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><defs><radialGradient id='m' cx='.38' cy='.36' r='.7'>"
        "<stop offset='0' stop-color='#f1dcae'/><stop offset='.55' stop-color='#c8a15c'/><stop offset='1' stop-color='#8a6a32'/></radialGradient></defs>"
        "<rect width='64' height='64' rx='12' fill='#0b0d10'/><circle cx='32' cy='32' r='18' fill='url(#m)'/>"
        "<circle cx='38' cy='37' r='3' fill='#6e5226' opacity='.35'/><circle cx='27' cy='40' r='2' fill='#6e5226' opacity='.28'/><circle cx='39' cy='25' r='1.8' fill='#6e5226' opacity='.25'/></svg>\n")


if __name__ == "__main__":
    built = [
        home(), tools_index(), guides_index(),
        article("/guides/trailing-drawdown/", "Trailing drawdown, explained with numbers", GUIDES[0][2], GUIDES[0][3], ARTICLE_DD, "/tools/sizing/", "Contract Sizing tool"),
        article("/guides/prop-evaluation-math/", "The math of passing a prop evaluation", GUIDES[1][2], GUIDES[1][3], ARTICLE_MATH, "/tools/pass/", "Prop Pass Simulator"),
        article("/guides/contract-sizing/", "Sizing contracts against a trailing max loss", GUIDES[2][2], GUIDES[2][3], ARTICLE_SIZE, "/tools/sizing/", "Contract Sizing tool"),
        article("/guides/opening-range-breakout/", GUIDES[3][1], GUIDES[3][2], GUIDES[3][3], ARTICLE_ORB, "/tools/sizing/", "Contract Sizing tool",
                cta='The range height is your risk. The <a href="/tools/sizing/">Contract Sizing tool</a> turns a stop in points into a contract size your cushion can carry.'),
        article("/guides/initial-balance/", GUIDES[4][1], GUIDES[4][2], GUIDES[4][3], ARTICLE_IB, "/tools/sizing/", "Contract Sizing tool",
                cta='A wide IB means a wide stop. The <a href="/tools/sizing/">Contract Sizing tool</a> shows how many contracts that stop allows under your max loss.'),
        pine(), about(), legal_disclaimer(), legal_privacy(),
    ] + research.build_all(page, ICONS)
    not_found()
    statics(built)
    print("built", len(built), "pages")
