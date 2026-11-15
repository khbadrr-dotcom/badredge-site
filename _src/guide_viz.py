"""Inline SVG diagrams for the beginner guides.

Colours come only from CSS classes (gv-*) that use site tokens, so both themes work.
Numbers match the worked examples in each guide's text. Price charts are illustrations, not market data.
"""

W = 560  # viewBox width; kept narrow so labels stay readable on phones


def _fig(svg, title, sub, h, label):
    return (f'<figure class="viz gv-fig"><figcaption><b>{title}</b>{f"<span>{sub}</span>" if sub else ""}</figcaption>'
            f'<svg class="gv" viewBox="0 0 {W} {h}" role="img" aria-label="{label}">{svg}</svg></figure>')


def _t(x, y, s, cls="gv-t", anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def _line(x1, y1, x2, y2, cls):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}"/>'


class _Scale:
    def __init__(self, x0, x1, y0, y1, vmin, vmax, n):
        self.x0, self.x1, self.y0, self.y1, self.vmin, self.vmax, self.n = x0, x1, y0, y1, vmin, vmax, n

    def x(self, i):  # slot centre for i in 0..n-1
        return self.x0 + (i + 0.5) * (self.x1 - self.x0) / self.n

    def y(self, v):
        return self.y1 - (v - self.vmin) / (self.vmax - self.vmin) * (self.y1 - self.y0)

    @property
    def slot(self):
        return (self.x1 - self.x0) / self.n


def _candles(sc, cs, hi_idx=None):
    out = []
    bw = sc.slot * 0.56
    for i, (o, h, l, c) in enumerate(cs):
        cls = "gv-up" if c >= o else "gv-dn"
        if hi_idx is not None and i in hi_idx:
            cls += " gv-hi"
        x = sc.x(i)
        top, bot = sc.y(max(o, c)), sc.y(min(o, c))
        out.append(f'<g class="{cls}">{_line(x, sc.y(h), x, sc.y(l), "gv-wick")}'
                   f'<rect x="{x - bw / 2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{max(bot - top, 1.5):.1f}" rx="1.5" class="gv-body"/></g>')
    return "".join(out)


def _bracket(sc, slot_edge, hi, lo, text_v, text):
    """Measured height drawn on a gap between candles, with end caps so it doesn't read as a wick."""
    bx = sc.x0 + slot_edge * sc.slot
    return (_line(bx, sc.y(hi), bx, sc.y(lo), "gv-brk") + _line(bx - 5, sc.y(hi), bx + 5, sc.y(hi), "gv-brk")
            + _line(bx - 5, sc.y(lo), bx + 5, sc.y(lo), "gv-brk") + _t(bx + 7, sc.y(text_v), text, "gv-s", "start"))


def _time_axis(sc, labels, y):
    return "".join(_t(sc.x(i) - sc.slot / 2, y, s, "gv-s", "middle") for i, s in labels)


# ---------------------------------------------------------------- trailing drawdown

def dd_trailing():
    closes = [50000, 50600, 50200, 51300, 52100, 52600, 51800, 52900]
    floors = [48000, 48600, 48600, 49300, 50000, 50000, 50000, 50000]
    n = len(closes)
    sc = _Scale(64, 540, 28, 250, 47600, 53400, n)
    grid = "".join(_line(64, sc.y(v), 540, sc.y(v), "gv-grid") + _t(56, sc.y(v) + 4, f"${v // 1000}k", "gv-s", "end")
                   for v in range(48000, 53001, 1000))
    # cushion band between balance and floor (floor drawn as steps)
    top = " ".join(f"{sc.x(i):.1f},{sc.y(c):.1f}" for i, c in enumerate(closes))
    fl_pts = []
    for i, f in enumerate(floors):
        fl_pts.append((sc.x(i), sc.y(f)))
        if i + 1 < n:
            fl_pts.append((sc.x(i + 1), sc.y(f)))
    band = top + " " + " ".join(f"{x:.1f},{y:.1f}" for x, y in reversed(fl_pts))
    floor_path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in fl_pts)
    bal = "M" + " L".join(f"{sc.x(i):.1f},{sc.y(c):.1f}" for i, c in enumerate(closes))
    dots = "".join(f'<circle cx="{sc.x(i):.1f}" cy="{sc.y(c):.1f}" r="3.6" class="gv-dot"/>' for i, c in enumerate(closes))
    xl = "".join(_t(sc.x(i), 272, "Start" if i == 0 else f"Day {i}", "gv-s", "middle") for i in range(n))
    lock_x, lock_y = sc.x(4), sc.y(50000)
    svg = (grid + f'<polygon points="{band}" class="gv-band"/>'
           + f'<path d="{floor_path}" class="gv-floor"/>' + f'<path d="{bal}" class="gv-bal"/>' + dots
           + f'<circle cx="{lock_x:.1f}" cy="{lock_y:.1f}" r="5" class="gv-lock"/>'
           + _t(lock_x + 10, lock_y + 20, "Floor locks at $50,000", "gv-t gv-lt")
           + _t(sc.x(2), sc.y(49450) + 4, "Cushion", "gv-t gv-gt", "middle")
           + xl)
    legend = ('<span class="legend"><span class="lg"><i class="lg-bal"></i>Closing balance</span>'
              '<span class="lg"><i class="lg-floor"></i>Floor (max loss level)</span></span>')
    return _fig(svg, "End-of-day trailing: the floor follows your best close",
                "Same numbers as the table above: $50,000 account, $2,000 max loss." + legend, 286,
                "Chart: balance rises from 50,000 to 52,900 while the floor trails 2,000 below the highest close and locks at 50,000 on day 4.")


def dd_intraday():
    # one trade during one session: balance path and the two floor rules
    path = [0, 150, 380, 520, 800, 640, 420, 300, 120, 0]
    n = len(path)
    sc = _Scale(64, 540, 30, 224, -2300, 1100, n)
    to = lambda v: sc.y(v)
    bal = "M" + " L".join(f"{sc.x(i):.1f},{to(v):.1f}" for i, v in enumerate(path))
    run = 0
    fl = []
    for i, v in enumerate(path):
        run = max(run, v)
        fl.append((sc.x(i), to(run - 2000)))
    fl_path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in fl)
    grid = "".join(_line(64, to(v), 540, to(v), "gv-grid") + _t(56, to(v) + 4, lab, "gv-s", "end")
                   for v, lab in [(800, "+$800"), (0, "$50k"), (-1200, "$48.8k"), (-2000, "$48k")])
    pk = sc.x(4)
    svg = (grid + f'<path d="{bal}" class="gv-bal"/>'
           + _line(sc.x(0), to(-2000), sc.x(n - 1), to(-2000), "gv-floor-eod")
           + f'<path d="{fl_path}" class="gv-floor"/>'
           + f'<circle cx="{pk:.1f}" cy="{to(800):.1f}" r="4" class="gv-dot"/>'
           + _t(pk, to(800) - 10, "Open profit +$800", "gv-t gv-gt", "middle")
           + _t(sc.x(n - 1), to(0) + 20, "Trade closes flat", "gv-s", "end")
           + _t(sc.x(5), to(-1200) - 9, "Intraday floor: up $800, stays there", "gv-t gv-lt", "start")
           + _t(sc.x(5), to(-2000) + 18, "End-of-day floor: unchanged", "gv-s", "start")
           + _t(sc.x(0), 248, "Trade opens", "gv-s", "start") + _t(sc.x(n - 1), 248, "Same session", "gv-s", "end"))
    return _fig(svg, "Intraday trailing: open profit moves the floor",
                "A trade runs to +$800 and comes back to breakeven. The account made nothing, but the cushion lost $800.", 258,
                "Chart: a trade rises to plus 800 dollars and falls back to zero; the intraday floor rises 800 dollars and stays, the end-of-day floor does not move.")


# ---------------------------------------------------------------- evaluation math

def math_race():
    rows = [(1, 120, 180), (3, 360, 540), (6, 720, 1080)]
    x0, x1 = 96, 540
    lo, hi = -2000, 3000
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    out = [_t(X(lo), 26, "Max loss −$2,000", "gv-s gv-dt", "start"), _t(X(hi), 26, "Target +$3,000", "gv-s gv-lt", "end"),
           _t(X(0), 26, "Start", "gv-s", "middle")]
    y = 64
    for n, loss, win in rows:
        out.append(_t(86, y + 4, f"{n} contract{'s' if n > 1 else ''}", "gv-t", "end"))
        out.append(f'<rect x="{X(lo):.1f}" y="{y - 9}" width="{X(0) - X(lo):.1f}" height="18" rx="9" class="gv-trk-d"/>')
        out.append(f'<rect x="{X(0):.1f}" y="{y - 9}" width="{X(hi) - X(0):.1f}" height="18" rx="9" class="gv-trk-u"/>')
        v = -loss
        while v > lo:
            out.append(_line(X(v), y - 7, X(v), y + 7, "gv-tick-d"))
            v -= loss
        v = win
        while v < hi:
            out.append(_line(X(v), y - 7, X(v), y + 7, "gv-tick-u"))
            v += win
        out.append(_line(X(0), y - 13, X(0), y + 13, "gv-zero"))
        out.append(_t(X(lo) + 2, y + 26, f"{2000 / loss:.1f} average losses", "gv-s gv-dt", "start"))
        out.append(_t(X(hi) - 2, y + 26, f"{3000 / win:.1f} average wins", "gv-s gv-lt", "end"))
        y += 66
    return _fig("".join(out), "Each tick is one average trade",
                "Wins $180 and losses $120 per contract. More contracts means fewer steps to either end of the race.", 238,
                "Diagram: at 1 contract about 17 losses or 17 wins reach either end; at 3 contracts about 5.6; at 6 contracts about 2.8.")


def math_sweet_spot():
    x0, x1, y0, y1 = 40, 540, 30, 196
    pts = []
    for k in range(101):
        s = k / 100
        v = (s ** 1.15) * (1 - s) ** 1.6
        pts.append((s, v))
    vmax = max(v for _, v in pts)
    path = "M" + " L".join(f"{x0 + s * (x1 - x0):.1f},{y1 - v / vmax * (y1 - y0 - 10):.1f}" for s, v in pts)
    area = path + f" L{x1},{y1} L{x0},{y1} Z"
    peak = max(pts, key=lambda p: p[1])[0]
    px = x0 + peak * (x1 - x0)
    svg = (f'<path d="{area}" class="gv-area"/><path d="{path}" class="gv-bal"/>'
           + _line(x0, y1, x1, y1, "gv-axis")
           + f'<rect x="{px - 40:.1f}" y="{y0 - 6}" width="80" height="{y1 - y0 + 6}" rx="8" class="gv-zone-t"/>'
           + _t(px, y0 + 10, "Sweet spot", "gv-t gv-lt", "middle")
           + _t(x0 + 6, y0 + 22, "Too small:", "gv-t", "start") + _t(x0 + 6, y0 + 40, "stalls", "gv-s", "start")
           + _t(x1 - 6, y0 + 22, "Too big:", "gv-t", "end") + _t(x1 - 6, y0 + 40, "a streak ends it", "gv-s", "end")
           + _t(x0, y1 + 20, "Fewer contracts", "gv-s", "start") + _t(x1, y1 + 20, "More contracts", "gv-s", "end")
           + _t(x0 - 8, (y0 + y1) / 2, "Pass odds", "gv-s", "middle").replace("<text", f'<text transform="rotate(-90 {x0 - 8} {(y0 + y1) / 2})"', 1))
    return _fig(svg, "The shape to look for", "An illustration, not data. A simulator finds where the peak sits for your own numbers.", 226,
                "Illustration: pass odds rise with size, peak in the middle, then fall as size gets too big.")


# ---------------------------------------------------------------- contract sizing

def size_same_move():
    cushion = 2000
    x0, x1 = 120, 540
    X = lambda v: x0 + v / cushion * (x1 - x0)
    out = [_t(x1, 24, "Your cushion: $2,000", "gv-s", "end")]
    rows = [("MGC (micro)", 50, "40 moves like this fit in the cushion"), ("GC (full)", 500, "Only 4 moves like this fit")]
    y = 54
    for name, v, note in rows:
        out.append(_t(108, y + 5, name, "gv-t", "end"))
        out.append(f'<rect x="{x0}" y="{y - 11}" width="{x1 - x0}" height="22" rx="11" class="gv-track"/>')
        k = 0
        while (k + 1) * v <= cushion and k < 40:
            out.append(f'<rect x="{X(k * v) + 0.8:.1f}" y="{y - 11}" width="{max(X(v) - X(0) - 1.6, 1.2):.1f}" height="22" rx="{3 if v > 100 else 1}" class="gv-seg{" gv-seg-1" if k == 0 else ""}"/>')
            k += 1
        out.append(_t(x0, y + 32, f"5 points = ${v}", "gv-t gv-gt", "start"))
        out.append(_t(x1, y + 32, note, "gv-s", "end"))
        y += 78
    return _fig("".join(out), "The same 5-point gold move, two contracts",
                "MGC pays $10 a point, GC $100 a point. Each block is one 5-point move against you.", 190,
                "Diagram: a 2,000 dollar cushion holds 40 five-point moves on micro gold but only 4 on full-size gold.")


def size_ladder():
    x0, x1, y0, y1 = 56, 540, 26, 214
    bmax, cmax = 4000, 8
    X = lambda b: x0 + b / bmax * (x1 - x0)
    Y = lambda c: y1 - c / cmax * (y1 - y0)

    def steps(block):
        pts, b = [], 0
        prev = None
        for b in range(0, bmax + 1, 10):
            c = max(1, b // block)
            if prev is not None and c != prev:
                pts.append((X(b), Y(prev)))
            pts.append((X(b), Y(c)))
            prev = c
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

    grid = "".join(_line(x0, Y(c), x1, Y(c), "gv-grid") + _t(x0 - 8, Y(c) + 4, str(c), "gv-s", "end") for c in range(0, cmax + 1, 2))
    xt = "".join(_t(X(b), y1 + 18, f"${b:,}", "gv-s", "middle") for b in range(0, bmax + 1, 1000))
    marks = "".join(f'<circle cx="{X(b):.1f}" cy="{Y(max(1, b // 700)):.1f}" r="4" class="gv-dot"/>' for b in (1200, 2000, 3500))
    svg = (grid + f'<path d="{steps(500)}" class="gv-floor"/>' + f'<path d="{steps(700)}" class="gv-bal"/>' + marks
           + _t(X(3500) - 8, Y(5) - 9, "$3,500 buffer → 5", "gv-t gv-gt", "end")
           + _t(X(1200), Y(1) + 22, "$1,200 → 1", "gv-t gv-gt", "middle")
           + _t(x1, y1 + 36, "Buffer (balance minus floor)", "gv-s", "end") + _t(x0 - 8, y0 - 10, "Contracts", "gv-s", "start"))
    legend = ('<span class="legend"><span class="lg"><i class="lg-bal"></i>Block $700</span>'
              '<span class="lg"><i class="lg-floor"></i>Block $500</span></span>')
    return _fig(svg, "The buffer ladder: size follows the cushion",
                "Contracts = buffer ÷ block, rounded down, minimum 1. Losses shrink size on their own." + legend, 258,
                "Step chart: contracts rise one step for every 700 dollars of buffer (gold) or every 500 dollars (teal).")


# ---------------------------------------------------------------- opening range breakout

ORB_RANGE = [(21000, 21022, 20992, 21018), (21018, 21030, 21005, 21008), (21008, 21015, 20990, 21012)]
ORB_BREAK = ORB_RANGE + [(21012, 21024, 21002, 21020), (21020, 21028, 21010, 21014), (21014, 21026, 21008, 21024),
                         (21024, 21046, 21020, 21042), (21042, 21058, 21036, 21054), (21054, 21062, 21044, 21048),
                         (21048, 21068, 21045, 21064), (21064, 21072, 21055, 21060)]
ORB_FAIL = ORB_RANGE + [(21012, 21022, 21004, 21018), (21018, 21038, 21016, 21034), (21034, 21036, 21012, 21016),
                        (21016, 21020, 20996, 21000), (21000, 21004, 20978, 20982), (20982, 20994, 20975, 20990),
                        (20990, 21000, 20984, 20996), (20996, 21002, 20986, 20992)]
ORB_TIMES = [(0, "9:30"), (3, "9:45"), (6, "10:00"), (9, "10:15")]


def _range_chart(cs, n_range, vmin, vmax, hi_lab, lo_lab, zone_lab, times, notes, h=290, hi_idx=None, ext=None, hi_right=False):
    sc = _Scale(20, 540, 34, h - 44, vmin, vmax, len(cs))
    hi = max(c[1] for c in cs[:n_range])
    lo = min(c[2] for c in cs[:n_range])
    zx1 = sc.x0 + n_range * sc.slot
    out = [f'<rect x="{sc.x0:.1f}" y="{sc.y(hi):.1f}" width="{zx1 - sc.x0:.1f}" height="{sc.y(lo) - sc.y(hi):.1f}" rx="6" class="gv-zone"/>',
           _line(sc.x0, sc.y(hi), sc.x1, sc.y(hi), "gv-lvl"), _line(sc.x0, sc.y(lo), sc.x1, sc.y(lo), "gv-lvl"),
           _t(sc.x0 + 4, sc.y(hi) - 22, zone_lab, "gv-t gv-gt", "start"),
           (_t(sc.x1, sc.y(hi) - 6, hi_lab, "gv-s gv-gt", "end") if hi_right else _t(zx1 + 6, sc.y(hi) - 6, hi_lab, "gv-s gv-gt", "start")), _t(zx1 + 6, sc.y(lo) + 15, lo_lab, "gv-s gv-gt", "start")]
    if ext:
        v, lab = ext
        out.append(_line(sc.x0, sc.y(v), sc.x1, sc.y(v), "gv-lvl-t"))
        out.append(_t(sc.x0 + 4, sc.y(v) - 6, lab, "gv-s gv-lt", "start"))
    out.append(_line(zx1, 30, zx1, h - 44, "gv-sep"))
    out.append(_candles(sc, cs, hi_idx))
    out.append(_line(sc.x0, h - 40, sc.x1, h - 40, "gv-axis"))
    out.append(_time_axis(sc, times, h - 22))
    for i, v, text, cls, anchor in notes:
        out.append(_t(sc.x(i), sc.y(v), text, cls, anchor))
    return "".join(out), sc


def orb_breakout():
    svg, sc = _range_chart(ORB_BREAK, 3, 20975, 21085, "Range high", "Range low", "Opening range: first 15 minutes",
                           ORB_TIMES, [(6, 21079, "Breakout: a candle closes above the high", "gv-t gv-lt", "middle")],
                           hi_idx={6})
    svg += f'<circle cx="{sc.x(6):.1f}" cy="{sc.y(21042):.1f}" r="4.5" class="gv-mark"/>' + _line(sc.x(6), sc.y(21077), sc.x(6), sc.y(21049), "gv-lead")
    # range height bracket
    svg += _bracket(sc, 5, 21030, 20990, 20995, "40 points")
    return _fig(svg, "An opening range breakout, step by step",
                "5-minute candles after the New York open (9:30 ET). An illustration, not a real session.", 290,
                "Candle chart: the first three 5-minute candles set a 40-point range; later a candle closes above the range high.")


def orb_false():
    svg, sc = _range_chart(ORB_FAIL, 3, 20955, 21065, "Range high", "Range low", "Opening range",
                           ORB_TIMES, [(4, 21050, "Closes above the high…", "gv-t gv-lt", "middle"),
                                       (7, 20961, "…then falls back through the low", "gv-t gv-dt", "middle")],
                           hi_idx={4, 5}, hi_right=True)
    return _fig(svg, "A false breakout", "Price closes outside the range, then returns inside. This happens often, which is why the stop and the rules matter more than the signal.", 290,
                "Candle chart: a candle closes above the range high, the next candle falls back inside, and price later closes below the range low.")


# ---------------------------------------------------------------- initial balance

IB_DAY = [(2650, 2658, 2646, 2656), (2656, 2662, 2652, 2654), (2654, 2657, 2644, 2647), (2647, 2655, 2645, 2653),
          (2653, 2659, 2650, 2657), (2657, 2661, 2652, 2655), (2655, 2665, 2654, 2664), (2664, 2672, 2662, 2670),
          (2670, 2676, 2666, 2668), (2668, 2678, 2667, 2676), (2676, 2682, 2671, 2674), (2674, 2679, 2669, 2677)]


def ib_chart():
    svg, sc = _range_chart(IB_DAY, 4, 2638, 2690, "IB high", "IB low", "Initial balance: first hour",
                           [(0, "Open"), (4, "+1h"), (8, "+2h")],
                           [(8.5, 2685, "Range extension above the IB", "gv-t gv-lt", "middle")],
                           h=300, ext=(2680, "IB high + 1× IB range"))
    svg += _bracket(sc, 5, 2662, 2644, 2645.6, "IB range 18 pts")
    return _fig(svg, "The initial balance and a range extension",
                "15-minute gold candles. The first four set the IB; the day then extends above it. An illustration, not a real session.", 300,
                "Candle chart: the first hour sets an 18-point initial balance; later candles move above the IB high toward the 1x extension line.")


def ib_day_types():
    panels = [("Stays inside", [0.5, 0.2, 0.8, 0.35, 0.5, 0.3, 0.7, 0.45, 0.6, 0.4]),
              ("Extends one side", [0.5, 0.2, 0.8, 0.35, 0.6, 0.85, 1.1, 1.25, 1.5, 1.45]),
              ("Extends both sides", [0.5, 0.2, 0.8, 0.35, 0.5, -0.15, -0.3, 0.4, 1.1, 1.3])]
    pw, gap, top, ph = 170, 15, 40, 130
    out = []
    for k, (name, path) in enumerate(panels):
        x0 = 10 + k * (pw + gap)
        Y = lambda v: top + ph - (v + 0.6) / 2.4 * ph
        ib_hi, ib_lo = Y(0.8), Y(0.2)
        ibx = x0 + pw * 0.3
        out.append(f'<rect x="{x0}" y="{top - 8}" width="{pw}" height="{ph + 16}" rx="10" class="gv-panel"/>')
        out.append(f'<rect x="{x0 + 6}" y="{ib_hi:.1f}" width="{ibx - x0 - 6:.1f}" height="{ib_lo - ib_hi:.1f}" rx="4" class="gv-zone"/>')
        out.append(_line(x0 + 6, ib_hi, x0 + pw - 6, ib_hi, "gv-lvl"))
        out.append(_line(x0 + 6, ib_lo, x0 + pw - 6, ib_lo, "gv-lvl"))
        pts = " L".join(f"{x0 + 10 + i * (pw - 20) / (len(path) - 1):.1f},{Y(v):.1f}" for i, v in enumerate(path))
        out.append(f'<path d="M{pts}" class="gv-bal"/>')
        out.append(_t(x0 + pw / 2, top + ph + 34, name, "gv-t", "middle"))
    out.append(_t(10, 22, "Shaded box = first hour. Lines = IB high and low.", "gv-s", "start"))
    return _fig("".join(out), "Three ways a day can treat the IB", "Simplified price paths, for reading the idea only.", 214,
                "Three small panels: price staying inside the initial balance, extending above it, and extending below then above it.")
