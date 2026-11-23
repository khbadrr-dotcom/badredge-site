"""Illustrations for the tools: the homepage Tools card and one header per simulator card on /tools/.
Drawn as plain SVG with the door-art classes (site.css). Illustrations only, not results."""
import math
import random


def _wrap(svg, W, H, cls=""):
    return (f'<div class="door-art tool-art{(" " + cls) if cls else ""}" aria-hidden="true">'
            f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet">{svg}</svg></div>')


def _pts(P):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in P)


def home():
    """Pre-open risk console: pass-odds gauge, payout-day tracker and a contract ladder, one per tool."""
    W, H = 330, 150
    s = []
    # panel frames
    for x0 in (6, 116, 226):
        s.append(f'<rect class="ta-panel" x="{x0}" y="8" width="98" height="134" rx="10"/>')
    # 1. gauge
    cx, cy, r = 55, 92, 36
    def arc(a0, a1, cls):
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        return f'<path class="{cls}" d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}"/>'
    s.append(arc(180, 128, "ta-arc dn"))
    s.append(arc(124, 64, "ta-arc gd"))
    s.append(arc(60, 0, "ta-arc up"))
    for a in range(0, 181, 15):
        ri, ro = r - 9, r - 6
        s.append(f'<line class="da-faint" x1="{cx + ri * math.cos(math.radians(a)):.1f}" y1="{cy - ri * math.sin(math.radians(a)):.1f}" '
                 f'x2="{cx + ro * math.cos(math.radians(a)):.1f}" y2="{cy - ro * math.sin(math.radians(a)):.1f}"/>')
    na = 48
    s.append(f'<line class="ta-needle" x1="{cx}" y1="{cy}" x2="{cx + (r - 4) * math.cos(math.radians(na)):.1f}" y2="{cy - (r - 4) * math.sin(math.radians(na)):.1f}"/>')
    s.append(f'<circle class="da-dot-gold" cx="{cx}" cy="{cy}" r="3.5"/>')
    s.append(f'<text class="da-lbl" x="{cx}" y="122" text-anchor="middle">pass odds</text>')
    s.append(f'<text class="da-lbl" x="20" y="28">01</text>')
    # 2. payout-day tracker: winning days fill toward a payout coin
    x0, y0, g = 134, 50, 14
    for i in range(10):
        col, row = i % 5, i // 5
        cls = "ta-day on" if i < 7 else "ta-day"
        s.append(f'<rect class="{cls}" x="{x0 + col * g:.1f}" y="{y0 + row * g:.1f}" width="10" height="10" rx="2.5"/>')
    s.append(f'<circle class="ta-coin" cx="165" cy="98" r="13"/><circle class="ta-coin-in" cx="165" cy="98" r="8.5"/>')
    s.append('<text class="ta-coin-t" x="165" y="101.5" text-anchor="middle">$</text>')
    s.append(f'<text class="da-lbl" x="165" y="132" text-anchor="middle">payout</text>')
    s.append(f'<text class="da-lbl" x="130" y="28">02</text>')
    # 3. contract ladder against the max loss
    lim = 300
    for i, w in enumerate((18, 30, 42, 54, 70)):
        y = 108 - i * 15
        cls = "ta-bar over" if 238 + w > lim else "ta-bar"
        s.append(f'<rect class="{cls}" x="238" y="{y}" width="{w}" height="10" rx="3"/>')
    s.append(f'<line class="da-floor" x1="{lim}" y1="40" x2="{lim}" y2="122"/>')
    s.append(f'<text class="da-lbl" x="275" y="132" text-anchor="middle">size</text>')
    s.append(f'<text class="da-lbl" x="240" y="28">03</text>')
    return _wrap("".join(s), W, H, "ta-home")


def pass_():
    """An evaluation: balance climbs to the target while the trailing max loss steps up behind it."""
    W, H = 320, 120
    rnd = random.Random(5)
    y, P = 84, [(16, 84)]
    for k, x in enumerate(range(28, 256, 12)):
        y = max(min(y - 3.2 + rnd.uniform(-6, 6) + (7 if k in (4, 11) else 0), 96), 26)
        P.append((x, y))
    P.append((266, 22))
    trail, hi = [], 84
    for x, yy in P:
        hi = min(hi, yy)
        f = min(hi + 30, 104)
        if trail:
            trail.append((x, trail[-1][1]))
        trail.append((x, f))
    s = ['<g class="da-grid"><line x1="0" y1="40" x2="320" y2="40"/><line x1="0" y1="72" x2="320" y2="72"/></g>',
         f'<line class="da-target" x1="12" y1="22" x2="304" y2="22"/>',
         f'<polygon class="da-area" points="{_pts(P)} 266,108 16,108"/>',
         f'<polyline class="ta-trail" points="{_pts(trail)}"/>',
         f'<polyline class="da-gold" points="{_pts(P)}"/>',
         f'<circle class="da-start" cx="16" cy="84" r="3"/>',
         '<line class="ta-pole" x1="266" y1="22" x2="266" y2="4"/><path class="ta-flag" d="M266,5 L282,10 L266,15 Z"/>',
         '<text class="da-lbl live" x="16" y="16">target</text>',
         '<text class="da-lbl dn" x="200" y="116">trailing max loss</text>']
    return _wrap("".join(s), W, H)


def payout():
    """A funded account: winning days are counted until the payout unlocks."""
    W, H = 320, 120
    vals = [14, -6, 18, 9, -10, 22, 12, -4, 16, 20, 8, 24]
    base, x0, bw, gap = 70, 16, 12, 6
    s = ['<g class="da-grid"><line x1="0" y1="70" x2="320" y2="70"/></g>']
    n = 0
    for i, v in enumerate(vals):
        x = x0 + i * (bw + gap)
        if v >= 0:
            s.append(f'<rect class="ta-pnl up" x="{x}" y="{base - v * 1.6:.1f}" width="{bw}" height="{v * 1.6:.1f}" rx="2"/>')
            if v >= 12 and n < 5:
                n += 1
                s.append(f'<circle class="da-mark" cx="{x + bw / 2}" cy="84" r="3"/>')
        else:
            s.append(f'<rect class="ta-pnl dn" x="{x}" y="{base}" width="{bw}" height="{-v * 1.6:.1f}" rx="2"/>')
    s.append('<text class="da-lbl live" x="16" y="100">winning days</text>')
    s.append('<line class="ta-pole" x1="236" y1="84" x2="262" y2="84"/>')
    s.append('<circle class="ta-coin" cx="284" cy="62" r="20"/><circle class="ta-coin-in" cx="284" cy="62" r="13"/>')
    s.append('<text class="ta-coin-t big" x="284" y="67" text-anchor="middle">$</text>')
    s.append('<text class="da-lbl code" x="284" y="104" text-anchor="middle">payout</text>')
    return _wrap("".join(s), W, H)


def sizing():
    """A stop in points becomes risk per contract; contracts stack until the max loss cushion is full."""
    W, H = 320, 120
    s = ['<g class="da-grid"><line x1="0" y1="60" x2="320" y2="60"/></g>',
         # candle with entry and stop
         '<line class="ta-wick" x1="46" y1="22" x2="46" y2="88"/>',
         '<rect class="ta-candle" x="36" y="30" width="20" height="52" rx="2"/>',
         '<line class="da-entry" x1="18" y1="32" x2="96" y2="32"/>',
         '<line class="da-floor" x1="18" y1="92" x2="96" y2="92"/>',
         '<path class="ta-bracket" d="M104,32 h6 v60 h-6"/>',
         '<text class="da-lbl code" x="62" y="26">entry</text>',
         '<text class="da-lbl dn" x="62" y="106">stop</text>',
         '<path class="ta-arrow" d="M124,62 h22 m-6,-5 l6,5 l-6,5"/>',
         # cushion bar filled by contracts
         '<rect class="ta-cushion" x="160" y="44" width="140" height="36" rx="8"/>']
    for i in range(5):
        x = 166 + i * 30
        cls = "ta-ct over" if i == 4 else "ta-ct"
        s.append(f'<rect class="{cls}" x="{x}" y="50" width="24" height="24" rx="5"/>')
    s.append('<line class="da-floor" x1="296" y1="34" x2="296" y2="92"/>')
    s.append('<text class="da-lbl" x="160" y="104">contracts</text>')
    s.append('<text class="da-lbl dn" x="300" y="104" text-anchor="end">max loss</text>')
    return _wrap("".join(s), W, H)


BY_HREF = {"/tools/pass/": pass_, "/tools/payout/": payout, "/tools/sizing/": sizing}
