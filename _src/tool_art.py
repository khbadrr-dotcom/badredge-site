"""Illustrations for the tools: the homepage Tools card and one header per simulator card on /tools/.
Drawn as plain SVG with the door-art classes (site.css). Illustrations only, not results."""
import math
import random


GOLD_DEFS = ('<defs><linearGradient id="tb-gold" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" class="tb-g0"/><stop offset="1" class="tb-g1"/></linearGradient>'
             '<linearGradient id="tb-goldh" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" class="tb-g1"/><stop offset="1" class="tb-g0"/></linearGradient></defs>')


def _wrap(svg, W, H, cls=""):
    if "tb" in cls.split():
        svg = GOLD_DEFS + svg
    return (f'<div class="door-art tool-art{(" " + cls) if cls else ""}" aria-hidden="true">'
            f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet">{svg}</svg></div>')


def _pts(P):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in P)


def home():
    """What the simulators actually output: many simulated evaluation runs between the
    profit target and the max loss, with the share that passes, fails or runs out of time."""
    W, H = 316, 172
    L, R, T, B = 14, 232, 28, 144            # plot box
    start_y = 104
    rnd = random.Random(21)
    days, n = 30, 40
    dx = (R - L) / days
    passed, failed, timed = [], [], []
    for k in range(n):
        y, P = start_y, [(L, start_y)]
        for d in range(1, days + 1):
            y += rnd.gauss(-2.3, 9.0)
            x = L + d * dx
            if y <= T:
                P.append((x, T)); passed.append(P); break
            if y >= B:
                P.append((x, B)); failed.append(P); break
            P.append((x, y))
        else:
            timed.append(P)
    s = ['<g class="hf-grid">' + "".join(f'<line x1="{L}" y1="{y:.1f}" x2="{R}" y2="{y:.1f}"/>'
                                          for y in (T + (B - T) * f for f in (.25, .5, .75))) + '</g>']
    for P in failed:
        s.append(f'<polyline class="hf-run fail" points="{_pts(P)}"/>')
    for P in timed:
        s.append(f'<polyline class="hf-run time" points="{_pts(P)}"/>')
    for P in passed:
        s.append(f'<polyline class="hf-run pass" points="{_pts(P)}"/>')
    # one highlighted run, drawn on top with a soft area, like the Strategy Lab curve
    hero = max(passed, key=len)
    s.append(f'<polygon class="hf-area" points="{_pts(hero)} {hero[-1][0]:.1f},{B} {L},{B}"/>')
    s.append(f'<polyline class="hf-hero" points="{_pts(hero)}"/>')
    for P in passed:
        s.append(f'<circle class="hf-hit" cx="{P[-1][0]:.1f}" cy="{T}" r="1.5"/>')
    s.append(f'<line class="hf-target" x1="{L}" y1="{T}" x2="{R}" y2="{T}"/>')
    s.append(f'<line class="hf-floor" x1="{L}" y1="{B}" x2="{R}" y2="{B}"/>')
    s.append(f'<circle class="hf-start" cx="{L}" cy="{start_y}" r="3"/>')
    s.append(f'<text class="da-lbl live" x="{L}" y="{T - 9}">profit target</text>')
    s.append(f'<text class="da-lbl" x="{L}" y="{B + 15}">max loss</text>')
    s.append(f'<text class="da-lbl" x="{R}" y="{B + 15}" text-anchor="end">day {days}</text>')
    # outcome split: one bar, three segments, no figures
    bx, bw = 252, 8
    tot = len(passed) + len(failed) + len(timed)
    y0 = T
    for cls, cnt, lbl in (("pass", len(passed), "pass"), ("time", len(timed), "time out"), ("fail", len(failed), "fail")):
        h = (B - T) * cnt / tot
        s.append(f'<rect class="hf-seg {cls}" x="{bx}" y="{y0 + 1:.1f}" width="{bw}" height="{max(h - 2, 1):.1f}" rx="2.5"/>')
        s.append(f'<text class="da-lbl hf-k {cls}" x="{bx + bw + 6}" y="{y0 + h / 2 + 3:.1f}">{lbl}</text>')
        y0 += h
    s.append(f'<text class="da-lbl" x="{bx}" y="{T - 9}">outcomes</text>')
    return _wrap("".join(s), W, H, "tb ta-home")


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


BY_HREF = {}  # filled at the end of the file


# ---- Set B (chosen by Khaled, Nov 23), refined: gold carries the idea, teal marks progress, red only as a hairline ----

def pass_b():
    """An evaluation: progress to the profit target, with each firm rule checked off along the way."""
    W, H = 320, 120
    x0, x1, y = 22, 298, 34
    fill = x0 + (x1 - x0) * 0.78
    s = ['<text class="da-lbl" x="22" y="18">start</text>',
         '<text class="da-lbl code" x="298" y="18" text-anchor="end">profit target</text>',
         f'<rect class="tb-track" x="{x0}" y="{y - 4}" width="{x1 - x0}" height="8" rx="4"/>',
         f'<rect fill="url(#tb-goldh)" x="{x0}" y="{y - 4}" width="{fill - x0:.1f}" height="8" rx="4"/>',
         f'<circle class="tb-knob" cx="{fill:.1f}" cy="{y}" r="6"/>',
         f'<line class="tb-flag-pole" x1="{x1}" y1="{y - 12}" x2="{x1}" y2="{y + 8}"/>']
    rules = ["daily limit", "max loss", "consistency", "min days"]
    for i, r in enumerate(rules):
        cx = 22 + i * 70
        s.append(f'<rect class="tb-rulebox" x="{cx}" y="58" width="64" height="44" rx="9"/>')
        s.append(f'<circle class="tb-ok" cx="{cx + 32}" cy="74" r="7"/>')
        s.append(f'<path class="tb-okt" d="M{cx + 28.5},{74} l2.5,2.6 l4.6,-5"/>')
        s.append(f'<text class="da-lbl sm" x="{cx + 32}" y="95" text-anchor="middle">{r}</text>')
    return _wrap("".join(s), W, H, "tb")


def payout_b():
    """A funded month as a calendar: qualifying days tick off toward the payout day."""
    W, H = 320, 120
    days = ["w", "l", "w", "s", "w", "l", "s", "w", "w", "l", "s", "w", "p", "", ""]
    s = []
    for j, d in enumerate("MTWTF"):
        s.append(f'<text class="da-lbl" x="{30 + j * 36}" y="14" text-anchor="middle">{d}</text>')
    for i, d in enumerate(days):
        c, r = i % 5, i // 5
        x, y = 16 + c * 36, 22 + r * 28
        if d == "p":
            s.append(f'<rect class="tb-day pay" x="{x}" y="{y}" width="28" height="22" rx="6"/>'
                     f'<text class="tb-cur" x="{x + 14}" y="{y + 15}" text-anchor="middle">$</text>')
        else:
            cls = {"w": "tb-day win", "l": "tb-day loss", "s": "tb-day", "": "tb-day empty"}[d]
            s.append(f'<rect class="{cls}" x="{x}" y="{y}" width="28" height="22" rx="6"/>')
            if d == "w":
                s.append(f'<path class="tb-tick" d="M{x + 9},{y + 11} l3.5,3.5 l6.5,-7"/>')
    cx, cy, R = 262, 54, 28
    circ = 2 * math.pi * R
    s.append(f'<circle class="tb-ring" cx="{cx}" cy="{cy}" r="{R}"/>')
    s.append(f'<circle class="tb-ring on" cx="{cx}" cy="{cy}" r="{R}" stroke-dasharray="{circ * 0.999:.1f} {circ:.1f}" transform="rotate(-90 {cx} {cy})"/>')
    for k in range(6):
        a = math.radians(-90 + k * 60)
        s.append(f'<circle class="tb-notch" cx="{cx + R * math.cos(a):.1f}" cy="{cy + R * math.sin(a):.1f}" r="2.2"/>')
    s.append(f'<text class="tb-cur big" x="{cx}" y="{cy + 6}" text-anchor="middle">$</text>')
    s.append(f'<text class="da-lbl" x="{cx}" y="106" text-anchor="middle">winning days</text>')
    return _wrap("".join(s), W, H, "tb")


def sizing_b():
    """Size scales as the buffer grows: stacks of contracts step up under the cushion line."""
    W, H = 320, 120
    s = ['<line class="tb-rule" x1="14" y1="98" x2="306" y2="98"/>']
    P = [(14, 80), (74, 80), (86, 64), (146, 64), (158, 48), (218, 48), (230, 32), (306, 32)]
    s.append(f'<polyline class="tb-buffer" points="{_pts(P)}"/>')
    for i in range(4):
        x = 26 + i * 72
        for k in range(i + 1):
            for j in range(3):
                s.append(f'<rect class="tb-ct" x="{x + j * 14}" y="{86 - k * 12}" width="11" height="9" rx="2"/>')
        s.append(f'<text class="da-lbl" x="{x + 20}" y="112" text-anchor="middle">{i + 1}x</text>')
    s.append('<text class="da-lbl live" x="306" y="24" text-anchor="end">buffer</text>')
    return _wrap("".join(s), W, H, "tb")


BY_HREF.update({"/tools/pass/": pass_b, "/tools/payout/": payout_b, "/tools/sizing/": sizing_b})  # Set B, chosen by Khaled Nov 23
