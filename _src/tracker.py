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
    <p>{n} strategies added together, or one market at a time. One contract each, after fees and slippage. Gold is the in-sample backtest; teal is new data since the settings were frozen.</p></div>
    <div class="chips" role="group" aria-label="Filter by market"></div>
  </div>"""
    else:
        head = f"""<div class="trk-head">
    <div><h2>Results tracker</h2>
    <p>{'The ' + str(n) + ' strategies in this family added together, or one at a time.' if n > 1 else 'Day by day.'} One contract, after fees and slippage. Gold is the in-sample backtest; teal is new data since the settings were frozen.</p></div>
    {'<div class="chips" role="group" aria-label="Filter by strategy"></div>' if n > 1 else ''}
  </div>"""
    return f"""
<section class="trk" data-family="{family or ''}">
  {head}
  <div class="trk-card">
    <div class="lbls"><span class="lbl"><i></i>Hypothetical backtest · after costs</span><span class="lbl">Exploratory · requires forward testing</span><span class="lbl f"><i></i>New data · settings frozen 21 Oct</span></div>
    <div class="trk-chart" aria-label="Equity curve with drawdown underneath"></div>
    <div class="sec-t">In-sample · {IN_WIN} · <span class="trk-sel"></span></div>
    <dl class="k row isk">{_k('Net after costs','net')}{_k('Max drawdown','dd')}{_k('Profit factor','pf')}{_k('Win rate','wr')}{_k('Trades','tr')}{_k('Green days','g')}{_k('Red days','r')}{_k('Longest green streak','mg')}{_k('Longest red streak','mr')}</dl>
    <div class="sec-t f">Since the freeze · {OUT_WIN} · new data, settings unchanged</div>
    <dl class="k row fwk">{_k('Net after costs','net')}{_k('Win rate','wr')}{_k('Trades','tr')}{_k('Green days','g')}{_k('Red days','r')}</dl>
    <p class="foot-note">Hypothetical results for one contract per strategy, after fees and one tick of slippage on each side. The in-sample period falls inside the year the settings were picked on, so it is flattered by that search. Drawdown is measured on daily closes. {_late(ss)} Not financial advice and not a signal.</p>
  </div>
</section>"""


def data_tag():
    return ('<script type="application/json" id="trk-data">' + json.dumps(DATA, separators=(",", ":")) + "</script>"
            '<script src="/assets/tracker.js" defer></script>')
