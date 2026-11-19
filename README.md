# Badr Edge website

Static site for badredge.com, deployed by Cloudflare Pages from `main`.

No build step: Cloudflare serves the files as they are. Keep strategies, backtests and performance results out of this public repo.

## Maintenance scripts

Run from the repo root. The last three need Playwright; the clips also need ffmpeg.

- `cd _src && PYTHONDONTWRITEBYTECODE=1 python3 build.py && python3 tool_bar.py` rebuilds the pages and the simulators' header, share card and clip button.
- `node _src/og/render.js` renders one share card per page into `assets/og/` (list in `_src/og/cards.json`, written by the build).
- `node _src/clips/record.js` records the simulators' "See it run" clips into `assets/clips/`.
- `node _src/check/site_check.js` opens every page on phone and desktop, dark and light, and lists anything broken.
