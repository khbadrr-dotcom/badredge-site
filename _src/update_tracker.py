#!/usr/bin/env python3
"""Append new days to the results tracker from TradingView Deep Backtesting runs.

Used by the weekly (Saturday) update. The TradingView runs themselves are done by the
TradingView connector; this script only turns their trade lists into daily rows.

Usage:
  python3 _src/update_tracker.py --sources SOURCES.json [--transcript FILE | --raw DIR]
                                 [--summary OUT.md] [--dry-run]

SOURCES.json is kept outside this public repo (it holds the private script ids and
settings). Each entry needs: name (as in tracker.json), script_id, version, symbol;
optional: warmup (days of history the run needs before "thru", default --warmup).

Where the runs come from:
  --transcript  a Claude Code session log (.jsonl). Default: the newest log under
                ~/.claude/projects. Every TradingView backtest result in it is read, so
                no numbers are copied by hand.
  --raw         a folder of saved backtest responses (one JSON file per run).

Rules (append only):
  * Each strategy keeps a "thru" date: the last day its rows are complete for.
  * Only trades that closed after "thru" (by exit date in GMT+3) are added, and "thru"
    moves to the last day of the run. Days already published are never rewritten.
  * Net per trade = TradingView profit / qty - the method's base cost (same as
    make_tracker_data.py), so the numbers stay comparable with the original exports.

Checks that stop the update (exit code 1, tracker.json untouched):
  * a strategy in SOURCES has no run, or the run used another script version
  * the trade list is incomplete (returned != total) or its sum differs from net profit
  * the run starts less than --warmup days before "thru" (indicators need history)
  * the runs do not all end on the same day
Days that overlap already-published rows are compared and differences are listed in the
summary as warnings (they are not changed).
"""
import argparse, glob, json, os, sys
import datetime as dt
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "tracker.json")
COST = {"MGC": 3.92, "MES": 3.72, "MNQ": 2.22, "MYM": 2.22, "M2K": 2.22, "SIL": 12.72,
        "PL": 14.32, "MCL": 3.72, "MHG": 4.42, "M6E": 3.50}
TZ = dt.timedelta(hours=3)  # trade dates are GMT+3, like the original exports


def day_of(ts):
    return (dt.datetime.fromtimestamp(ts, dt.timezone.utc) + TZ).strftime("%Y-%m-%d")


def newest_transcript():
    logs = glob.glob(os.path.expanduser("~/.claude/projects/**/*.jsonl"), recursive=True)
    if not logs:
        sys.exit("no session log found; pass --transcript or --raw")
    return max(logs, key=os.path.getmtime)


def _results_from_text(txt):
    try:
        r = json.loads(txt)
    except ValueError:
        return []
    return [r] if isinstance(r, dict) and r.get("mode") == "deep_backtesting" and "report" in r else []


def load_runs(transcript=None, raw=None):
    """All Deep Backtesting results, oldest first."""
    out = []
    if raw:
        for f in sorted(glob.glob(os.path.join(raw, "*.json"))):
            out += _results_from_text(open(f, encoding="utf-8").read())
        return out
    for line in open(transcript, encoding="utf-8"):
        if "deep_backtesting" not in line:
            continue
        try:
            o = json.loads(line)
        except ValueError:
            continue
        content = (o.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for b in content:
            if isinstance(b, dict) and b.get("type") == "tool_result":
                c = b.get("content")
                txt = c if isinstance(c, str) else "".join(x.get("text", "") for x in c or [] if isinstance(x, dict))
                out += _results_from_text(txt)
    return out


def rows_for(trades, cost):
    days = defaultdict(lambda: [0.0, 0, 0, 0.0, 0.0])
    for t, profit, qty in trades:
        pnl = profit / qty - cost
        a = days[day_of(t)]
        a[0] += pnl; a[1] += 1; a[2] += pnl > 0
        a[3 if pnl > 0 else 4] += abs(pnl)
    return {d: [d, round(a[0], 2), a[1], a[2], round(a[3], 2), round(a[4], 2)] for d, a in days.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", required=True)
    ap.add_argument("--transcript")
    ap.add_argument("--raw")
    ap.add_argument("--summary")
    ap.add_argument("--warmup", type=int, default=28, help="minimum days of history before thru")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    sources = json.load(open(a.sources, encoding="utf-8"))
    runs = load_runs(a.transcript or (None if a.raw else newest_transcript()), a.raw)
    D = json.load(open(DATA, encoding="utf-8"))
    by_name = {s["name"]: s for s in D["strategies"]}
    errors, warns, lines, ends = [], [], [], set()
    updates = {}

    for src in sources:
        s = by_name.get(src["name"])
        if s is None:
            errors.append(f"{src['name']}: not in tracker.json"); continue
        thru = s.get("thru") or s["days"][-1][0]
        match = [r for r in runs if r.get("script_id") == src["script_id"]
                 and src["symbol"] in (r.get("symbol"), r.get("symbol_requested"))]
        if not match:
            errors.append(f"{src['name']}: no TradingView run found"); continue
        r = match[-1]  # the latest run wins
        if str(r.get("version")) != str(src["version"]):
            errors.append(f"{src['name']}: ran script version {r.get('version')}, expected {src['version']}"); continue
        rep = r["report"]; perf = rep["performance"]["all"]; rng = rep["range"]["backtest"]
        trades = [[x["exit"]["t"], x["profit"], x["qty"]] for x in rep["trades"]]
        if not (len(trades) == rep.get("trades_total", len(trades)) == perf["total_trades"]):
            errors.append(f"{src['name']}: incomplete trade list ({len(trades)} of {perf['total_trades']}); shorten the run"); continue
        if abs(sum(t[1] for t in trades) - perf["net_profit"]) > 0.01:
            errors.append(f"{src['name']}: trades do not add up to net profit"); continue
        # the period end is exclusive at 00:00Z (date_to = Saturday ends on Friday)
        start = rng["from"][:10]
        end = (dt.datetime.fromisoformat(rng["to"].replace("Z", "+00:00")) - dt.timedelta(minutes=1)).date().isoformat()
        warmup = int(src.get("warmup", a.warmup))
        if (dt.date.fromisoformat(thru) - dt.date.fromisoformat(start)).days < warmup:
            errors.append(f"{src['name']}: run starts {start}, needs {warmup}+ days before {thru}"); continue
        ends.add(end)
        rows = rows_for(trades, COST[s["mkt"]])
        new = [rows[d] for d in sorted(rows) if thru < d <= end]
        old = {x[0]: x for x in s["days"]}
        lo = max(start, (dt.date.fromisoformat(thru) - dt.timedelta(days=14)).isoformat())
        for d in sorted(set(rows) | set(old)):
            if lo <= d <= thru and rows.get(d, [d, 0, 0])[:3] != old.get(d, [d, 0, 0])[:3]:
                tv, o = rows.get(d), old.get(d)
                warns.append(f"{src['name']} {d}: TradingView " + (f"{tv[1]:+.2f} ({tv[2]} tr)" if tv else "no trade")
                             + ", published " + (f"{o[1]:+.2f} ({o[2]} tr)" if o else "no trade"))
        updates[src["name"]] = (new, end)
        lines.append((src["name"], len(new), sum(x[2] for x in new), sum(x[1] for x in new)))

    if len(ends) > 1:
        errors.append(f"runs end on different days: {sorted(ends)}; rerun with the same date_to")
    if errors:
        print("UPDATE STOPPED\n" + "\n".join("  " + e for e in errors))
        sys.exit(1)

    end = ends.pop()
    for s in D["strategies"]:
        if s["name"] in updates:
            new, _ = updates[s["name"]]
            s["days"] += new
            s["thru"] = end
    D["to"] = max([D["to"], end])
    for s in D["strategies"]:
        s.setdefault("thru", s["days"][-1][0])

    total = sum(l[3] for l in lines)
    md = [f"Weekly tracker update through **{end}** (TradingView Deep Backtesting, 1 contract, after costs).", "",
          "| Strategy | New days | Trades | Net |", "|---|---:|---:|---:|"]
    md += [f"| {n} | {k} | {t} | {v:+,.2f} |" for n, k, t, v in sorted(lines)]
    md += [f"| **All** | | {sum(l[2] for l in lines)} | **{total:+,.2f}** |", ""]
    if warns:
        md += ["Overlap check (published rows are kept as they are):", ""] + [f"- {w}" for w in warns] + [""]
    else:
        md += ["Overlap check: every already-published day in the run window matches TradingView.", ""]
    text = "\n".join(md)
    print(text)
    if a.summary:
        open(a.summary, "w", encoding="utf-8").write(text + "\n")
    if a.dry_run:
        print("(dry run: tracker.json not written)"); return
    json.dump(D, open(DATA, "w", encoding="utf-8"), separators=(",", ":"))
    print("tracker.json updated")


if __name__ == "__main__":
    main()
