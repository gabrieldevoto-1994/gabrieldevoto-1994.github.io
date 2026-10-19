"""Check the rendered site in _site/ before publishing.

Run from the project folder, after `quarto render`:
    python tools/check_site.py            # check the local build
    python tools/check_site.py --live     # check https://gabrieldevoto.com instead

What it does:
  * serves _site/ on a free local port (stops by itself at the end)
  * screenshots light + dark mode at 1280px (desktop) and 375px (phone)
  * fails if the page scrolls sideways or the buttons / title line overflow
  * checks every link on the page (CV, papers, buttons)

Screenshots go to your temp folder (never into the project); the path is printed.
Exit code 0 = all good, 1 = something to fix.

Needs: pip install playwright   (uses the installed Google Chrome; if Chrome is
missing, run `python -m playwright install chromium` and pass --bundled)
"""
import functools
import http.server
import re
import sys
import tempfile
import threading
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
OUT = Path(tempfile.gettempdir()) / "gabrieldevoto-check"
OUT.mkdir(exist_ok=True)

live = "--live" in sys.argv
problems = []

# ---- serve _site locally -------------------------------------------------
server = None
if live:
    base = "https://gabrieldevoto.com/"
else:
    if not (SITE / "index.html").exists():
        sys.exit("No _site/index.html: run `quarto render` first.")
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(QuietHandler, directory=str(SITE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}/"
print(f"Checking {base}")

# ---- layout checks + screenshots ----------------------------------------
LAYOUT_JS = """() => {
  const vw = window.innerWidth;
  const over = sel => [...document.querySelectorAll(sel)].filter(e => {
    const b = e.getBoundingClientRect(); return b.left < -1 || b.right > vw + 1; }).length;
  return {
    scrollWidth: document.documentElement.scrollWidth, viewport: vw,
    buttonsOff: over('.about-link'), titleOff: over('h1.title, p.subtitle'),
    links: [...document.querySelectorAll('a[href]')].map(a => a.href),
  };
}"""

links = set()
with sync_playwright() as p:
    browser = p.chromium.launch() if "--bundled" in sys.argv else p.chromium.launch(channel="chrome")
    for scheme in ("light", "dark"):
        for width, mobile in ((1280, False), (375, True)):
            ctx = browser.new_context(viewport={"width": width, "height": 900},
                                      is_mobile=mobile, has_touch=mobile,
                                      device_scale_factor=1, color_scheme=scheme)
            page = ctx.new_page()
            page.goto(base, wait_until="networkidle")
            page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
            r = page.evaluate(LAYOUT_JS)
            links.update(r["links"])
            shot = OUT / f"{scheme}_{width}.png"
            page.screenshot(path=str(shot), full_page=True)
            tag = f"{scheme} {width}px"
            ok = True
            if r["scrollWidth"] > r["viewport"]:
                problems.append(f"{tag}: page scrolls sideways ({r['scrollWidth']}px wide on a {r['viewport']}px screen)"); ok = False
            if r["buttonsOff"]:
                problems.append(f"{tag}: {r['buttonsOff']} button(s) run off the screen"); ok = False
            if r["titleOff"]:
                problems.append(f"{tag}: name or title line runs off the screen"); ok = False
            print(f"  {'OK ' if ok else 'BAD'} {tag:12} -> {shot}")
            ctx.close()
    browser.close()

# ---- link checks ----------------------------------------------------------
print("Links:")
for url in sorted(links):
    if url.startswith("mailto:"):
        print(f"  OK  {url}"); continue
    if not url.startswith("http") or re.search(r"#", url) and url.split("#")[0] == base:
        continue
    if "linkedin.com" in url:
        print(f"  ??  {url}  (LinkedIn blocks automated checks; click it once by hand)"); continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        code = urllib.request.urlopen(req, timeout=20).status
    except Exception as e:
        code = getattr(e, "code", type(e).__name__)
    ok = code == 200
    print(f"  {'OK ' if ok else 'BAD'} {url}  ({code})")
    if not ok:
        problems.append(f"link does not open: {url} ({code})")

if server:
    server.shutdown()

print()
if problems:
    print("PROBLEMS:")
    for pr in problems:
        print("  - " + pr)
    sys.exit(1)
print("All checks passed.")
