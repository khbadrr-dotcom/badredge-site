#!/usr/bin/env python3
"""Builds the static pages of badredge.com.

Run:  python3 _src/build.py
It writes the HTML files at their published paths. The tools under /tools/<name>/ are
standalone pages and are not touched, except /tools/index.html, which is built here.
"""
import os, random, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import research

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://badredge.com"
YEAR = datetime.date.today().year
UPDATED = "November 2026"  # legal pages only; not shown on the homepage or footer

# The Badr Edge mark: a chamfered B with the cut-off corner set apart in brass (the "edge").
MARK_B = "M10 8H30L46 24V26L41 31L50 40V47L41 56H10Z M19 17H28L31 20.5L28 24H19Z M19 38H35L39 42.5L35 47H19Z"
MARK_E = "M35 8H46V19Z"
MARK = (f'<svg class="mark" viewBox="6 6 48 52" aria-hidden="true"><path class="mk-b" fill-rule="evenodd" d="{MARK_B}"/>'
        f'<path class="mk-e" d="{MARK_E}"/></svg>')
BRAND = f'<a class="brand" href="/" aria-label="Badr Edge home">{MARK}<span class="wm">Badr <span class="word-2">Edge</span></span></a>'

# Payout figure on /about/. Off until the lawyer call clears dollar figures on the site.
SHOW_PAYOUT_FIGURE = False
PAYOUT_FIGURE = "$250,000+"
PAYOUT_PROOF_URL = ""  # link to the payout records page or PDF, once it exists

NAV = [("/tools/", "Tools"), ("/guides/", "Guides"), ("/research/", "Research"), ("/pine/", "Pine Script"), ("/about/", "About")]

ICONS = {
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/></svg>',
    "coins": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><ellipse cx="9" cy="7" rx="6" ry="3"/><path d="M3 7v5c0 1.7 2.7 3 6 3s6-1.3 6-3V7"/><path d="M9 15v2c0 1.7 2.7 3 6 3s6-1.3 6-3v-5c0-1.7-2.7-3-6-3"/></svg>',
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
<meta name="theme-color" content="#090d0d">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Badr Edge">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/theme.js" defer></script>
{extra}</head>
<body>
"""


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>' for href, label in NAV)
    return f"""<header class="site-head">
  <div class="wrap">
    {BRAND}
    <nav class="nav" id="nav" aria-label="Main">{links}<a class="cta" href="/tools/">Open the tools</a></nav>
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
        <li><a href="/guides/">All guides</a></li>
      </ul></div>
      <div><h4>Badr Edge</h4><ul>
        <li><a href="/about/">About</a></li>
        <li><a href="/research/">Research</a></li>
        <li><a href="/pine/">Pine Script</a></li>
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


def guide_cards():
    return "\n      ".join(f"""<a class="card reveal" href="{h}">
        <div class="icon">{ICONS['book']}</div>
        <h3>{t}</h3>
        <p>{d}</p>
        <span class="go">{m} &rarr;</span>
      </a>""" for h, t, d, m in GUIDES)


def home():
    body = f"""
<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="eyebrow">Independent futures research desk</span>
      <h1>Trade with a process, <span class="gold">not a guess.</span></h1>
      <p class="lede">Free tools to plan risk, guides to the rules that move accounts, and an open record of how trading ideas get tested. Built by a working futures trader.</p>
      <div class="hero-actions">
        <a class="btn primary" href="/tools/">Explore the tools</a>
        <a class="btn" href="/research/">See the research</a>
      </div>
      <dl class="hero-meta"><div><dt>Access</dt><dd>Free, no sign-up</dd></div><div><dt>Built by</dt><dd>A working trader</dd></div><div><dt>Signals</dt><dd>None</dd></div></dl>
    </div>
    <div class="term reveal">
      <div class="term-bar"><span class="term-tabs"><span class="on"><b>MGC</b>5m</span><span>MES</span><span>MNQ</span></span><span class="term-tag">Illustration</span></div>
      <div class="term-chart">{desk_chart()}</div>
      <div class="ch-legend"><span><i class="bx"></i>Opening range</span><span><i></i>Range high / low</span><span><i class="vw"></i>Session average</span></div>
      <div class="desk">
      <a class="desk-row" href="/tools/"><span class="desk-ico">{ICONS['target']}</span><span class="desk-name">Tools<small>Risk, sizing and planning simulators</small></span><span class="desk-state live">3 live</span></a>
      <a class="desk-row" href="/guides/"><span class="desk-ico">{ICONS['book']}</span><span class="desk-name">Guides<small>The rules behind the numbers</small></span><span class="desk-state live">3 published</span></a>
      <a class="desk-row" href="/research/"><span class="desk-ico">{ICONS['shield']}</span><span class="desk-name">Research<small>How ideas get tested, in the open</small></span><span class="desk-state live">{len(research.FAMILIES)} families</span></a>
      <a class="desk-row" href="/pine/"><span class="desk-ico">{ICONS['code']}</span><span class="desk-name">Pine Script<small>Tested TradingView strategy work</small></span><span class="desk-state">Soon</span></a>
      </div>
    </div>
  </div>
</section>

<div class="specbar"><div class="wrap"><dl>
  <div><dt>Markets</dt><dd>MGC MES MNQ MYM <span>+6</span></dd></div>
  <div><dt>Sessions</dt><dd>Asia · London · New York</dd></div>
  <div><dt>Research</dt><dd>{len(research.FAMILIES)} families <span>·</span> 0 passed</dd></div>
  <div><dt>Tools</dt><dd>3 simulators <span>·</span> in-browser</dd></div>
</dl></div></div>

<section class="band" id="desk">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Inside the desk</span>
      <h2>Everything here serves <span class="gold">one process.</span></h2>
      <p class="lede">Plan before the session, size to what the account can take, and review what happened. Each part of Badr Edge supports one of those steps.</p>
    </div>
    <div class="grid-2 doors">
      <a class="card reveal" href="/tools/">
        <div class="icon">{ICONS['target']}</div><span class="tagline">Live</span>
        <h3>Tools</h3>
        <p>Free simulators for risk, position size and account planning. Put in your own numbers or a TradingView trade list and see the range of outcomes.</p>
        <span class="go">Explore the tools &rarr;</span>
      </a>
      <a class="card reveal" href="/guides/">
        <div class="icon">{ICONS['book']}</div><span class="tagline">Live</span>
        <h3>Guides</h3>
        <p>Clear breakdowns of drawdown, sizing and the maths of an attempt, with worked numbers and a tool to test each idea.</p>
        <span class="go">Read the guides &rarr;</span>
      </a>
      <a class="card reveal" href="/research/">
        <div class="icon">{ICONS['shield']}</div><span class="tagline">Live</span>
        <h3>Research</h3>
        <p>A public log of how trading ideas are built, frozen and stress-tested before they're trusted, including the ones that failed.</p>
        <span class="go">Open the research &rarr;</span>
      </a>
      <a class="card reveal" href="/pine/">
        <div class="icon">{ICONS['code']}</div><span class="tagline">Soon</span>
        <h3>Pine Script</h3>
        <p>How TradingView strategies get written in Pine Script v6 and validated with realistic costs and out-of-sample tests.</p>
        <span class="go">Opening soon &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">The process</span>
      <h2>Plan, size, review. <span class="gold">Every session.</span></h2>
    </div>
    <div class="steps">
      <div class="step reveal"><h3>Plan the risk</h3><p>Decide what a bad day costs before the session starts. Know your loss limit, your stop and the point where you walk away.</p></div>
      <div class="step reveal"><h3>Size to the account</h3><p>Trade the size the account can survive, not the size you hope for. Add size only when the cushion has grown to carry it.</p></div>
      <div class="step reveal"><h3>Review the evidence</h3><p>Look at what you did, not what you remember. Check if your edge still looks like the one you planned with.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Principles</span>
      <h2>What Badr Edge is, <span class="gold">and what it isn't.</span></h2>
    </div>
    <div class="principles">
      <div class="principle reveal"><b>No signals</b><span>You won't find trade calls or alerts here. You make your own decisions.</span></div>
      <div class="principle reveal"><b>No promised returns</b><span>No win rates, no screenshots of profits, no "guaranteed" anything.</span></div>
      <div class="principle reveal"><b>Tools over talk</b><span>Every idea comes with a way to test it on your own numbers.</span></div>
      <div class="principle reveal"><b>Private by design</b><span>The tools run in your browser. Nothing you load is uploaded.</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Latest guides</span>
      <h2>Start with the rules <span class="gold">that end accounts.</span></h2>
      <p class="lede">Worked numbers, no jargon. Each guide links to a tool so you can test the idea yourself.</p>
    </div>
    <div class="grid-3">
      {guide_cards()}
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Research</span><h2>Most strategies fail. Here's the record.</h2>
      <p class="lede">A public log of a futures research desk: the method, every strategy family tested, results after costs, and why each one was closed. No strategy has passed final validation.</p></div>
    <div class="grid-3">
      <a class="card reveal" href="/research/method/"><div class="icon">{ICONS['scale']}</div><h3>Method</h3><p>Explore, freeze, validate. Random-direction nulls, unseen years and real costs.</p><span class="go">Read the method</span></a>
      <a class="card reveal" href="/research/graveyard/"><div class="icon">{ICONS['shield']}</div><h3>Strategy graveyard</h3><p>Opening ranges, FVGs, pivots, momentum and more. One page each, with the verdict.</p><span class="go">Open the graveyard</span></a>
      <a class="card reveal" href="/research/lessons/"><div class="icon">{ICONS['book']}</div><h3>Lessons</h3><p>Why in-sample results fool you, and why costs beat most retail setups.</p><span class="go">Read the lessons</span></a>
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
      <details><summary>Do you sell signals or courses?</summary><p>No. There are no signals, alerts or courses here. Pine Script work is described on the <a href="/pine/" >Pine Script page</a>.</p></details>
      <details><summary>Is any of this financial advice?</summary><p>No. Everything here is educational. Simulations are hypothetical and rely on the inputs you give them. Your trading decisions are your own.</p></details>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <span class="eyebrow">Start here</span>
    <h2>Start where <span class="gold">you are.</span></h2>
    <p class="lede">Have numbers to test? Open a tool. Want the reasoning first? Read a guide.</p>
    <div class="hero-actions" style="justify-content:center"><a class="btn primary" href="/tools/">Explore the tools</a><a class="btn" href="/guides/">Read the guides</a></div>
  </div>
</section>
"""
    return page("/", "Badr Edge",
                "Badr Edge: a working futures trader's desk, opened up. Free risk tools, guides and research on how trading ideas get tested.",
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
  <p class="lede">Worked examples. Each guide ends with a tool to test the idea on your own numbers.</p>
</div></section>
<section style="padding-top:24px"><div class="wrap"><div class="grid-3">
  {guide_cards()}
</div></div></section>
"""
    return page("/guides/", "Guides", "Guides to trailing drawdown, prop evaluation math and contract sizing for futures traders, with worked numbers.", "/guides/", body)


def article(path, title, desc, minutes, body_html, tool_href, tool_name):
    body = f"""
<header class="article-head"><div class="wrap">
  <a class="eyebrow" href="/guides/" style="text-decoration:none">&larr; Guides</a>
  <h1>{title}</h1>
  <p class="lede">{desc}</p>
  <p class="meta">{minutes}</p>
</div></header>
<article class="prose">
{body_html}
<div class="callout"><p><strong>Test it on your numbers.</strong> The <a href="{tool_href}">{tool_name}</a> runs this on your own win rate, averages or TradingView trade list.</p></div>
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

<h3>3. Trailing, intraday</h3>
<p>The floor follows your highest balance at any moment, including open profit. If a trade runs +$800 and comes back to breakeven, the floor already moved up $800 and stays there. This is the strictest type: letting winners breathe can shrink your cushion even on trades you don't lose.</p>

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

<h2>Two ways to fail</h2>
<ul>
  <li><strong>Too big:</strong> a normal losing streak hits the floor before the edge has time to show.</li>
  <li><strong>Too small:</strong> the attempt runs out of time or patience. You reset, pay again, or start forcing trades.</li>
</ul>
<p>The best size is usually in the middle, and it's narrower than people expect. That is exactly what a Monte Carlo simulation finds: it replays thousands of attempts at each size and counts how many pass, fail or stall.</p>

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
<p>The ladder does what discipline often doesn't: it cuts size after losses and only adds it when the account has earned the room.</p>
<div class="callout"><p>The block size is the key number. Too small and a normal losing streak breaches the floor. Too large and the account grows slowly. The Contract Sizing tool searches for the smallest block that keeps your breach chance under a limit you choose.</p></div>

<h2>Don't forget costs</h2>
<p>Commission and slippage are charged per contract, so they scale with size. One tick of slippage on MNQ is $0.50, but over hundreds of trades and several contracts it adds up. Always test your size with costs included.</p>
"""


def pine():
    body = """
<section class="page-head"><div class="wrap">
  <span class="eyebrow">Pine Script</span>
  <h1>Built in v6. Tested until it breaks.</h1>
  <p class="lede">I build TradingView strategies in Pine Script v6 for my own systematic research. This page shows how I write and validate them, and where I can help.</p>
</div></section>

<section style="padding-top:24px"><div class="wrap">
  <div class="grid-3">
    <div class="card reveal"><div class="icon">""" + ICONS["code"] + """</div><h3>Fixes and clean-ups</h3><p>Repainting, wrong session times, orders that don't fire, inputs that do nothing. Find the bug, fix it, and explain what was wrong.</p></div>
    <div class="card reveal"><div class="icon">""" + ICONS["code"] + """</div><h3>Upgrades to v6</h3><p>Move older scripts to Pine v6 with the same logic, cleaner inputs and fewer surprises, checked trade by trade against the original.</p></div>
    <div class="card reveal"><div class="icon">""" + ICONS["shield"] + """</div><h3>Validation reports</h3><p>An independent stress test of a strategy you already have: costs, slippage, unseen data and Monte Carlo, in one written report.</p></div>
  </div>
  <div class="callout" style="margin-top:28px;max-width:820px"><p><strong>Opening soon.</strong> Services aren't open for orders yet. Questions are welcome at <a href="mailto:hello@badredge.com" style="color:var(--gold)">hello@badredge.com</a>.</p></div>
</div></section>

<section class="band"><div class="wrap split">
  <div class="sec-head" style="margin:0">
    <span class="eyebrow">How a strategy gets tested</span>
    <h2>Most backtests are too kind. These aren't.</h2>
    <ul class="checklist" style="margin-top:8px">
      <li><span><b>Frozen rules.</b> Settings are fixed before the test, so the result can't be tuned after the fact.</span></li>
      <li><span><b>Real costs.</b> Commission per contract and at least one tick of slippage on every trade.</span></li>
      <li><span><b>Unseen data.</b> Sized and tuned on earlier months, then judged on months it never saw.</span></li>
      <li><span><b>Stress tests.</b> Doubled slippage, losses 50% bigger, winners 10% smaller.</span></li>
      <li><span><b>Many-tests check.</b> When many variants are tried, results are corrected so a lucky one doesn't look like an edge.</span></li>
      <li><span><b>Independent replica.</b> The Pine logic is rebuilt outside TradingView and compared trade by trade.</span></li>
    </ul>
  </div>
  <div class="figure reveal">
    <div class="code" style="border:0;padding:4px 2px;background:transparent">VALIDATION REPORT · structure

<span class="k">1</span>  Summary and verdict
     PASS · NO EDGE · INSUFFICIENT EVIDENCE
<span class="k">2</span>  Rules as tested (frozen inputs)
<span class="k">3</span>  Costs and fill assumptions
<span class="k">4</span>  In-sample vs out-of-sample
<span class="k">5</span>  Year-by-year stability
<span class="k">6</span>  Stress: 2× slippage, smaller winners
<span class="k">7</span>  Monte Carlo drawdown range
<span class="k">8</span>  Prop-rule fit: pass and payout odds
<span class="k">9</span>  Code review notes</div>
    <figcaption>The structure of a report. The verdict can be "no edge", and often is. That's the point.</figcaption>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">What you won't get</span><h2>Clear lines</h2></div>
  <div class="principles">
    <div class="principle"><b>No signals</b><span>No trade calls, alerts or copy trading.</span></div>
    <div class="principle"><b>No performance promises</b><span>A test describes the past under stated assumptions. It doesn't predict profit.</span></div>
    <div class="principle"><b>No resold strategies</b><span>Your code stays yours and isn't shared or reused.</span></div>
    <div class="principle"><b>No advice</b><span>Engineering and testing only. Trading decisions are yours.</span></div>
  </div>
</div></section>
"""
    return page("/pine/", "Pine Script", "Pine Script v6 strategy development and validation: frozen rules, realistic costs, out-of-sample and stress testing.", "/pine/", body)


def about():
    if SHOW_PAYOUT_FIGURE:
        proof = (f'<a class="proof" href="{PAYOUT_PROOF_URL}">View payout records &rarr;</a>' if PAYOUT_PROOF_URL
                 else '<span class="proof off">Payout records available on request</span>')
        fig = f"""<span class="k">Prop firm payouts</span>
      <span class="v">{PAYOUT_FIGURE}</span>
      <p>Paid out by prop firms on funded accounts, from firm dashboards and payout certificates. Not audited, and not a return on anyone else's money.</p>
      {proof}"""
    else:
        fig = """<span class="k">Prop firm payouts</span>
      <span class="v pending">Payout record on file.</span>
      <p>Payouts from four prop firms are documented with dashboards and certificates. A summary will be published here once it has been reviewed.</p>
      <span class="proof off">Summary in review</span>"""
    body = f"""
<section class="page-head"><div class="wrap">
  <span class="eyebrow">About</span>
  <h1>Built from real trading. <span class="gold">Refined through research.</span></h1>
  <p class="lede">Badr Edge is an independent futures research desk, built on more than three years of active trading and shaped by data, testing and disciplined execution.</p>
</div></section>

<section style="padding:48px 0 0"><div class="wrap">
  <div class="record reveal">
    <div class="record-fig">
      {fig}
    </div>
    <dl>
      <div><dt>Experience</dt><dd><b>3+ years</b> of active trading in financial markets</dd></div>
      <div><dt>Prop firms</dt><dd>Evaluations passed at <b>6 firms</b>, payouts from <b>4</b>, promoted to the live funded stage at <b>3</b></dd></div>
      <div><dt>Markets</dt><dd>Gold and US equity index futures, mainly micros: MGC, MES, MNQ, MYM</dd></div>
      <div><dt>Also</dt><dd>Personal CFD brokerage accounts, traded alongside the prop accounts</dd></div>
      <div><dt>Method</dt><dd>Discretionary price action for execution; systematic research for everything that can be tested</dd></div>
    </dl>
  </div>
</div></section>

<article class="prose" style="max-width:820px;padding-top:56px;padding-bottom:0">
  <h2>Experience</h2>
  <p>Most of my trading has been through proprietary trading firms: passing evaluations, trading funded accounts under each firm's rules and drawdown limits, and taking payouts. At three firms that has led to promotion to the live funded stage, and the work now is progressing toward trading live funded accounts at size. Alongside the prop accounts, I trade personal CFD brokerage accounts.</p>
  <p>Execution is a discretionary candlestick price-action process, built over two years and traded mostly in gold and US index futures across the Asia, London and New York sessions.</p>

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
  <p>Every tool here started as something I built for my own accounts. The research is published in full, including the failures, which are most of it.</p>

  <h2>The name</h2>
  <p>Badr is Arabic for the full moon: the night you can see the whole picture. The edge is the process, not a promise of results.</p>

  <h2>Get in touch</h2>
  <p>Feedback, bug reports and tool ideas: <a href="mailto:hello@badredge.com">hello@badredge.com</a>.</p>
  <p class="note">Past payouts and trading results do not predict future results. Badr Edge does not manage money, offer signals or give investment advice. See the <a href="/legal/disclaimer/">disclaimer</a>.</p>
</article>
"""
    return page("/about/", "About", "About Badr Edge: an independent futures research desk built on more than three years of active trading, mostly through prop firms.", "/about/", body)


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
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "favicon.svg"), "w").write(
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='12' fill='#0c1111'/>"
        f"<g transform='translate(3 2) scale(.94)'><path fill='#e3e8e5' fill-rule='evenodd' d='{MARK_B}'/><path fill='#c8a15c' d='{MARK_E}'/></g></svg>\n")


if __name__ == "__main__":
    built = [
        home(), tools_index(), guides_index(),
        article("/guides/trailing-drawdown/", "Trailing drawdown, explained with numbers", GUIDES[0][2], GUIDES[0][3], ARTICLE_DD, "/tools/sizing/", "Contract Sizing tool"),
        article("/guides/prop-evaluation-math/", "The math of passing a prop evaluation", GUIDES[1][2], GUIDES[1][3], ARTICLE_MATH, "/tools/pass/", "Prop Pass Simulator"),
        article("/guides/contract-sizing/", "Sizing contracts against a trailing max loss", GUIDES[2][2], GUIDES[2][3], ARTICLE_SIZE, "/tools/sizing/", "Contract Sizing tool"),
        pine(), about(), legal_disclaimer(), legal_privacy(),
    ] + research.build_all(page, ICONS)
    not_found()
    statics(built)
    print("built", len(built), "pages")
