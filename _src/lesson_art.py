"""Small static drawings for the homepage lesson card, one per lesson.

Each drawing is a quiet SVG (360 x 120) that shows the idea of its lesson with the
site's colour code: gold = the plan / main line, teal = gain or the right move,
red = loss or risk, faint = context. Classes are styled in assets/site.css (.la-*).
No motion. Order matches lessons.LESSONS.
"""
import random

W, H = 360, 120


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pts(P):
    return " ".join(f"{_f(x)},{_f(y)}" for x, y in P)


def line(x1, y1, x2, y2, c="f", dash=False):
    d = ' stroke-dasharray="4 4"' if dash else ""
    return f'<line class="la-{c}" x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}"{d}/>'


def poly(P, c="g", dash=False):
    d = ' stroke-dasharray="4 4"' if dash else ""
    return f'<polyline class="la-{c}" points="{pts(P)}"{d}/>'


def rect(x, y, w, h, c="g", r=2):
    if h < 0:
        y, h = y + h, -h
    return f'<rect class="la-{c}f" x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" rx="{r}"/>'


def dot(x, y, c="g", r=3):
    return f'<circle class="la-{c}d" cx="{_f(x)}" cy="{_f(y)}" r="{_f(r)}"/>'


def ring(x, y, c="g", r=3):
    return f'<circle class="la-{c}" cx="{_f(x)}" cy="{_f(y)}" r="{_f(r)}" fill="none"/>'


def txt(x, y, s, c="l", anchor="start"):
    return f'<text class="la-{c}" x="{_f(x)}" y="{_f(y)}" text-anchor="{anchor}">{s}</text>'


def walk(seed, n, x0, x1, y0, drift, vol, lo=10, hi=110):
    rnd, P, y = random.Random(seed), [], y0
    for k in range(n):
        x = x0 + (x1 - x0) * k / (n - 1)
        P.append((x, y))
        y = min(max(y - drift + rnd.gauss(0, vol), lo), hi)
    return P


BASE = 64  # zero line for bar drawings


def winloss(wins, losses, lab_w="", lab_l=""):
    """Gains above the line in teal, losses below in red, to scale."""
    s, x, k = line(16, BASE, 344, BASE), 30, 13
    for v in wins:
        s += rect(x, BASE, 18, -v * k, "t"); x += 26
    x += 14
    for v in losses:
        s += rect(x, BASE, 18, v * k, "r"); x += 26
    s += txt(30, 14, lab_w) + txt(344, 114, lab_l, anchor="end")
    return s


def recover():
    s = line(16, BASE, 344, BASE)
    for j, (dd, up) in enumerate([(10, 11.1), (25, 33.3), (50, 100)]):
        x = 46 + j * 108
        s += rect(x, BASE, 22, dd * .9, "r") + rect(x + 28, BASE, 22, -up * .5, "t")
        s += txt(x + 11, BASE + dd * .9 + 11, f"−{dd}%", anchor="middle")
        s += txt(x + 39, BASE - up * .5 - 5, f"+{_f(up)}%", anchor="middle")
    return s


def stop_size(stop_pts=15, n=4, x0=24, x1=200, label=True):
    entry, stop = 40, 40 + stop_pts * 3.2
    s = line(x0, entry, x1, entry, "g") + line(x0, stop, x1, stop, "r", dash=True)
    s += line(x1 + 10, entry, x1 + 10, stop, "f") + line(x1 + 6, entry, x1 + 14, entry, "f") + line(x1 + 6, stop, x1 + 14, stop, "f")
    s += txt(x1 + 18, (entry + stop) / 2 + 3, f"{stop_pts} pts")
    if label:
        s += txt(x0, entry - 8, "entry") + txt(x0, stop + 14, "stop", "lr")
    bx = x1 + 70
    for k in range(n):
        s += rect(bx + (k % 5) * 14, 96 - (k // 5) * 14, 10, 10, "g")
    return s


def trail(mode="intraday"):
    P = walk(5, 40, 20, 340, 80, .9, 4.5, 24, 104)
    s = poly(P, "g")
    floor, F, peak = None, [], 999
    for x, y in P:
        peak = min(peak, y)
        f = peak + 30
        F.append((x, f))
    s += poly(F, "r", dash=True) + txt(340, 116, "floor follows the peak", "lr", "end")
    if mode == "both":
        E, last = [], F[0][1]
        for k, (x, f) in enumerate(F):
            if k % 10 == 0:
                last = P[k][1] + 30 if P[k][1] + 30 < last else last
            E.append((x, last))
        s += poly(E, "t", dash=True)
        s = s.replace(txt(340, 116, "floor follows the peak", "lr", "end"), "")
        s += txt(20, 14, "intraday floor", "lr") + txt(130, 14, "end-of-day floor", "lt")
    return s


def journal(rows=("setup", "entry", "stop", "target", "why")):
    s = f'<rect class="la-f" x="90" y="8" width="180" height="104" rx="6" fill="none"/>'
    for k, r in enumerate(rows):
        y = 26 + k * 19
        s += txt(106, y + 3, r) + line(160, y, 252, y)
        s += f'<path class="la-t" d="M{256},{y - 1} l3,3 l6,-7" fill="none"/>' if k < len(rows) else ""
    return s


def escalate():
    s = line(16, 30, 344, 30)
    sizes = [1, 1.6, 2.3, 3.1]
    x = 40
    for k, v in enumerate(sizes):
        s += rect(x, 30, 30, v * 22, "r" if k == 0 else "rr"); x += 44 + (40 if k == 0 else 0)
    s += line(108, 14, 108, 112, "t") + txt(114, 22, "pause", "lt")
    s += txt(40, 22, "−1R") + txt(344, 114, "bigger size, worse entries", anchor="end")
    return s


def curves(a_drop, b_drop, la, lb, ca="r", cb="g", up=False, steps=10):
    s = ""
    for drop, lab, c in ((a_drop, la, ca), (b_drop, lb, cb)):
        P, y = [], 24
        for k in range(steps + 1):
            P.append((24 + k * 25, y)); y += drop * (1 if not up else -1)
        s += poly(P, c) + dot(*P[-1], c=c, r=2.5) + txt(P[-1][0] + 8, P[-1][1] + 4, lab, "l" + c)
    return s


def hbars(items):
    s, mx = "", max(v for _, v, _ in items)
    for k, (lab, v, c) in enumerate(items):
        y = 12 + k * 26
        s += txt(16, y + 12, lab) + rect(110, y, max(4, 210 * v / mx), 14, c)
        s += txt(110 + max(4, 210 * v / mx) + 6, y + 12, f"${_f(v)}")
    return s


def rscale(marks=((-1, "r"), (2, "t"), (.5, "t"), (-1, "r"), (3, "t"))):
    s, x0, u = line(20, 70, 340, 70), 100, 52
    for r in range(-1, 5):
        x = x0 + r * u
        s += line(x, 64, x, 76) + txt(x, 94, ("+" if r > 0 else "") + f"{r}R", anchor="middle")
    for k, (r, c) in enumerate(marks):
        s += dot(x0 + r * u, 52 - k * 8, c, 3.5)
    return s


def moved_stop():
    s = line(24, 36, 230, 36, "g") + txt(24, 28, "entry")
    s += line(24, 66, 230, 66, "g", dash=True) + txt(24, 80, "planned stop")
    s += line(24, 104, 230, 104, "r", dash=True) + txt(24, 116, "moved stop", "lr")
    s += f'<path class="la-r" d="M250,70 V98 M245,92 l5,7 l5,-7" fill="none"/>' + txt(262, 90, "more risk,", "lr") + txt(262, 102, "no new plan", "lr")
    return s


def splits(rows):
    s = ""
    for k, (lab, p) in enumerate(rows):
        y = 18 + k * 32
        s += txt(16, y + 11, lab) + rect(80, y, 240 * p, 14, "t") + rect(80 + 240 * p, y, 240 * (1 - p), 14, "q")
        s += line(80 + 240 * p, y - 4, 80 + 240 * p, y + 18, "g") + txt(328, y + 11, f"{round(p * 100)}%")
    return s


def gap():
    s = line(20, 54, 340, 54, "r", dash=True) + txt(340, 48, "stop", "lr", "end")
    for k, (o, c) in enumerate([(30, 34), (34, 30), (30, 38), (38, 42)]):
        x = 60 + k * 34
        s += line(x + 6, o - 6, x + 6, c + 6, "f") + rect(x, min(o, c), 12, abs(c - o) + 2, "t" if c < o else "q")
    s += line(222, 72, 222, 104, "f") + rect(216, 76, 12, 22, "r")
    s += rect(240, 54, 70, 22, "rr", 3) + txt(246, 69, "slippage", "lr")
    return s


def blocks():
    s = rect(30, 30, 90, 60, "g", 4) + txt(75, 108, "1 GC · $1,500", anchor="middle")
    for k in range(10):
        s += rect(180 + (k % 5) * 30, 34 + (k // 5) * 30, 22, 22, "g" if k < 3 else "q")
    s += txt(240, 108, "MGC · $150 each", anchor="middle")
    return s


def budget(rows=((4, "$500 a trade"), (10, "$200 a trade"))):
    s = ""
    for k, (n, lab) in enumerate(rows):
        y = 26 + k * 44
        w = 300 / n
        for j in range(n):
            s += rect(30 + j * w + 1, y, w - 3, 16, "r" if j == n - 1 else "rr")
        s += txt(30, y - 6, lab) + txt(330, y - 6, f"{n} losses", anchor="end")
    return s


def tags():
    rnd, s = random.Random(3), ""
    for r in range(4):
        for c in range(12):
            bad = c in (7, 8) and r in (1, 2)
            col = "r" if bad else ("t" if rnd.random() < .45 else "q")
            s += rect(40 + c * 24, 14 + r * 22, 16, 14, col)
    s += txt(40, 112, "setup × hour of day") + txt(232, 112, "one cluster", "lr")
    return s


def average_down():
    P = [(20, 30), (80, 46), (120, 40), (170, 64), (210, 58), (260, 86), (340, 104)]
    s = poly(P, "f")
    for (x, y), r in zip([(80, 46), (170, 64), (260, 86)], (3, 5, 7)):
        s += dot(x, y, "r", r)
    s += txt(200, 22, "size grows as the idea fails", "lr")
    return s


def correlated():
    a = walk(11, 30, 20, 340, 60, .3, 5, 20, 100)
    b = [(x, y + 6 + random.Random(int(x)).gauss(0, 1.5)) for x, y in a]
    return poly(a, "g") + poly(b, "t") + txt(340, a[-1][1] - 8, "NQ", anchor="end") + txt(340, b[-1][1] + 16, "ES", "lt", "end")


def _g(inner, dx):
    return f'<g transform="translate({dx} 0)">{inner}</g>'


def tradeoff():
    s = ""
    for k, (pts_, n) in enumerate(((20, 10), (40, 5))):
        x0, stop = 20 + k * 175, 24 + pts_ * 1.5
        s += line(x0, 24, x0 + 70, 24, "g") + line(x0, stop, x0 + 70, stop, "r", dash=True)
        s += line(x0 + 80, 24, x0 + 80, stop, "f") + txt(x0 + 86, (24 + stop) / 2 + 3, f"{pts_} pts")
        for j in range(n):
            s += rect(x0 + (j % 5) * 14, 108 - (j // 5) * 14, 10, 10, "g")
        s += txt(x0 + 86, 116, f"{n} contracts")
    return s


def costs():
    s = rect(30, 44, 240, 26, "t", 3) + rect(270, 44, 60, 26, "r", 3)
    return s + txt(30, 36, "$25 a trade before costs") + txt(300, 90, "$5 costs", "lr", "middle") + txt(150, 90, "what is left", "lt", "middle")


def consistency():
    vals = [6, 9, 4, 20, 8, 11, 7, 10, 9]
    s = line(16, 104, 344, 104)
    for k, v in enumerate(vals):
        s += rect(30 + k * 34, 104, 20, -v * 4, "g" if v == 20 else "q")
    s += txt(30 + 3 * 34 + 10, 14, "best day ≤ 40% of total", "lg", "middle")
    return s


def excursion():
    P = [(30, 60), (60, 72), (90, 84), (120, 70), (160, 48), (200, 30), (240, 40), (280, 52), (320, 46)]
    s = line(30, 60, 330, 60, "g", dash=True) + poly(P, "f")
    s += line(30, 84, 330, 84, "r", dash=True) + txt(334, 88, "MAE", "lr", "end")
    s += line(30, 30, 330, 30, "t", dash=True) + txt(334, 24, "MFE", "lt", "end")
    s += txt(30, 54, "entry")
    return s


def oneline():
    rnd = random.Random(8)
    P = [(20 + k * 4, 40 + 18 * __import__("math").sin(k * .7) + rnd.gauss(0, 6)) for k in range(40)]
    return poly(P, "f") + line(200, 60, 340, 60, "g") + txt(200, 50, "one line, kept", "lg")


def fan(n=14, seed=40, gold=True):
    s = ""
    for k in range(n):
        P = walk(seed + k, 21, 20, 330, 64, 0, 4.2, 6, 116)
        s += poly(P, "q")
    if gold:
        s += line(20, 64, 330, 64, "g", dash=True) + txt(330, 12, "same odds, different paths", "lg", "end")
    return s


def daily_limit():
    P = [(20, 30), (60, 46), (90, 40), (130, 62), (170, 56), (210, 86)]
    s = line(20, 86, 340, 86, "r", dash=True) + txt(340, 100, "daily limit · 3 losses", "lr", "end")
    s += poly(P, "g") + dot(210, 86, "r", 3) + line(210, 86, 340, 86, "t") + txt(220, 78, "done for the day", "lt")
    return s


def vol_bands():
    s = ""
    for k, (w, n) in enumerate(((14, 6), (32, 3))):
        x0 = 20 + k * 180
        s += rect(x0, 54 - w, 140, w * 2, "q", 4)
        s += poly(walk(60 + k, 16, x0, x0 + 140, 54, 0, w / 3, 54 - w, 54 + w), "g")
        for j in range(n):
            s += rect(x0 + j * 16, 100, 10, 10, "g")
    return s


def copies():
    s = line(16, 30, 344, 30)
    for k in range(5):
        s += rect(30 + k * 34, 30, 22, 16, "r")
    s += txt(214, 52, "=", anchor="middle") + rect(240, 30, 40, 80, "r") + txt(30, 22, "5 accounts, one trade")
    return s


def frames():
    s = ""
    for k, lab in enumerate(("entry", "exit")):
        x0 = 40 + k * 160
        s += f'<rect class="la-f" x="{x0}" y="14" width="120" height="80" rx="5" fill="none"/>'
        P = walk(70 + k, 10, x0 + 10, x0 + 110, 60, .8 if k else .2, 5, 22, 88)
        s += poly(P, "g") + txt(x0 + 60, 110, lab, anchor="middle")
    return s


def skip():
    s = ""
    for k in range(10):
        x = 30 + k * 31
        if k == 6:
            s += rect(x, 40, 16, 40, "g") + line(x + 8, 30, x + 8, 90, "g")
        else:
            s += rect(x, 50, 16, 20, "q") + line(x + 8, 44, x + 8, 76, "f")
    s += txt(30 + 6 * 31 + 8, 108, "the one setup", "lg", "middle")
    return s


def streak():
    rnd = random.Random(14)
    seq = [rnd.random() < .55 for _ in range(20)]
    seq[6] = seq[14] = True
    seq[7:14] = [False] * 7
    s = ""
    for k, w in enumerate(seq):
        s += dot(24 + k * 16.5, 50, "t" if w else "r", 4.5)
    x0, x1 = 24 + 7 * 16.5 - 6, 24 + 13 * 16.5 + 6
    s += f'<path class="la-r" d="M{_f(x0)},62 v6 H{_f(x1)} v-6" fill="none"/>'
    return s + txt((x0 + x1) / 2, 86, "seven in a row is normal", "lr", "middle")


def size_down():
    P = [(20, 24), (80, 34), (130, 30), (180, 50), (230, 58), (280, 54), (340, 60)]
    s = poly(P, "g") + line(170, 14, 170, 112, "f", dash=True)
    for k in range(9):
        x = 24 + k * 36
        s += rect(x, 112, 14, -(22 if x < 170 else 11), "g" if x < 170 else "t")
    return s + txt(178, 22, "size halves", "lt")


def after_costs():
    a = [(20 + k * 32, 96 - k * 7.5) for k in range(10)]
    b = [(20 + k * 32, 96 - k * 2.6 + (3 if k % 2 else -2)) for k in range(10)]
    return poly(a, "q") + txt(316, a[-1][1] - 6, "before costs", anchor="end") + poly(b, "g") + txt(316, b[-1][1] + 18, "after costs", "lg", "end")


def patience():
    s = line(20, 20, 340, 20, "g", dash=True) + txt(340, 14, "target", "lg", "end")
    for k in range(10):
        s += rect(36 + k * 22, 108, 14, -(k + 1) * 8.6, "t")
    s += rect(286, 108, 14, -40, "rr") + rect(310, 108, 14, -20, "r") + txt(306, 50, "forcing it", "lr", "middle")
    return s


def week():
    rnd = random.Random(21)
    s = line(16, 70, 344, 70)
    for k in range(5):
        v = rnd.uniform(-30, 30)
        s += rect(30 + k * 34, 70, 20, -v, "q")
    s += rect(240, 70, 60, -26, "g") + txt(270, 98, "the week", "lg", "middle") + txt(115, 112, "five days of noise", anchor="middle")
    return s


def grade():
    s = rscale(((-1, "t"), (3, "r")))
    s += f'<path class="la-t" d="M44,32 l4,4 l8,-9" fill="none"/>' + txt(62, 36, "planned", "lt")
    s += f'<path class="la-r" d="M250,8 l8,8 M258,8 l-8,8" fill="none"/>' + txt(264, 16, "unplanned", "lr")
    return s


def oos():
    split = 210
    P = [(20 + k * 10, 96 - k * 3.7) for k in range(20)]
    Q = walk(33, 14, split, 340, P[-1][1], .1, 4, 10, 110)
    return (rect(20, 10, split - 20, 100, "q", 4) + txt(30, 24, "tuned here") + poly(P, "g")
            + line(split, 10, split, 110, "f", dash=True) + poly(Q, "t") + txt(split + 8, 24, "new data", "lt"))


def news():
    s = line(200, 10, 200, 110, "r", dash=True) + txt(206, 20, "CPI", "lr")
    P = [(20, 70), (60, 68), (100, 72), (140, 69), (196, 70), (204, 30), (214, 96), (230, 52), (270, 60), (340, 56)]
    return s + poly(P, "f") + line(20, 92, 180, 92, "g") + dot(180, 92, "g", 3) + txt(20, 108, "flat before the release", "lg")


def calendar():
    s = ""
    for k in range(20):
        x, y = 40 + (k % 10) * 28, 22 + (k // 10) * 30
        c = "t" if k in (0, 1, 2, 4, 5, 7, 8, 9, 10, 11) else "q"
        s += rect(x, y, 20, 20, c, 3)
    s += rect(40 + 4 * 28, 52, 20, 20, "g", 3) + txt(50 + 4 * 28, 98, "payout window", "lg", "middle")
    return s


def one_change():
    s = ""
    for k in range(3):
        y = 30 + k * 30
        s += line(80, y, 280, y, "f")
        x = 230 if k == 1 else 130
        s += dot(x, y, "g" if k == 1 else "q", 7)
    return s + txt(290, 64, "one rule", "lg")


def drip():
    s = ""
    for k in range(40):
        x, y = 24 + (k % 20) * 10, 30 + (k // 20) * 22
        s += line(x, y, x, y + 12, "r")
    s += rect(270, 110, 40, -80, "r") + txt(290, 22, "$800", "lr", "middle") + txt(24, 96, "$4 at a time")
    return s


def levels():
    s = rect(20, 10, 120, 100, "q", 4) + txt(30, 104, "before the open")
    for y in (30, 58, 86):
        s += line(20, y, 340, y, "g", dash=True)
    return s + poly([(140, 70), (170, 62), (200, 58), (230, 44), (260, 32), (290, 40), (320, 30), (340, 28)], "t")


def ruin():
    s = txt(20, 30, "$200") + txt(20, 74, "$400")
    for k in range(10):
        s += dot(80 + k * 24, 26, "r", 6)
    for k in range(5):
        s += dot(80 + k * 24, 70, "r", 6)
    return s + txt(80, 106, "losses in a row to reach max loss")


def focus():
    rnd, s = random.Random(5), ""
    for _ in range(16):
        s += ring(rnd.uniform(20, 180), rnd.uniform(20, 100), "f", rnd.uniform(4, 9))
    return s + ring(270, 60, "g", 34) + ring(270, 60, "g", 18) + dot(270, 60, "g", 4)


def tally():
    s = txt(40, 26, "week A") + txt(210, 26, "week B")
    for k in range(3):
        s += line(44 + k * 12, 40, 44 + k * 12, 64, "r")
    s += txt(40, 84, "3 losses") + txt(40, 98, "0 rule breaks", "lt")
    for k in range(5):
        s += line(214 + k * 12, 40, 214 + k * 12, 64, "r") if k < 4 else line(208, 60, 266, 44, "r")
    s += txt(210, 84, "green P&L") + txt(210, 98, "5 rule breaks", "lr")
    return s


ART = [
    lambda: winloss([1, 1, 1], [4], "+$100 ×3", "−$400 ×1"),
    recover,
    lambda: stop_size(15, 4),
    trail,
    journal,
    escalate,
    lambda: winloss([2, 2, 2, 2], [1, 1, 1, 1, 1, 1], "4 × +$300", "6 × −$150"),
    lambda: curves(4.6, 1.2, "2% risk", "0.5% risk"),
    lambda: hbars([("MES", 5, "g"), ("ES", 50, "g"), ("MGC", 10, "t"), ("GC", 100, "t")]),
    lambda: trail("both"),
    rscale,
    moved_stop,
    lambda: splits([("1 : 2", 1 / 3), ("1 : 1", .5), ("2 : 1", 2 / 3)]),
    gap,
    blocks,
    budget,
    tags,
    average_down,
    costs,
    correlated,
    tradeoff,
    consistency,
    excursion,
    oneline,
    fan,
    daily_limit,
    vol_bands,
    copies,
    frames,
    skip,
    streak,
    size_down,
    after_costs,
    patience,
    week,
    grade,
    oos,
    news,
    calendar,
    one_change,
    drip,
    levels,
    ruin,
    focus,
    tally,
]


def svg(i):
    return (f'<svg class="lsn-art" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">'
            f'{ART[i]()}</svg>')
