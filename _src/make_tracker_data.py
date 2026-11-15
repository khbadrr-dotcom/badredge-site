"""Turn TradingView trade-list CSVs into derived daily results for the results tracker.

Usage: python3 _src/make_tracker_data.py <csv> [<csv> ...]
Writes _src/data/tracker.json: per strategy, daily net P&L for ONE contract after the method's base cost
(fee + 1 tick slippage each side). No prices or raw bars are stored.
"""
import csv, json, os, re, sys
from collections import defaultdict

COST = {"MGC": 3.92, "MES": 3.72, "MNQ": 2.22, "MYM": 2.22, "M2K": 2.22, "SIL": 12.72,
        "PL": 14.32, "MCL": 3.72, "MHG": 4.42, "M6E": 3.50}
# file-name pattern -> (strategy name as published, market code, family slug)
MAP = [
    (r"BH_MYM", ("MYM ORB Break & Hold", "MYM", "orb-break-and-hold")),
    (r"IBMultiSes_MGC", ("MGC IB Multi-Session", "MGC", "initial-balance")),
    (r"M2K_ORB_v4", ("M2K ORB v4", "M2K", "orb-v4")),
    (r"M6E_IB", ("M6E IB Multi-Session", "M6E", "initial-balance")),
    (r"MCL_ORB_v4", ("MCL ORB v4", "MCL", "orb-v4")),
    (r"MHG_IB", ("MHG IB Multi-Session", "MHG", "initial-balance")),
    (r"MNQ_IB", ("MNQ IB Multi-Session", "MNQ", "initial-balance")),
    (r"MNQ_ORB_v4", ("MNQ ORB v4", "MNQ", "orb-v4")),
    (r"ORB_PRO_1_CME_MINI_MES", ("MES ORB Pro Max", "MES", "orb-pro-max")),
    (r"PL_ORB_v4", ("PL ORB v4", "PL", "orb-v4")),
    (r"PRO_1_CBOT_MINI_MYM", ("MYM ORB Pro Max", "MYM", "orb-pro-max")),
    (r"SIL_ORB_v4", ("SIL ORB v4", "SIL", "orb-v4")),
    (r"ORB_v4_MGC", ("MGC ORB v4", "MGC", "orb-v4")),
    (r"ORB_PRO_1_COMEX_MINI_MGC", ("MGC ORB Pro Max", "MGC", "orb-pro-max")),
]
FREEZE = "2026-10-22"  # first day after the settings were frozen
END = "2026-11-06"  # common last day across the exports


def ident(path):
    base = os.path.basename(path)
    for pat, v in MAP:
        if re.search(pat, base) and not (pat == "MNQ_IB" and "ORB" in base):
            return v
    raise SystemExit(f"unknown file {base}")


out, first, last = [], None, None
for path in sys.argv[1:]:
    name, mkt, slug = ident(path)
    days, trades = defaultdict(lambda: [0.0, 0, 0, 0.0, 0.0]), []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if not r["Type"].startswith("Exit"):
                continue
            q = float(r["Size (qty)"])
            pnl = float(r["Net PnL USD"]) / q - float(r["Commission USD"] or 0) / q - COST[mkt]
            d = r["Date and time"][:10]
            if d > END:
                continue
            a = days[d]
            a[0] += pnl; a[1] += 1; a[2] += pnl > 0
            a[3 if pnl > 0 else 4] += abs(pnl)
            trades.append(round(pnl, 2))
    ds = sorted(days)
    first = min(first or ds[0], ds[0]); last = max(last or ds[-1], ds[-1])
    # each day: date, net P&L, trades, winning trades, gross win, gross loss (1 contract, after costs)
    out.append({"name": name, "mkt": mkt, "slug": slug,
                "days": [[d, round(days[d][0], 2), days[d][1], days[d][2], round(days[d][3], 2), round(days[d][4], 2)] for d in ds]})
out.sort(key=lambda s: (s["mkt"], s["name"]))
json.dump({"from": first, "to": last, "freeze": FREEZE, "strategies": out},
          open(os.path.join(os.path.dirname(__file__), "data", "tracker.json"), "w"), separators=(",", ":"))
for s in out:
    n = sum(x[2] for x in s["days"]); w = sum(x[3] for x in s["days"])
    print(f'{s["name"]:24} {n:4} wr {100*w/n:5.1f} net {sum(x[1] for x in s["days"]):9.2f} days {len(s["days"])}')
print(first, last)
