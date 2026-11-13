"""Refresh _src/board_data.json for the homepage market board.

Run hourly by .github/workflows/board.yml. Prices: Yahoo Finance chart API
(delayed; the full-size contract is used for each micro, same price).
Events: Forex Factory weekly calendar, US high-impact only.
If a source fails, the previous data for that part is kept.
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "board_data.json")
UA = {"User-Agent": "Mozilla/5.0 (badredge board refresh)"}
# micro, name, group, source symbol
MARKETS = [
    ("MNQ", "Micro Nasdaq-100", "Index", "NQ=F"),
    ("MES", "Micro S&P 500", "Index", "ES=F"),
    ("MYM", "Micro Dow", "Index", "YM=F"),
    ("M2K", "Micro Russell 2000", "Index", "RTY=F"),
    ("MGC", "Micro Gold", "Metal", "GC=F"),
    ("SIL", "Micro Silver", "Metal", "SI=F"),
    ("PL", "Platinum", "Metal", "PL=F"),
    ("MCL", "Micro Crude", "Energy", "CL=F"),
    ("MHG", "Micro Copper", "Metal", "HG=F"),
    ("M6E", "Micro EUR/USD", "FX", "6E=F"),
]


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def closes(sym, interval, rng):
    d = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval={interval}&range={rng}")
    q = d["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    return [c for c in q if c is not None]


def market_rows():
    rows = []
    for micro, name, grp, sym in MARKETS:
        hourly = closes(sym, "1h", "5d")[-48:]
        daily = closes(sym, "1d", "10d")
        last = hourly[-1]
        prev = daily[-2] if len(daily) > 1 else hourly[0]
        nd = 4 if last < 10 else 2
        rows.append([micro, name, grp, round(last, nd), round((last / prev - 1) * 100, 3),
                     [round(c, nd) for c in hourly]])
    return rows


def event_rows():
    ev = get("https://nfs.faireconomy.media/ff_calendar_thisweek.json")
    out = []
    for e in ev:
        if e.get("country") != "USD" or e.get("impact") != "High":
            continue
        t = datetime.fromisoformat(e["date"]).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out.append([t, e["title"], "", e.get("forecast") or "", e.get("previous") or "", "USD"])
    return sorted(out)


def main():
    old = json.load(open(PATH))
    new = dict(old)
    try:
        new["markets"] = market_rows()
        new["asof"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception as e:  # keep last good prices
        print("prices failed:", e, file=sys.stderr)
    try:
        rows = event_rows()
        if rows:
            new["events"] = rows
    except Exception as e:
        print("events failed:", e, file=sys.stderr)
    if new["markets"] == old["markets"] and new["events"] == old["events"]:
        print("no change"); return
    with open(PATH, "w") as f:
        json.dump(new, f, separators=(",", ":"))
    print("updated", new["asof"])


if __name__ == "__main__":
    main()
