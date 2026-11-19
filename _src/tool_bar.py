"""Keep the three standalone simulators in the site's header.

The simulators under /tools/<name>/ are hand-built pages that build.py does not
generate. This script rewrites only their header block (between the be:bar
markers) so the menu matches the main site's NAV. Run it after changing NAV:

    PYTHONDONTWRITEBYTECODE=1 python3 _src/tool_bar.py
"""
import os, re
from build import NAV, THEME_BTN, ROOT, og_image

TOOLS = {"pass": "", "payout": "", "sizing": " be-bar--inset"}   # sizing pads <body>, so its bar bleeds out to the edges
FONTS = "https://fonts.googleapis.com/css2?family=Manrope:wght@400..800&family=IBM+Plex+Mono:wght@400;500;600&display=swap"
MENU_JS = ("<script>(function(){var b=document.querySelector('.be-menu'),n=document.getElementById('be-nav');"
           "if(b&&n)b.addEventListener('click',function(){var o=n.classList.toggle('open');"
           "b.setAttribute('aria-expanded',o);b.textContent=o?'Close':'Menu';});})();</script>")


def bar(extra):
    links = [f'<a href="{href}"{" class=\"be-hl\"" if i == 0 else ""}>{label}</a>' for i, (href, label) in enumerate(NAV)]
    links.insert(1, '<a class="be-cta" href="/tools/" aria-current="page"><i class="be-dot"></i>Open the tools</a>')
    return (f'<nav class="be-bar{extra}" aria-label="Site"><div class="be-in">\n'
            '  <a class="be-brand" href="/" aria-label="Badr Edge home"><span class="be-moon" aria-hidden="true"></span>'
            '<span class="be-word">Badr <span>Edge</span></span></a>\n'
            f'  <div class="be-nav" id="be-nav">{"".join(links)}</div>\n'
            f'  <span class="be-actions">{THEME_BTN}<button class="be-menu" type="button" aria-expanded="false" aria-controls="be-nav">Menu</button></span>\n'
            f'</div></nav>\n{MENU_JS}\n')


for name, extra in TOOLS.items():
    p = os.path.join(ROOT, "tools", name, "index.html")
    s = open(p, encoding="utf-8").read()
    s, n = re.subn(r'<nav class="be-bar.*?(?=<!-- /be:bar -->)', lambda m: bar(extra), s, count=1, flags=re.S)
    assert n == 1, f"no header block in {p}"
    # one font request, the same families as the main site
    s, n = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Inter\+Tight[^"]*">', f'<link rel="stylesheet" href="{FONTS}">', s)
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n'
               r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Archivo[^"]*">\n', "", s)
    # each simulator shares its own card
    s = re.sub(r'https://badredge\.com/assets/og[-/][a-z-]+\.jpg\?v=\d+', og_image(f"/tools/{name}/"), s)
    open(p, "w", encoding="utf-8").write(s)
    print("header synced:", p)
