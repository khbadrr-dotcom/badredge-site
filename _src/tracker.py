"""Results tracker: equity curve, drawdown and day stats from derived daily results (see make_tracker_data.py)."""
import json, os
from datetime import date

DATA = json.load(open(os.path.join(os.path.dirname(__file__), "data", "tracker.json")))
STRATS = DATA["strategies"]


def _d(s):
    d = date.fromisoformat(s)
    return f"{d.day} {d.strftime('%b')} {d.year}"


def _last_before_freeze():
    return max(x[0] for s in STRATS for x in s["days"] if x[0] < DATA["freeze"])


IN_WIN = f"{_d(DATA['from'])} – {_d(_last_before_freeze())}"
OUT_WIN = f"{_d(DATA['freeze'])} – {_d(DATA['to'])}"


def _late(ss):
    """Strategies whose trade list starts well after the window opens (only a shorter export was available)."""
    start = date.fromisoformat(DATA["from"])
    late = [s for s in ss if (date.fromisoformat(s["days"][0][0]) - start).days > 60]
    return "".join(f" {s['name']} starts on {_d(s['days'][0][0])} because only a shorter trade list was available." for s in late)


def _k(label, key):
    return f'<div><dt>{label}</dt><dd data-s="{key}">–</dd></div>'


def card(family=None):
    """family=None: all strategies with ticker chips. Otherwise one family's strategies with a chip per strategy."""
    ss = [s for s in STRATS if family is None or s["slug"] == family]
    if not ss:
        return ""
    n = len(ss)
    if family is None:
        head = f"""<div class="trk-head">
    <div><span class="eyebrow">Results tracker</span><h2>All strategies, <span class="gold">one ledger.</span></h2>
    <p>{n} strategies added together, or one market at a time. One contract each, after fees and slippage. Gold is the in-sample backtest; teal is forward data on unchanged settings, latest through {_d(DATA['to'])}.</p></div>
    <div class="chips" role="group" aria-label="Filter by market"></div>
  </div>"""
    else:
        head = f"""<div class="trk-head">
    <div><h2>Results tracker</h2>
    <p>{'The ' + str(n) + ' strategies in this family added together, or one at a time.' if n > 1 else 'Day by day.'} One contract, after fees and slippage. Gold is the in-sample backtest; teal is forward data on unchanged settings, latest through {_d(DATA['to'])}.</p></div>
    {'<div class="chips" role="group" aria-label="Filter by strategy"></div>' if n > 1 else ''}
  </div>"""
    return f"""
<section class="trk" data-family="{family or ''}">
  {head}
  <div class="trk-card">
    <div class="lbls"><span class="lbl"><i></i>Hypothetical backtest · after costs</span><span class="lbl">Exploratory · in forward testing</span><span class="lbl f"><i></i>Forward data · updated every Saturday · one set of settings across the whole chart</span></div>
    <div class="trk-chart" aria-label="Equity curve with drawdown underneath"></div>
    <div class="sec-t">In-sample · {IN_WIN} · <span class="trk-sel"></span></div>
    <dl class="k row isk">{_k('Net after costs','net')}{_k('Max drawdown','dd')}{_k('Profit factor','pf')}{_k('Win rate','wr')}{_k('Trades','tr')}{_k('Green days','g')}{_k('Red days','r')}{_k('Longest green streak','mg')}{_k('Longest red streak','mr')}</dl>
    <div class="cal" aria-label="Daily results calendar">
      <div class="cal-head">
        <div><div class="sec-t">Daily results · hypothetical, after costs</div><b class="cal-m"></b><span class="cal-sum"></span></div>
        <div class="cal-nav"><button type="button" class="cal-prev" aria-label="Previous month">&lsaquo;</button><button type="button" class="cal-next" aria-label="Next month">&rsaquo;</button></div>
      </div>
      <div class="cal-grid" role="grid"></div>
      <p class="cal-tip" aria-live="polite">Tap a day for its trades. A teal dot marks forward data on unchanged settings.</p>
    </div>
    <p class="foot-note">Hypothetical results for one contract per strategy, after fees and one tick of slippage on each side. The in-sample period falls inside the year the settings were picked on, so it is flattered by that search. Drawdown is measured on daily closes. {_late(ss)} Not financial advice and not a signal.</p>
  </div>
</section>"""


def data_tag():
    return ('<script type="application/json" id="trk-data">' + json.dumps(DATA, separators=(",", ":")) + "</script>"
            '<script src="/assets/tracker.js" defer></script>')


def two_ways(indicators=None, tools_art=""):
    """Homepage section: the toolkit and the strategies, side by side."""
    from collections import defaultdict
    D = DATA
    day = defaultdict(float)
    for s in D["strategies"]:
        for x in s["days"]: day[x[0]] += x[1]
    ks = sorted(day); eq = [0]
    for k in ks: eq.append(eq[-1] + day[k])
    nIn = sum(1 for k in ks if k < D["freeze"])
    W, H = 520, 120
    hi, lo = max(eq), min(eq)
    X = lambda i: i / (len(eq) - 1) * W
    Y = lambda v: 8 + (hi - v) / (hi - lo) * (H - 16)
    pin = "".join(f"{'M' if i == 0 else 'L'}{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(eq[:nIn + 1]))
    pout = "".join(f"{'M' if i == 0 else 'L'}{X(i + nIn):.1f},{Y(v):.1f}" for i, v in enumerate(eq[nIn:]))
    spark = f'''<svg class="tw-spark" viewBox="0 0 {W} {H}" preserveAspectRatio="none"><defs><linearGradient id="twg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="var(--accent)" stop-opacity=".28"/><stop offset="1" stop-color="var(--accent)" stop-opacity="0"/></linearGradient></defs>
    <rect x="{X(nIn):.1f}" y="2" width="{W - X(nIn):.1f}" height="{H - 4}" rx="6" class="tw-fz"/>
    <path d="{pin}L{X(nIn):.1f},{H}L0,{H}Z" fill="url(#twg)"/><path d="{pin}" class="tw-eq"/><path d="{pout}" class="tw-fw"/>
    <circle cx="{W}" cy="{Y(eq[-1]):.1f}" r="3.5" class="tw-tip"/></svg>'''
    tools = [("Prop Pass Simulator", "/tools/pass/"), ("Payout Simulator", "/tools/payout/"), ("Contract Sizing", "/tools/sizing/")]
    tl = "".join(f'<a href="{h}">{a}</a>' for a, h in tools)
    ind = [x for x in (indicators or []) if x[3]]
    shot = next((x for x in ind if x[0] == "session-opening-range"), ind[0] if ind else None)
    shot_html = (f'<img class="tw-shot" src="/assets/ind/{shot[0]}.webp" alt="{shot[1]} on a futures chart" width="960" height="492" loading="lazy" decoding="async">' if shot else "")
    return f'''
    <section class="tw" id="two-ways"><div class="wrap">
      <div class="tw-head"><span class="eyebrow">Start here</span><h2>Pick your <span class="gold">starting point.</span></h2></div>
      <div class="tw-grid tw-3">
        <div class="tw-card">
          <div class="tw-top"><span class="tw-live">Free</span><span class="tw-kind">Tools</span></div>
          <h3>Plan the risk before the open.</h3>
          <p>Browser simulators built around prop-firm rules. No sign-up.</p>
          <div class="tw-vis">{tools_art}</div>
          <div class="tw-chips">{tl}</div>
          <a class="tw-cta" href="/tools/">Explore the tools <i>&rarr;</i></a>
        </div>
        <div class="tw-card">
          <div class="tw-top"><span class="tw-live">Free</span><span class="tw-kind">Indicators</span></div>
          <h3>Indicators for TradingView.</h3>
          <p>Open-source Pine Script v6, built from the research families.</p>
          <div class="tw-vis">{shot_html}</div>
          <div class="tw-chips"><a href="/tools/indicators/">Sessions and ranges</a><a href="/tools/indicators/">Liquidity</a><a href="/tools/indicators/">Market structure</a></div>
          <a class="tw-cta" href="/tools/indicators/">See the indicators <i>&rarr;</i></a>
        </div>
        <a class="tw-card" href="/research/backtested/">
          <div class="tw-top"><span class="tw-live">Updated weekly</span><span class="tw-kind">Strategy Lab</span></div>
          <h3>Strategies tested after costs.</h3>
          <p>Gold is last year, in-sample. Teal is forward data, updated weekly.</p>
          <div class="tw-chart">{spark}<div class="tw-axis"><span>Nov 2025</span><span>Nov 2026</span></div></div>
          <div class="tw-chips"><span>After costs</span><span>1 micro</span><span class="st">Exploratory</span></div>
          <span class="tw-cta">See the Strategy Lab <i>&rarr;</i></span>
        </a>
      </div>
      <p class="tw-note">Research only. Every strategy requires forward testing before any real-money use.</p>
    </div></section>'''
