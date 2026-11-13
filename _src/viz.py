"""Small, dependency-free charts for the research pages (HTML + CSS bars, inline SVG).

All colours come from site CSS tokens, so light and dark themes both work.
Every chart has a visible title, value labels and a hover title; numbers are also in the tables below them.
"""


def hbars(rows, title, sub="", unit="", fmt="{:.1f}", ref=None, ref_label="", max_v=None, cls=""):
    """Horizontal bar chart. rows = [(label, value, href_or_None, note)]. ref = vertical reference value."""
    top = max_v or max(v for _, v, _, _ in rows) * 1.08
    out = []
    refm = f'<b class="hb-refm" style="left:{ref / top * 100:.1f}%"></b>' if ref is not None else ""
    for label, v, href, note in rows:
        w = min(v / top, 1) * 100
        over = ' over' if v > top else ''
        lab = f'<a href="{href}">{label}</a>' if href else label
        out.append(f'<div class="hb-row" title="{label}: {fmt.format(v)}{unit}">'
                   f'<span class="hb-lab">{lab}{f"<small>{note}</small>" if note else ""}</span>'
                   f'<span class="hb-track"><i class="hb-bar{over}" style="width:{w:.1f}%"></i>{refm}</span>'
                   f'<span class="hb-val">{fmt.format(v)}{unit}</span></div>')
    leg = f'<span class="legend"><span class="lg"><i class="lg-ref"></i>{ref_label}</span></span>' if ref is not None else ""
    return (f'<figure class="viz hb {cls}"><figcaption><b>{title}</b>{f"<span>{sub}</span>" if sub else ""}{leg}</figcaption>'
            f'<div class="hb-body">{"".join(out)}</div></figure>')


def paired(rows, title, sub, a_label, b_label, unit="$"):
    """Two measures of the same unit per row (e.g. net vs worst drawdown), one shared scale."""
    top = max(max(a, b) for _, a, b, _ in rows) * 1.05
    out = []
    for label, a, b, href in rows:
        lab = f'<a href="{href}">{label}</a>' if href else label
        out.append(f'<div class="pr-row" title="{label}: {a_label} {unit}{a:,.0f}, {b_label} {unit}{b:,.0f}">'
                   f'<span class="hb-lab">{lab}</span><span class="pr-bars">'
                   f'<span class="pr-line"><i class="pr-a" style="width:{a / top * 100:.1f}%"></i><em>{unit}{a:,.0f}</em></span>'
                   f'<span class="pr-line"><i class="pr-b" style="width:{b / top * 100:.1f}%"></i><em>{unit}{b:,.0f}</em></span>'
                   f'</span></div>')
    legend = (f'<span class="lg"><i class="pr-a"></i>{a_label}</span><span class="lg"><i class="pr-b"></i>{b_label}</span>')
    return (f'<figure class="viz pr"><figcaption><b>{title}</b><span>{sub}</span><span class="legend">{legend}</span></figcaption>'
            f'<div class="hb-body">{"".join(out)}</div></figure>')


def split_bar(win, label="Win rate"):
    """Single 100% bar: winners vs the rest."""
    return (f'<div class="split" title="{label}: {win:.1f}% of trades won">'
            f'<i style="width:{win:.1f}%"></i><span>{win:.1f}% of trades won</span></div>')


def stepper(stage):
    """Research path with the current stage highlighted. stage: 1..4"""
    steps = [("Idea", "Rule written down"), ("Backtested", "Run after costs"),
             ("Last-year pick", "Settings picked in-sample"), ("Forward testing", "Logged on new data, rules frozen")]
    out = []
    for i, (h, s) in enumerate(steps, 1):
        st = "done" if i < stage else ("now" if i == stage else "next")
        out.append(f'<li class="{st}"><b>{h}</b><small>{s}</small></li>')
    return f'<ol class="stepper" aria-label="Research stage: {steps[stage - 1][0]}">{"".join(out)}</ol>'


def timeline(spans, start, end, marks=(), title="", sub=""):
    """spans = [(label, from_ym, to_ym, cls)] with ym = (year, month). Years along the axis."""
    def x(ym):
        return ((ym[0] - start[0]) * 12 + ym[1] - start[1]) / ((end[0] - start[0]) * 12 + end[1] - start[1]) * 100
    bars = "".join(f'<span class="tl-span {c}" style="left:{x(a):.2f}%;width:{x(b) - x(a):.2f}%" title="{l}"><em>{l}</em></span>'
                   for l, a, b, c in spans)
    ticks = "".join(f'<span class="tl-tick" style="left:{x((y, 1)):.2f}%">{y}</span>'
                    for y in range(start[0] + (start[1] > 1), end[0] + 1) if x((y, 1)) <= 100)
    mk = "".join(f'<span class="tl-mark" style="left:{x(ym):.2f}%"><em>{l}</em></span>' for l, ym in marks)
    return (f'<figure class="viz tl"><figcaption><b>{title}</b>{f"<span>{sub}</span>" if sub else ""}</figcaption>'
            f'<div class="tl-body"><div class="tl-lane">{bars}{mk}</div><div class="tl-axis">{ticks}</div></div></figure>')


def pipeline(steps):
    """steps = [(title, detail)] -> numbered flow."""
    return '<ol class="pipeline">' + "".join(
        f'<li><span class="pl-n">{i:02d}</span><b>{t}</b><small>{d}</small></li>' for i, (t, d) in enumerate(steps, 1)) + "</ol>"


def gauge(value, limit, title, fmt, note):
    """Value against a fixed desk limit on one scale."""
    top = max(value, limit) * 1.25
    return (f'<div class="gauge" title="{title}: {fmt.format(value)} (limit {fmt.format(limit)})">'
            f'<div class="g-head"><b>{title}</b><span>{fmt.format(value)}</span></div>'
            f'<div class="g-track"><i style="width:{value / top * 100:.1f}%"></i>'
            f'<span class="g-lim" style="left:{limit / top * 100:.1f}%"><em>Desk limit {fmt.format(limit)}</em></span></div>'
            f'<small>{note}</small></div>')
