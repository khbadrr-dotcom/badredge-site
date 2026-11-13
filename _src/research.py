"""Research section of badredge.com: method, backtested strategies, lessons, under observation.

Imported by build.py. Content rules (from Khaled, 2026-11-12):
1. Never claim a profitable or validated strategy. Every result carries a status label.
2. Results are after costs (fees + slippage). Optimised picks are always labelled in-sample.
3. No performance promises, no signals. Not-financial-advice note on every page.
4. Publish rules, method and findings only. No raw market data (licence forbids redistribution).
"""

RESEARCH_UPDATED = "12 November 2026"

STATUS = {
    "no-edge": ("Tested · no edge", "st-no"),
    "exploratory": ("Exploratory", "st-exp"),
    "unsuitable": ("Real effect · currently unsuitable", "st-uns"),
    "observe": ("Under observation", "st-obs"),
}

COST_NOTE = ("All dollar figures are hypothetical backtest results for one contract, after exchange and broker fees and "
             "one tick of slippage on each side of every market or stop order. They describe the past under stated "
             "assumptions and do not predict future results.")

NFA = ("Research notes for education only. Not financial advice, not a recommendation and not a signal. "
       "No strategy on this site has passed final validation. Futures trading involves substantial risk of loss.")


def badge(status):
    label, cls = STATUS[status]
    return f'<span class="status {cls}">{label}</span>'


# ---------------------------------------------------------------------------------------------------------------
# Backtested strategies: one entry per tested family
# Each: slug, name, status, group, markets, scope, idea, tested (list), results (html), verdict, lesson
# ---------------------------------------------------------------------------------------------------------------
FAMILIES = [
    dict(
        slug="orb-pro-max", name="Opening range breakout: Pro Max", status="no-edge", group="Opening range and session",
        markets="MGC, MES, MYM, MNQ, SIL, PL", scope="5m and 15m charts · tuned on Oct 2025 to Oct 2026 · replayed on Oct 2021 to Oct 2025",
        idea="Mark the high and low of a fixed 30-minute window. Trade the first close beyond that range, or the first fair-value gap that forms after it, with the stop on the other side of the range.",
        tested=[
            "Hundreds of thousands of setting combinations per market (window start, entry type, stop, target, filters), searched on the most recent 12 months.",
            "The best setting per market was frozen and replayed unchanged on four earlier years it had never seen.",
            "One market (MYM) also got a pre-registered frozen test, written down before it was run.",
            "15 trader-designed filters (trend, volatility, session, day-of-week and more) were added to the best gold version, each compared against a random placebo filter.",
        ],
        results="""<table><thead><tr><th>Pick</th><th>12 months, in-sample (picked here)</th><th>2021 to 2025, unseen</th></tr></thead><tbody>
<tr><td>MGC #1</td><td>323 trades · 71% WR · +$7,403</td><td>1,362 trades · 52% WR · &minus;$4,666 · DD $4,900</td></tr>
<tr><td>MYM #1 (pre-registered)</td><td>122 trades · 80% WR · +$1,844</td><td>549 trades · 53% WR · &minus;$2,074</td></tr>
<tr><td>MES #1</td><td>76 trades · 71% WR · +$821</td><td>264 trades · 58% WR · +$77</td></tr>
<tr><td>MGC #2 (pre-registered)</td><td>90 trades · 84% WR · +$2,412</td><td>294 trades · 66% WR · &minus;$323</td></tr>
</tbody></table>
<p>The in-sample column is the best result out of a very large search on the same data, so it is expected to look good. The added trader filters: 0 of 15 beat a random placebo filter, and all 15 made the base version worse.</p>""",
        verdict="No edge beyond selection. The picked settings sit inside what a random-direction search produces, and both pre-registered frozen tests failed.",
        lesson="A 70 to 80% win rate on the year you optimised on is the normal output of a big search, not a sign of an edge. Random-direction picks from the same pipeline also showed 77 to 92% win rates.",
    ),
    dict(
        slug="orb-break-and-hold", name="Opening range: Break and Hold", status="no-edge", group="Opening range and session",
        markets="MGC, MES, MYM, MNQ", scope="15m signals · two windows per day · same tune-then-replay design",
        idea="Five levels inside each opening range (high, 75%, middle, 25%, low). A 15-minute candle that closes beyond a level is a 'hold', and the trade goes in that direction with an EMA trend filter.",
        tested=[
            "Full grid of windows, levels, filters and exits on four markets, ranked on the last 12 months.",
            "Walk-forward check: choose the best setting on the first half of the year, then trade it on the second half.",
            "The best MYM setting was frozen and replayed on 2021 to 2025.",
        ],
        results="""<table><thead><tr><th>Check</th><th>Result</th></tr></thead><tbody>
<tr><td>MGC walk-forward</td><td>first half, picked there: +$10,889 · second half, unseen: &minus;$955</td></tr>
<tr><td>MYM #1, in-sample 12m</td><td>245 trades · 71% WR · +$2,660</td></tr>
<tr><td>MYM #1, 2021 to 2025 unseen</td><td>1,064 trades · 64% WR · &minus;$1,812 · DD $2,844</td></tr>
</tbody></table>""",
        verdict="No edge beyond selection on any of the four markets.",
        lesson="A walk-forward collapse (large profit on the half you chose from, a loss on the next half) is the fastest way to spot an over-fitted setting.",
    ),
    dict(
        slug="orb-v4", name="Opening range: two-window v4", status="no-edge", group="Opening range and session",
        markets="MGC, MNQ, SIL, PL, M2K, MCL, MHG, M6E, MYM", scope="1m charts · tuned on the last 12 months · replayed on 2021 to 2025",
        idea="Two independent opening-range windows per day. Entry on a candle close beyond enabled range levels, with an optional 'reclaim' entry and an opening-range size filter.",
        tested=[
            "Grid search on nine markets; best setting per market frozen.",
            "Each pick compared against ten random-direction searches run through the identical pipeline.",
            "Frozen replay of every pick on 2021 to 2025.",
        ],
        results="""<table><thead><tr><th>Pick</th><th>12 months, in-sample</th><th>2021 to 2025, unseen</th></tr></thead><tbody>
<tr><td>SIL #1</td><td>145 trades · 90% WR · +$21,156</td><td>541 trades · 75% WR · &minus;$2,657</td></tr>
<tr><td>MGC #1</td><td>152 trades · 80% WR · +$9,517</td><td>644 trades · 66% WR · &minus;$374</td></tr>
<tr><td>PL #1</td><td>79 trades · 89% WR · +$13,839</td><td>409 trades · 68% WR · &minus;$967</td></tr>
<tr><td>MCL #1</td><td>151 trades · 83% WR · +$2,645</td><td>601 trades · 66% WR · &minus;$2,193</td></tr>
</tbody></table>
<p>PL was the only pick that beat all ten random-direction searches and passed its walk-forward check. It still lost on the four unseen years, so it stays exploratory, not promising.</p>""",
        verdict="No edge. Every frozen pick lost money on the unseen years.",
        lesson="Even a pick that beats its random-direction null can fail on unseen data when the sample is thin (85 trades). Passing one check is not validation.",
    ),
    dict(
        slug="initial-balance", name="Initial Balance (multi-session)", status="no-edge", group="Opening range and session",
        markets="MGC, MNQ, MHG, M6E, SIL, MYM, MCL, M2K, MES", scope="1m charts · Tokyo, London and New York slots · tuned 12m, replayed 2021 to 2025",
        idea="The first hour of a session sets the Initial Balance. Trade rejections of its edges, immediate breakouts, or breakouts followed by a retest, with targets at the midpoint and 0.5x to 2x extensions.",
        tested=[
            "Up to three independent one-hour engines per day, three entry models and a range of extensions, searched per market.",
            "Frozen replay of the best settings on 2021 to 2025.",
            "A separate study of breakout continuation and fades in Tokyo and London.",
        ],
        results="""<table><thead><tr><th>Pick</th><th>12 months, in-sample</th><th>2021 to 2025, unseen</th></tr></thead><tbody>
<tr><td>MGC #1</td><td>231 trades · 80% WR · +$5,006</td><td>1,126 trades · 76% WR · &minus;$2,733 · DD $3,947</td></tr>
<tr><td>MNQ #1</td><td>417 trades · 81% WR · +$8,383</td><td>1,664 trades · 73% WR · &minus;$2,803</td></tr>
<tr><td>MHG #1</td><td>375 trades · 51% WR · +$7,156</td><td>1,320 trades · 41% WR · &minus;$7,693</td></tr>
</tbody></table>
<p>Notice the MGC row: a 76% win rate on unseen data, and still a loss. Small targets win often, and the few full-size losses take it all back.</p>""",
        verdict="No edge beyond selection. Two narrow Tokyo/London variants remain exploratory, with too few trades and edges too small to matter after costs.",
        lesson="A high win rate is not an edge. What matters is average net profit per trade compared with the round-trip cost.",
    ),
    dict(
        slug="asian-range-breakout", name="Asian range breakout (gold)", status="exploratory", group="Opening range and session",
        markets="MGC", scope="1h chart · rules written before testing · split 2025 / 2026",
        idea="Mark the range of the Asian session. Trade the breakout during London and New York hours, stop at the other side of the range, target 1R, time exit in the afternoon.",
        tested=[
            "One rule set written down before any test (no grid search).",
            "In-sample year 2025, then an out-of-sample test on 2026 to October.",
        ],
        results="""<table><thead><tr><th>Window</th><th>Trades</th><th>Win rate</th><th>Profit factor</th><th>Avg per trade</th><th>Max DD</th></tr></thead><tbody>
<tr><td>Full period</td><td>389</td><td>56%</td><td>1.38</td><td>+$45.6</td><td>$5,670</td></tr>
<tr><td>2026 out-of-sample</td><td>168</td><td>58%</td><td>1.44</td><td>+$70.2</td><td>$3,246</td></tr>
</tbody></table>""",
        verdict="Exploratory (on hold). It passed its own out-of-sample bar, but a reviewer asked for gold data back to 2015 before anything can be concluded, and that test has not been run. The drawdown is also above the $2,000 limit for one contract.",
        lesson="One good out-of-sample year is a reason to test further, not a reason to trade. A reviewer asked for about ten years of gold history before going further.",
    ),
    dict(
        slug="smt-divergence", name="SMT divergence", status="no-edge", group="Price action and levels",
        markets="MNQ, MES, MYM, MGC, SIL, PL (8 market pairs)", scope="1m to 15m · reversal and filter versions",
        idea="When one of two related markets makes a new high or low and the other does not, the move is expected to fail and reverse.",
        tested=[
            "General SMT reversal across eight market pairs.",
            "SMT as a filter inside other setups (Initial Balance fades, GIFVG).",
            "A narrow New York pre-session version on MNQ.",
        ],
        results="""<ul>
<li>General reversal: no directional edge. Results matched a random-direction control.</li>
<li>London Initial Balance fade on MES when MNQ has not broken: 147 trades, about +$5 per contract (+0.08R). The mirror trade was negative. Exploratory.</li>
<li>New York pre-session MNQ version: 21 trades in-sample and 8 out-of-sample. Far too few to judge.</li>
</ul>""",
        verdict="No edge as a general reversal signal. Two narrow versions are logged as exploratory because the samples are tiny.",
        lesson="Divergence feels predictive on a chart because you remember the reversals. Counted over every occurrence, it was no better than a coin flip on direction.",
    ),
    dict(
        slug="ifvg-breaker", name="iFVG and breaker blocks", status="no-edge", group="Price action and levels",
        markets="10 markets: MNQ, MES, MYM, M2K, MGC, SIL, PL, MCL, MHG, M6E", scope="5m and 15m · 360 settings · frozen test 2021 to 2025",
        idea="After a liquidity sweep and a market-structure shift, an inverted fair-value gap that overlaps a breaker block marks a zone. Enter with a limit order in the zone, stop beyond the sweep.",
        tested=[
            "360 settings per market, plus versions with only the iFVG or only the breaker.",
            "Random-direction null and walk-forward on the last 12 months.",
            "Pre-registered frozen test on 2021 to 2025 for one primary setting per market.",
        ],
        results="""<ul>
<li>The best 12-month setting sat inside the random-direction null on 9 of 10 markets.</li>
<li>Walk-forward second half was zero or negative on 9 of 10.</li>
<li>Frozen test: 0 of 10 primaries passed. Average result per trade ranged from &minus;0.23R to +0.03R after costs.</li>
</ul>""",
        verdict="No edge, in this scope.",
        lesson="A confluence of two concepts needs a placebo test (fake zones of the same size), not just a test of each part on its own.",
    ),
    dict(
        slug="gifvg", name="GIFVG checklist", status="no-edge", group="Price action and levels",
        markets="MNQ, MES, MYM, MGC, SIL, PL", scope="5m higher-timeframe gap + 1m inversion · 2021 to 2026",
        idea="A higher-timeframe fair-value gap, confirmed by a 1-minute inversion after a liquidity raid with SMT, targeting the range extreme.",
        tested=["The full checklist, plus six ablations that remove one condition at a time.", "2,538 trades pooled across six markets."],
        results="""<ul>
<li>All 42 market and version cells were negative per trade after costs.</li>
<li>Pooled: &minus;0.21R per trade (upper 95% bound &minus;0.15R).</li>
<li>The same entries with a random direction also lost about &minus;0.22R, so cost and payoff shape decided the result, not the pattern.</li>
</ul>""",
        verdict="No edge, in this scope.",
        lesson="If random entries with the same stops and targets lose about the same amount, the pattern is adding nothing.",
    ),
    dict(
        slug="key-level-retests", name="Key-level break and retest", status="no-edge", group="Price action and levels",
        markets="MNQ, MES, MYM", scope="5m and 15m · 23 level types · 540 settings",
        idea="Break of a key level (prior day high/low, session highs/lows, opens and more), then a retest that holds, or a failed break with a wick reclaim.",
        tested=["23 level types, two entry models, three exit styles, plus VIX and cross-market filters.", "Gross check before costs, on both the real and the flipped direction."],
        results="""<ul>
<li>Before costs, the average result was negative on the real side in 36 of 36 groups, and on the flipped side in 35 of 36.</li>
<li>No setting survived the random-direction null or walk-forward.</li>
</ul>""",
        verdict="No sign of an edge. Formally closed as insufficient evidence on statistical power, with the family closed in this scope.",
        lesson="Check the gross result on both directions before any optimisation. If both lose before costs, no filter or exit will rescue it.",
    ),
    dict(
        slug="support-resistance-pivots", name="Support and resistance with pivots", status="no-edge", group="Price action and levels",
        markets="10 markets", scope="5m and 15m · 1,440 settings · frozen test 2021 to 2025",
        idea="Swing-based support and resistance zones that line up with daily floor pivots or Camarilla levels. Trade the bounce, the break, or the break and retest.",
        tested=["1,440 settings across ten markets.", "Pre-registered frozen test on 2021 to 2025, Holm-corrected across 20 primaries."],
        results="""<ul>
<li>Frozen pooled primary (15m bounce at confluence): &minus;0.095R per trade, 95% interval &minus;0.115R to &minus;0.074R, with full statistical power.</li>
<li>0 of 20 primaries passed after Holm correction.</li>
</ul>""",
        verdict="No edge. Family closed in this scope.",
        lesson="A precise negative result is still a result: this test had enough trades to rule out an edge of the size that would matter.",
    ),
    dict(
        slug="psar-ema200", name="Parabolic SAR with 200 EMA", status="no-edge", group="Trend and momentum",
        markets="MGC, SIL, PL, MHG, M2K", scope="5m to 60m · volume and delta filters · frozen test on MGC 30m",
        idea="Take Parabolic SAR flips only in the direction of the 200 EMA, with volume above average.",
        tested=["Timeframe scan from 5 to 60 minutes and filter tuning on the last 12 months.", "Frozen replay of the gold 30m version on 2021 to 2025."],
        results="""<ul>
<li>Best 12-month picks sat inside the random-direction null (MGC 0.885, SIL 0.495 percentile; 0.95 needed).</li>
<li>Walk-forward second half was negative or broke the $2,000 drawdown limit in 9 of 15 cases.</li>
<li>MGC 30m frozen replay: profit factor 0.75, &minus;$8,012.</li>
</ul>""",
        verdict="No edge.",
        lesson="Classic indicator combinations are already in every chart package. Expect them to be priced in, and test them like anything else.",
    ),
    dict(
        slug="ema-vwap-momentum", name="EMA and VWAP momentum", status="no-edge", group="Trend and momentum",
        markets="MES, MNQ, MYM, MGC", scope="5m · 720 settings · 2021 to 2026 · frozen test",
        idea="Enter when a fast EMA crosses the session VWAP (or a slower EMA), with a volume filter and a daily trend bias.",
        tested=["EMA12 x VWAP crosses on MES and MYM.", "720 momentum settings with volume and daily bias, with a frozen test on 2021 to 2025."],
        results="""<ul>
<li>Gross edge was about $0.10 to $1 per trade against a $2 to $4 round-trip cost.</li>
<li>Frozen test: 0 of 12 passed. The best one made +$224 over four years (t = &minus;0.22, so indistinguishable from zero).</li>
<li>12-month to 6-month walk-forward was negative on all four markets.</li>
</ul>""",
        verdict="No edge.",
        lesson="Compare the average gross profit per trade with the round-trip cost first. If the edge is smaller than the cost, nothing else matters.",
    ),
    dict(
        slug="monday-high-low", name="Monday high and low", status="no-edge", group="Price action and levels",
        markets="MNQ, MES, MYM", scope="9,120 settings · 12m search · frozen test 2021 to 2025",
        idea="Monday's high and low act as weekly reference levels. Trade the reaction at the next session open, or a sweep and reclaim during the week.",
        tested=["9,120 settings on the last 12 months.", "Pre-registered frozen test of the best four on 2021 to 2025."],
        results="""<ul>
<li>12-month picks beat the selection null only weakly, and walk-forward failed on all three markets.</li>
<li>Frozen: 4 of 4 no edge. MNQ primary &minus;0.056R per trade.</li>
</ul>""",
        verdict="No edge, in this scope.",
        lesson="A weak pass on correlated markets (three US indices) counts as one result, not three.",
    ),
    dict(
        slug="iv-walls", name="Options open-interest walls", status="no-edge", group="Price action and levels",
        markets="MES, MNQ", scope="Quarterly and serial ES/NQ options · 5m and 15m · 72 settings per model",
        idea="The strikes with the largest open interest above and below price act as walls: price rejects them or breaks through and retests.",
        tested=["Three models (wick rejection, breakout, break and retest).", "Every setting run on the real walls and on placebo strikes the same distance away.", "Open interest used only as it was known at the time (2 to 5 days old)."],
        results="""<ul>
<li>All six market and model cells lost after costs: &minus;0.03R to &minus;0.27R per trade.</li>
<li>The best wall settings were no better than the best placebo settings.</li>
</ul>""",
        verdict="No edge, in this scope. Weekly and 0DTE options were not tested.",
        lesson="Placebo levels are the fair test for any level-based idea. If made-up levels do as well, the real ones carry no information.",
    ),
    dict(
        slug="daily-trend", name="Daily trend signals traded intraday", status="no-edge", group="Trend and momentum",
        markets="10 markets", scope="EWMAC and TSMOM signals · entries at 01:00, 10:00 or 16:30 GMT+3 · frozen test 2022 to 2025",
        idea="Use a classic daily trend signal (moving-average crossover or 12-month momentum) to choose the direction, then hold only inside the trading day.",
        tested=["Four literature-fixed variants, about 8,850 trades each.", "Pre-registered frozen test with Holm correction and power calculated in advance."],
        results="""<ul>
<li>All four were negative after costs: &minus;0.031R to &minus;0.043R per trade.</li>
<li>Gross results before costs were also slightly negative.</li>
<li>Power was 0.77 to 1.00, so an edge of a useful size would likely have been detected.</li>
</ul>""",
        verdict="No edge.",
        lesson="Trend following earns over weeks and months. Cutting it into single sessions removes most of what it captures.",
    ),
    dict(
        slug="intraday-momentum", name="Market intraday momentum", status="no-edge", group="Trend and momentum",
        markets="MES, MNQ, MYM, M2K", scope="Gao et al. (2018) and Baltussen et al. (2021) rules · frozen test 2021 to 2025",
        idea="Published research found that the first half hour of the day predicts the direction of the last half hour.",
        tested=["Five pre-registered versions, including the papers' own last-half-hour trade.", "No parameters were fitted."],
        results="""<ul>
<li>All five lost after costs: &minus;$2.17 to &minus;$28.61 per day.</li>
<li>The predictive link faded year by year: +0.15 in 2021, +0.07, +0.01, then negative from 2024.</li>
<li>Inside the allowed trading hours the gross gain was about $1 to $2 per trade, below a $2.20 to $3.70 round trip.</li>
</ul>""",
        verdict="No edge. Exhausted in scope.",
        lesson="Published effects decay once they are known. Check the effect year by year before trusting a paper's full-period average.",
    ),
    dict(
        slug="noise-area", name="Noise-area momentum", status="observe", group="Trend and momentum",
        markets="MNQ (lead), MES, MYM, M2K, MGC and 7 more", scope="Zarattini, Aziz and Barbon (2024) rule · frozen tests 2021 to 2026",
        idea="Build a band around the open from the average move at each minute over the last 14 days. Trade only when price leaves the band and is on the same side of VWAP; otherwise stay flat.",
        tested=["The published rule, unchanged, on MNQ (with MES as a control).", "The same rule on the other index micros, on Tokyo and London sessions, and on seven more markets."],
        results="""<ul>
<li>MNQ, New York hours: the closest thing to a lead this desk has found. Details on the <a href="/research/under-observation/">Under observation</a> page.</li>
<li>MES control: &minus;$4.16 per trade. MYM: &minus;$1.71. M2K: &minus;$5.27.</li>
<li>Tokyo and London anchors: no edge on MNQ or MGC.</li>
<li>Seven other markets (MYM, M2K, SIL, PL, MCL, MHG, M6E): 0 of 7 profitable, &minus;$18,326 combined.</li>
</ul>""",
        verdict="Under observation on MNQ only (formally insufficient evidence). No edge on every other market and session tested.",
        lesson="When an effect shows up on one market and nowhere else, treat that as a warning, not as confirmation.",
    ),
    dict(
        slug="box-breakouts", name="Consolidation box breakouts", status="no-edge", group="Price action and levels",
        markets="MNQ, MES, MGC", scope="1m and 5m · 12m search · 4-month untouched check",
        idea="Detect a tight consolidation box, then trade the breakout or the failed breakout back into the box.",
        tested=["Grid search on the last 12 months, random-direction null, walk-forward.", "One run of the frozen picks on an untouched 4-month window."],
        results="""<table><thead><tr><th>Market</th><th>Null percentile (0.95 needed)</th><th>Untouched 4 months</th></tr></thead><tbody>
<tr><td>MNQ</td><td>0.27</td><td>161 trades · &minus;$180</td></tr>
<tr><td>MES</td><td>0.21</td><td>133 trades · &minus;$559</td></tr>
<tr><td>MGC</td><td>0.46</td><td>114 trades · &minus;$2,282</td></tr>
</tbody></table>""",
        verdict="No edge found. Formally insufficient evidence, because four months is too short to rule an edge out completely.",
        lesson="A pick that sits inside its random-direction null has nothing to explain. Further tuning cannot fix that.",
    ),
    dict(
        slug="volume-profile", name="Volume profile levels", status="no-edge", group="Price action and levels",
        markets="MNQ, MES, MGC", scope="POC, VAH, VAL, high and low volume nodes · 3,456 settings",
        idea="Trade rejections or acceptance at volume-profile levels built from sessions, consolidation boxes or the previous 4-hour candle.",
        tested=["3,456 settings, random-direction null with 1,000 seeds, walk-forward, untouched 4-month check.", "Shifted fake levels as a placebo."],
        results="""<ul>
<li>Before costs, the average result was about zero in all 40 level and trigger groups.</li>
<li>All three picks sat inside their null, walk-forward failed 3 of 3, and the untouched check lost on all three (&minus;$12, &minus;$535, &minus;$398).</li>
<li>Shifted fake levels did as well as the real ones.</li>
</ul>""",
        verdict="No edge. Family closed in this scope.",
        lesson="If fake levels work as well as real ones, the levels are not the reason for the result.",
    ),
    dict(
        slug="amd-1h4h", name="1h and 4h AMD (accumulation, manipulation, distribution)", status="no-edge", group="Price action and levels",
        markets="MNQ, MES, MGC", scope="4 session anchors × 1h/4h × 2 triggers × 4 targets × 2 deadlines",
        idea="The first hour or four hours build a range (accumulation), a sweep of one side is the manipulation, and the reclaim starts the real move (distribution).",
        tested=["128 settings per market, ranked on the last 6 months of a 12-month window.", "200-seed random-direction null, walk-forward, untouched 4-month check."],
        results="""<ul>
<li>0 of 3 picks survived. Walk-forward failed on all three.</li>
<li>Untouched check, average per trade: MNQ &minus;0.56R, MES &minus;0.45R, MGC &minus;0.14R.</li>
</ul>""",
        verdict="No edge on MNQ and MGC. MES is formally insufficient evidence (only 21 trades in the check).",
        lesson="A popular narrative is not a mechanism. It has to be written as exact rules before it can be tested at all.",
    ),
    dict(
        slug="short-timeframe-trend", name="Short-timeframe trend following", status="exploratory", group="Trend and momentum",
        markets="MNQ, MES, MGC", scope="1m to 5m · EMA slope, N-bar breakout, strong bar · 504 settings",
        idea="Join short intraday trends early with a trailing or time-based exit.",
        tested=["504 settings with a gross check before costs.", "1,000-seed random-direction null, walk-forward, untouched 4-month check."],
        results="""<ul>
<li>1- and 2-minute signals had no gross edge on any market, so costs made them negative.</li>
<li>MNQ 5m 'strong bar' continuation looked best in exploration (+$8,061 over 381 trades, in-sample) but missed the full null (0.932), and its walk-forward pick lost.</li>
<li>Untouched check: +0.047R per trade with an interval from &minus;0.11R to +0.20R. All the profit came from 5 days.</li>
</ul>""",
        verdict="Exploratory. Formally insufficient evidence on MNQ and MES; no pick on MGC.",
        lesson="When five days make all the profit, the result describes those five days, not a repeatable rule.",
    ),
    dict(
        slug="microstructure-effects", name="Volume shocks and 1-minute reversals", status="unsuitable", group="Real but untradeable",
        markets="MGC, MNQ, MES", scope="1m bars · several studies",
        idea="Small, short-lived effects around abnormal volume and very short moves.",
        tested=["Reversal after abnormal-volume shocks.", "1-minute bounce after sharp bars.", "MNQ continuation after large moves away from the open.", "Passive limit orders around the last price."],
        results="""<ul>
<li>MGC after volume shocks: a real reversal of about 0.1 to 0.2 points, against a 0.78-point cost hurdle.</li>
<li>The 1-minute bounce turned out to be the bid-ask bounce, which you cannot capture with market orders.</li>
<li>MNQ continuation after large moves from the open: real before costs, but 83 to 87% of it came from the top 10 days.</li>
<li>Passive limits: filled mostly when price was about to go against them (adverse selection).</li>
</ul>""",
        verdict="Real effects, currently unsuitable. They exist in the data but are smaller than the cost of trading them, or too concentrated to rely on.",
        lesson="A statistically real effect and a tradeable edge are different things. The cost of the round trip decides.",
    ),
    dict(
        slug="cross-market-portfolio", name="14-strategy cross-market portfolio", status="no-edge", group="Portfolio",
        markets="MGC, MES, MYM, MNQ, SIL, PL, M2K, MCL, MHG, M6E", scope="The 14 best opening range and Initial Balance picks, run together · 1 micro each",
        idea="Individually weak strategies on different markets, combined with risk managed at portfolio level, might add up to something steady.",
        tested=["The 14 frozen picks combined, settings never changed.", "Replay on 2021 to 2025, data none of them was chosen on.", "Also: a 'best 5 of 14' subset and a cross-market gap fade held for hours."],
        results="""<table><thead><tr><th></th><th>Last 12 months (where picks were chosen)</th><th>2021 to 2025 (unseen)</th></tr></thead><tbody>
<tr><td>Net, after costs</td><td>+$89,458</td><td>&minus;$31,794</td></tr>
<tr><td>Max drawdown</td><td>$1,549</td><td>$34,196</td></tr>
<tr><td>Win rate</td><td>75.5%</td><td>below 75% on most picks</td></tr>
<tr><td>Picks making money</td><td>14 of 14</td><td>1 of 14 (+$77)</td></tr>
<tr><td>Years making money</td><td></td><td>0 of 5</td></tr>
</tbody></table>
<p>The left column is the best of many thousands of combinations on the same year, so it is in-sample by construction. The 'best 5' subset lost &minus;$9,641. The cross-market gap fade lost on all 9 versions.</p>""",
        verdict="No edge. Combining picks diversified the risk but could not create an edge the single picks did not have.",
        lesson="Fourteen small losers add up to one large loser. Diversification reduces noise; it cannot turn a zero edge into a positive one.",
    ),
]

ALSO_TESTED = [
    "Round numbers, Donchian channels, floor-pivot crosses and prior-day value area",
    "Session VWAP stretch fades",
    "Opening gaps, economic release minutes and fixed-clock session moves",
    "London gold fix and COMEX settlement, FX fix on Euro FX micros",
    "Metals late-day reversal and MNQ first-30-minute fade",
    "Volatility regime filters (GARCH) on existing picks",
    "AI time-series forecast filters (Kronos, TiRex, Toto) as take-or-skip filters",
    "Position sizing rules: anti-martingale, equity steps, percent risk, Kelly-style",
]


def family_page(page, f, prev_f, next_f):
    tested = "".join(f"<li>{t}</li>" for t in f["tested"])
    nav = '<nav class="fam-nav" aria-label="More families">'
    if prev_f:
        nav += f'<a href="/research/backtested/{prev_f["slug"]}/"><span>Previous</span>{prev_f["name"]}</a>'
    else:
        nav += "<span></span>"
    if next_f:
        nav += f'<a class="next" href="/research/backtested/{next_f["slug"]}/"><span>Next</span>{next_f["name"]}</a>'
    nav += "</nav>"
    body = f"""
<header class="article-head"><div class="wrap">
  <a class="eyebrow" href="/research/backtested/" style="text-decoration:none">&larr; Backtested strategies</a>
  <div>{badge(f['status'])}</div>
  <h1>{f['name']}</h1>
  <p class="lede">{f['idea']}</p>
  <p class="meta">Markets: {f['markets']}<br>Scope: {f['scope']}</p>
</div></header>
<article class="prose rs">
  <h2>What was tested</h2>
  <ul>{tested}</ul>
  <h2>What happened</h2>
  {f['results']}
  <p class="note">{COST_NOTE}</p>
  <h2>Verdict</h2>
  <div class="callout"><p>{badge(f['status'])}</p><p>{f['verdict']}</p></div>
  <h2>Lesson</h2>
  <p>{f['lesson']}</p>
  {nav}
  <p class="note">{NFA} See the <a href="/research/method/">method</a> for how every test is run and judged.</p>
</article>
"""
    desc = f"{f['name']}: what was tested, results after costs, and the verdict. {STATUS[f['status']][0]}."
    return page(f"/research/backtested/{f['slug']}/", f["name"], desc, "/research/", body)


# ---------------------------------------------------------------------------------------------------------------
def research_index(page):
    counts = {k: sum(1 for f in FAMILIES if f["status"] == k) for k in STATUS}
    reasons = [("Wrong direction: no better than a coin flip", 39), ("Too few trades to tell", 15),
               ("Failed a placebo or control", 9), ("Worked in one period only", 8), ("Edge smaller than costs", 7),
               ("Same idea as one already closed", 3), ("Fills only when wrong (limit orders)", 2),
               ("Picked by luck from a big search", 2), ("Backtest artifact", 1)]
    mx = max(n for _, n in reasons)
    bars = "".join(f'<div class="rbar"><span class="rl">{l}</span><span class="rt"><i style="width:{n / mx * 100:.1f}%"></i></span><b>{n}</b></div>' for l, n in reasons)
    body = f"""
<section class="page-head"><div class="wrap">
  <span class="eyebrow">Research desk</span>
  <h1>What we tested, and <span class="gold">why almost all of it failed.</span></h1>
  <p class="lede">A public record of a futures research desk: the rules, the method and the results after costs. Including the failures, which are most of it. Nothing here is a strategy to follow.</p>
</div></section>

<section style="padding-top:12px"><div class="wrap">
  <div class="stats reveal">
    <div><b>0</b><span>strategies passed final validation</span></div>
    <div><b>{len(FAMILIES)}</b><span>strategy families written up here</span></div>
    <div><b>86</b><span>closed ideas in the failure log</span></div>
    <div><b>10</b><span>futures markets, 1-minute data</span></div>
  </div>
  <div class="callout" style="margin-top:28px;max-width:860px"><p><strong>The headline.</strong> No strategy on this desk has passed final validation. The closest lead is <a href="/research/under-observation/">under observation</a>, and it fails the desk's own risk limits even if it holds up. Everything else is published so you don't have to spend months finding the same dead ends.</p></div>
</div></section>

<section><div class="wrap">
  <div class="grid-3">
    <a class="card reveal" href="/research/method/"><div class="icon">{ICON_SCALE}</div><h3>Method</h3><p>Two tracks, one gate. How ideas are explored, frozen and judged, and why a 75% win rate is never the goal.</p><span class="go">Read the method</span></a>
    <a class="card reveal" href="/research/backtested/"><div class="icon">{ICON_STONE}</div><h3>Backtested strategies</h3><p>One page per family: the idea, the markets, the results after costs, the verdict and the lesson.</p><span class="go">See the backtests</span></a>
    <a class="card reveal" href="/research/lessons/"><div class="icon">{ICON_BOOK}</div><h3>Lessons</h3><p>What the failures taught: over-fitting, fill artifacts, costs and effects that fade.</p><span class="go">Read the lessons</span></a>
  </div>
</div></section>

<section class="band"><div class="wrap split">
  <div class="sec-head" style="margin:0">
    <span class="eyebrow">Why ideas fail</span>
    <h2>The main reason each idea was closed.</h2>
    <p class="lede">From the desk's failure log of 86 closed ideas. Most did not fail on costs or bad luck. They had no directional edge to begin with.</p>
    <div class="hero-actions"><a class="btn" href="/research/backtested/">See every family</a></div>
  </div>
  <div class="figure reveal"><div class="rbars">{bars}</div><figcaption>Primary failure reason per closed idea, as of {RESEARCH_UPDATED}.</figcaption></div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><span class="eyebrow">How to read the labels</span><h2>Every result carries a status.</h2></div>
  <div class="principles">
    <div class="principle"><b>{STATUS['no-edge'][0]}</b><span>Tested properly, no edge after costs. {counts['no-edge']} families.</span></div>
    <div class="principle"><b>{STATUS['exploratory'][0]}</b><span>Something worth a look, not enough evidence. {counts['exploratory']} families.</span></div>
    <div class="principle"><b>{STATUS['unsuitable'][0]}</b><span>The effect exists in the data but costs or concentration make it untradeable. {counts['unsuitable']} family.</span></div>
    <div class="principle"><b>{STATUS['observe'][0]}</b><span>The closest lead. Being tracked on new data with no changes. {counts['observe']} family.</span></div>
  </div>
  <p class="note" style="margin-top:28px;max-width:860px">{NFA} Market data comes from a licensed 1-minute futures feed and is not redistributed here; only rules, methods and summary results are published.</p>
</div></section>
"""
    return page("/research/", "Research", "A public futures research record: method, backtested strategies with results after costs, and lessons. No strategy has passed validation.", "/research/", body)


def graveyard(page):
    groups = []
    for g in ["Opening range and session", "Price action and levels", "Trend and momentum", "Real but untradeable", "Portfolio"]:
        fs = [f for f in FAMILIES if f["group"] == g]
        cards = []
        for f in fs:
            cards.append(f"""<a class="card fam reveal" href="/research/backtested/{f['slug']}/">
  {badge(f['status'])}
  <h3>{f['name']}</h3>
  <p>{f['verdict'].split('. ')[0].rstrip('.')}.</p>
  <span class="fam-mk">{f['markets']}</span>
</a>""")
        groups.append(f'<h2 class="grp">{g}</h2><div class="grid-3">{"".join(cards)}</div>')
    also = "".join(f"<li>{a}</li>" for a in ALSO_TESTED)
    body = f"""
<section class="page-head"><div class="wrap">
  <a class="eyebrow" href="/research/" style="text-decoration:none">&larr; Research</a>
  <h1>Backtested <span class="gold">strategies.</span></h1>
  <p class="lede">Every family the desk tested, one page each: the idea, the markets, what was run, the results after costs, the verdict and the lesson. Optimised numbers are always labelled in-sample.</p>
</div></section>
<section style="padding-top:12px"><div class="wrap">
  {"".join(groups)}
  <h2 class="grp">Also tested and closed</h2>
  <div class="prose" style="margin:0;padding:0;max-width:860px"><ul>{also}</ul>
  <p class="note">{COST_NOTE} {NFA}</p></div>
</div></section>
"""
    return page("/research/backtested/", "Backtested strategies", "Every futures strategy family tested by the Badr Edge research desk, with results after costs and a verdict for each.", "/research/", body)


def method(page):
    body = f"""
<header class="article-head"><div class="wrap">
  <a class="eyebrow" href="/research/" style="text-decoration:none">&larr; Research</a>
  <h1>Method: two tracks, one gate.</h1>
  <p class="lede">Most backtests are built to look good. This process is built to find out whether an idea survives data it has never seen, after real costs.</p>
  <p class="meta">Updated {RESEARCH_UPDATED}</p>
</div></header>
<article class="prose rs">
  <h2>Track 1: explore</h2>
  <p>New ideas are explored on the most recent 12 months (22 Oct 2025 to 21 Oct 2026). Grid searches are allowed here, and anything found here is labelled <strong>in-sample</strong>. An in-sample result is a hypothesis, never evidence, because the best of thousands of settings will always look good on the data it was picked from.</p>
  <p>Before an idea moves on, it has to pass three cheap checks:</p>
  <ul>
    <li><strong>Gross check, both directions.</strong> The raw signal is measured before costs, on the real side and on the flipped side. If both lose before costs, the idea stops.</li>
    <li><strong>Random-direction null.</strong> The whole search is rerun many times with random trade directions, using the same times, stops and costs. The real pick has to beat at least 95% of these random picks. This one check caught every over-fitted strategy on this desk.</li>
    <li><strong>Walk-forward.</strong> Pick the best setting on the first half of the window, then trade it unchanged on the second half.</li>
  </ul>

  <h2>Track 2: confirm on frozen data</h2>
  <p>The rules are written down, hashed and committed before the test (pre-registration). They are then run <strong>once</strong> on four earlier years, 22 Oct 2021 to 21 Oct 2025, that the idea was never tuned on. Nothing is changed after the result. If it fails, that window is spent for that idea.</p>

  <h2>The Validator gate</h2>
  <p>A separate reviewer role decides the verdict. The researcher who built the idea does not. The gate checks:</p>
  <ul>
    <li><strong>Independent rebuild.</strong> Trades are rebuilt from raw bars with separate code and must match.</li>
    <li><strong>Holm correction.</strong> When several versions are tested together, the significance bar is raised so one lucky version cannot pass.</li>
    <li><strong>Minimum meaningful effect and power,</strong> set before the run. An edge too small to cover costs and the risk budget does not count, even if it is statistically real.</li>
    <li><strong>Cost stress.</strong> 2x and 3x slippage, and fees +50%.</li>
    <li><strong>Year-by-year consistency</strong> and both unseen sub-periods positive.</li>
    <li><strong>Concentration.</strong> The best 10 days may not carry more than half the profit.</li>
    <li><strong>Placebo controls.</strong> Level-based ideas are rerun on fake levels; confluence ideas on fake zones.</li>
  </ul>
  <p>Verdicts are <strong>PASS</strong>, <strong>NO EDGE</strong> or <strong>INSUFFICIENT EVIDENCE</strong> (when the test did not have enough trades to rule an edge out). No idea has received a PASS.</p>

  <h2>Acceptance: a separate, later filter</h2>
  <p>Even a PASS would still have to meet the desk's practical limits before it could be considered. These limits are a filter at the end, <strong>never a research target</strong>:</p>
  <table><thead><tr><th>Rule</th><th>Limit</th></tr></thead><tbody>
    <tr><td>Win rate</td><td>at least 75%</td></tr>
    <tr><td>Max drawdown, 1 contract</td><td>$2,000</td></tr>
    <tr><td>Profit target</td><td>$3,000</td></tr>
    <tr><td>Trading hours</td><td>01:00 to 22:00 GMT+3, flat by the end, no overnight holds</td></tr>
    <tr><td>Size in tests</td><td>1 micro (1 contract for platinum), no compounding</td></tr>
  </tbody></table>
  <div class="callout"><p><strong>Why the 75% win-rate bar is never optimised for.</strong> When the random-direction pipeline was run, its own best picks showed 77 to 92% win rates on 12 months. A high win rate with a small target is what a search produces by default. Ranking on win rate selects luck.</p></div>

  <h2>Costs used in every test</h2>
  <p>Fees per round turn plus one tick of slippage on each side for market and stop orders. Limit orders need price to trade one tick through before they count as filled.</p>
  <table><thead><tr><th>Market</th><th>Tick value</th><th>Fee per round turn</th><th>Base round trip</th></tr></thead><tbody>
    <tr><td>MGC micro gold</td><td>$1.00</td><td>$1.92</td><td>$3.92</td></tr>
    <tr><td>MES micro S&amp;P 500</td><td>$1.25</td><td>$1.22</td><td>$3.72</td></tr>
    <tr><td>MNQ micro Nasdaq-100</td><td>$0.50</td><td>$1.22</td><td>$2.22</td></tr>
    <tr><td>MYM micro Dow</td><td>$0.50</td><td>$1.22</td><td>$2.22</td></tr>
    <tr><td>M2K micro Russell</td><td>$0.50</td><td>$1.22</td><td>$2.22</td></tr>
    <tr><td>SIL micro silver</td><td>$5.00</td><td>$2.72</td><td>$12.72</td></tr>
    <tr><td>PL platinum</td><td>$5.00</td><td>$4.32</td><td>$14.32</td></tr>
    <tr><td>MCL micro crude</td><td>$1.00</td><td>$1.72</td><td>$3.72</td></tr>
    <tr><td>MHG micro copper</td><td>$1.25</td><td>$1.92</td><td>$4.42</td></tr>
    <tr><td>M6E micro EUR/USD</td><td>$1.25</td><td>$1.00</td><td>$3.50</td></tr>
  </tbody></table>
  <p class="note">Slippage of one tick is a convention, not a measurement. Current fee rates are applied to older years.</p>

  <h2>Data</h2>
  <p>1-minute bars for ten CME Globex futures markets, from a licensed data vendor, checked against TradingView. Contracts roll to the daily volume leader. The licence does not allow redistribution, so no raw data is published here, only rules and summary results.</p>

  <p class="note">{NFA}</p>
</article>
"""
    return page("/research/method/", "Research method", "How the Badr Edge research desk tests futures strategies: explore, pre-register, freeze, validate. Costs, nulls, Holm correction and acceptance rules.", "/research/", body)


def lessons(page):
    items = [
        ("In-sample optimisation fools you", "The 14 best opening range and Initial Balance picks made +$89,458 together on the year they were chosen from, with a $1,549 drawdown and a 75.5% win rate. On four earlier years they lost &minus;$31,794 with a $34,196 drawdown. Search hard enough on one year and something will always look great on that year.", "/research/backtested/cross-market-portfolio/"),
        ("Run the random-direction null first", "Rerun the whole search with random directions. If your best pick does not beat 95% of the random picks, it was selected by luck. This check caught every over-fitted strategy on the desk; simple replication checks caught none of them.", "/research/method/"),
        ("The limit fill-bar artifact", "A backtest that fills a limit order and hits the target on the same bar is counting a trade that may never have happened. Early high-win-rate, small-target results came from this. Now the target only counts from the bar after the fill, and any high win rate with a small target is treated as a bug until it is replicated.", None),
        ("Drawdown caps must allow 'no pick'", "A risk limit is a hard filter. When nothing fits under the $2,000 drawdown cap, the answer is no strategy, not the closest one. A soft cap once let a pick through with a $3,763 drawdown.", None),
        ("Costs exceed gross edge on most retail setups", "Many popular setups make between $0.10 and $2 per trade before costs. A micro contract round trip costs $2.20 to $3.90 here. Compare average gross profit per trade with the round-trip cost before anything else, and flag anything under about twice the cost.", "/research/backtested/ema-vwap-momentum/"),
        ("Effects decay", "The published first-half-hour to last-half-hour momentum effect measured +0.15 in 2021, +0.07 in 2022, about zero in 2023 and negative since 2024. A paper's full-period average can hide an effect that has already gone.", "/research/backtested/intraday-momentum/"),
        ("A high win rate is not an edge", "One Initial Balance pick kept a 76% win rate on unseen years and still lost $2,733. Small targets win often; a few full stops take it back. Never rank on win rate.", "/research/backtested/initial-balance/"),
        ("Check both directions before costs", "If the real side and the flipped side both lose before costs, no filter, exit or sizing rule will rescue the idea. Key-level retests failed this on 36 of 36 groups.", "/research/backtested/key-level-retests/"),
        ("Use placebos for levels and confluence", "Fake levels, fake strikes and shifted zones did as well as the real ones for volume profile and options walls. Ablations (removing one part at a time) are not enough.", "/research/backtested/volume-profile/"),
        ("Sizing scales risk, not edge", "Fixed size, percent risk, equity steps, anti-martingale and Kelly-style rules all left the net per contract about the same. Streak-based rules were worse than fixed size, and percent-risk sizing loaded up on the worst, narrow-stop trades.", None),
        ("Watch concentration", "When the best 10 days carry most of the profit, the result describes those days. The closest lead on this desk has 98% of its profit in its top 10 days.", "/research/under-observation/"),
        ("Low-frequency ideas run out of power", "An idea that trades about once a week cannot be confirmed or rejected on a few years of data. Calculate the power before the test, and close the idea honestly as 'insufficient evidence' when it is too low.", None),
        ("Combining weak strategies doesn't create an edge", "Diversification smooths noise but cannot turn many zero-edge strategies into one positive edge. Fourteen small losers made one large loser.", "/research/backtested/cross-market-portfolio/"),
        ("Fixed-clock rules change with the seasons", "Rules on fixed GMT+3 times shift by an hour against New York when US daylight saving changes. The noise-area lead made about $23 per trade in summer and about $2 in winter.", None),
    ]
    cards = ""
    for i, (h, p, link) in enumerate(items, 1):
        more = f' <a href="{link}">See the evidence</a>.' if link else ""
        cards += f'<div class="lesson reveal"><span class="ln">{i:02d}</span><div><h3>{h}</h3><p>{p}{more}</p></div></div>'
    body = f"""
<section class="page-head"><div class="wrap" style="max-width:860px">
  <a class="eyebrow" href="/research/" style="text-decoration:none">&larr; Research</a>
  <h1>Lessons from <span class="gold">the failures.</span></h1>
  <p class="lede">What months of tests with no validated edge taught. Each one changed how the next test was run.</p>
</div></section>
<section style="padding-top:12px"><div class="wrap" style="max-width:860px">
  <div class="lessons">{cards}</div>
  <p class="note" style="margin-top:32px">{COST_NOTE} {NFA}</p>
</div></section>
"""
    return page("/research/lessons/", "Research lessons", "Lessons from a futures research desk with no validated edge: over-fitting, fill artifacts, costs, placebo tests and effect decay.", "/research/", body)


def under_observation(page):
    body = f"""
<header class="article-head"><div class="wrap">
  <a class="eyebrow" href="/research/" style="text-decoration:none">&larr; Research</a>
  <div>{badge('observe')}</div>
  <h1>Noise-area momentum on MNQ</h1>
  <p class="lede">The closest thing to a lead this desk has found. It is <strong>not validated</strong>, it fails the desk's own risk limits, and it is published here only as a research note being watched on new data.</p>
  <p class="meta">Formal verdict: INSUFFICIENT EVIDENCE · Market: MNQ, New York hours · Updated {RESEARCH_UPDATED}</p>
</div></header>
<article class="prose rs">
  <h2>The rule</h2>
  <p>This is the published rule from Zarattini, Aziz and Barbon (2024), tested exactly as written with nothing tuned:</p>
  <ul>
    <li>For each minute of the New York session, measure the average absolute move from the open over the previous 14 sessions. That builds a 'noise area' band around the open.</li>
    <li>Every half hour from 10:00 to 15:30 New York time, be long if price is above the band and above session VWAP, short if below both, and flat otherwise.</li>
    <li>Flat by 22:00 GMT+3 at the latest. One micro contract, no leverage scaling.</li>
  </ul>

  <h2>The frozen test</h2>
  <p>Rules were written and hashed before the run. It was run once on July 2023 to October 2026, a window never used for this rule.</p>
  <table><thead><tr><th>Measure</th><th>MNQ</th><th>MES (control)</th></tr></thead><tbody>
    <tr><td>Trades</td><td>590</td><td>655</td></tr>
    <tr><td>Net after costs</td><td>+$9,884</td><td>&minus;$2,724</td></tr>
    <tr><td>Net per trade</td><td>+$16.75</td><td>&minus;$4.16</td></tr>
    <tr><td>Win rate</td><td>42%</td><td>38%</td></tr>
    <tr><td>Max drawdown (closed trades)</td><td>$2,615</td><td>$3,796</td></tr>
    <tr><td>Random-direction percentile</td><td>0.970</td><td>0.456</td></tr>
    <tr><td>Per trade at 2x slippage</td><td>+$15.75</td><td></td></tr>
  </tbody></table>
  <p>Every calendar year in the window was positive on MNQ, and both long and short sides made money.</p>

  <h2>Why it is not validated</h2>
  <ul>
    <li><strong>Missed the Holm bar.</strong> p = 0.0135 against a required 0.0125. Close is not a pass.</li>
    <li><strong>Concentrated.</strong> The top 10 days carried 98% of the net profit. The limit is 50%.</li>
    <li><strong>Drawdown too large.</strong> $2,615 for one micro, above the $2,000 limit.</li>
    <li><strong>Win rate 42%,</strong> far below the 75% acceptance bar.</li>
    <li><strong>Market-specific.</strong> The same rule lost on MES, MYM, M2K and seven other markets, and on Tokyo and London sessions.</li>
    <li><strong>Season-dependent.</strong> About +$23 per trade in summer and +$2 in winter, because the fixed GMT+3 exit moves against New York time.</li>
  </ul>
  <div class="callout"><p><strong>Status: under observation.</strong> Even if later data confirmed the effect, it would be 'real but currently unsuitable' under the desk's risk limits. It is not a recommendation and not a signal.</p></div>

  <h2>What happens next</h2>
  <p>The frozen rule is logged on new data from 22 October 2026, with no changes. A handful of weeks proves nothing either way: at roughly 180 trades a year, one year of new data alone cannot settle it. The plan is to pool new data with the frozen window and re-judge it under the same pre-registered rules.</p>

  <p class="note">{COST_NOTE}</p>
  <p class="note">{NFA}</p>
</article>
"""
    return page("/research/under-observation/", "Under observation: noise-area MNQ", "The closest lead on the Badr Edge research desk, noise-area momentum on MNQ, and why it is not validated.", "/research/", body)


ICON_SCALE = ICON_STONE = ICON_BOOK = ""


def build_all(page, icons):
    global ICON_SCALE, ICON_STONE, ICON_BOOK
    ICON_SCALE = icons["scale"]
    ICON_BOOK = icons["book"]
    ICON_STONE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
                  'stroke-linejoin="round"><path d="M6 21V10a6 6 0 0 1 12 0v11"/><path d="M4 21h16M12 9v6M9.5 12h5"/></svg>')
    built = [research_index(page), method(page), graveyard(page), lessons(page), under_observation(page)]
    for i, f in enumerate(FAMILIES):
        built.append(family_page(page, f, FAMILIES[i - 1] if i else None, FAMILIES[i + 1] if i + 1 < len(FAMILIES) else None))
    return built
