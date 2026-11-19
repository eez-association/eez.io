#!/usr/bin/env python3
"""Assemble the eez.io + integrate merge demo into dist/.

Sources (fresh clones from GitHub, see README):
  _src/mockup     0xarmagan/eez-website-mockup  -> eez.io home (stands in for Framer)
  _src/integrate  0xarmagan/eez-integrate-site  -> pages under /use-cases, /status, /get-in-touch
Both get one shared header + footer from shared/.
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MOCK = ROOT / "_src/mockup"
INT = ROOT / "_src/integrate/dist"
SH = ROOT / "shared"
OUT = ROOT / "dist"

HEADER = (SH / "header.html").read_text()
FOOTER = (SH / "footer.html").read_text()
GIT_MAIN = (SH / "get-in-touch.main.html").read_text()
DEVCON = (SH / "devcon.html").read_text()
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;800&family=Geist+Mono:wght@400;500&display=swap">')
SHELL_HEAD = '<link rel="stylesheet" href="/_shell/shell.css?v=6">'
SHELL_JS = '<script src="/_shell/shell.js?v=3" defer></script>'

# integrate page -> (new file under dist, new URL)
PAGES = {
    "institutions": ("use-cases/institutions.html", "/use-cases/institutions"),
    "chains": ("use-cases/chains.html", "/use-cases/chains"),
    "dapps": ("use-cases/apps.html", "/use-cases/apps"),
    "infra": ("use-cases/infra.html", "/use-cases/infra"),
    "use-cases": ("use-cases/all.html", "/use-cases/all"),
    "kit": ("use-cases/kit.html", "/use-cases/kit"),
    "scoping": ("use-cases/scoping.html", "/use-cases/scoping"),
    "intake": ("get-in-touch.html", "/get-in-touch"),
}
ASSET_BASE = "/use-cases/"  # integrate's css/js/fonts/data live here


def sub1(pattern, repl, text, flags=re.S):
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"pattern not found: {pattern[:60]}")
    return new


def page_link(m):
    name, rest = m.group(2), m.group(3) or ""
    return f'{m.group(1)}{PAGES[name][1]}{rest}"' if name in PAGES else m.group(0)


def rewrite_integrate(html, url):
    html = sub1(r'<header class="site-head">.*?</header>', DEVCON + HEADER, html)
    html = sub1(r'<footer class="site-foot">.*?</footer>', FOOTER, html)
    # no status page on eez.io: drop the "Full trust model" footnotes that pointed at it
    html = re.sub(r'\s*<div class="footnote"><a class="eez-badge" href="/?status\.html#trust">[^<]*</a></div>', '', html)
    # page links (keep ?query and #hash)
    names = "|".join(map(re.escape, PAGES))
    html = re.sub(rf'((?:href|src)=")/?({names})\.html([?#][^"]*)?"', page_link, html)
    html = html.replace('href="index.html"', 'href="/"')
    # page links inside inline JSON/JS data, e.g. {"l": "institutions.html#use-cases"}
    html = re.sub(rf'"({names})\.html(#[^"]*)?"', lambda m: f'"{PAGES[m.group(1)][1]}{m.group(2) or ""}"', html)
    # favicons -> eez.io's
    html = re.sub(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>', '', html)
    html = html.replace("</head>", '<link rel="icon" type="image/svg+xml" href="/assets/eez-mark.svg">\n</head>', 1)
    # relative assets -> absolute under /use-cases/
    def asset(m):
        ref = m.group(2)
        if re.match(r'(https?:|//|/|#|mailto:|data:|tel:|javascript:|\$\{)', ref):
            return m.group(0)
        return f'{m.group(1)}{ASSET_BASE}{ref}"'
    html = re.sub(r'((?:href|src)=")([^"]+)"', asset, html)
    html = re.sub(r'url\((["\']?)(?!https?:|/|data:|#)([^)"\']+)\1\)', lambda m: f'url({m.group(1)}{ASSET_BASE}{m.group(2)}{m.group(1)})', html)
    html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://eez.io{url}">', html)
    html = re.sub(r'(<meta property="og:url" content=")[^"]*"', rf'\g<1>https://eez.io{url}"', html)
    # Figma: "Talk to us" and "Start the intake" become "Get in touch"
    html = html.replace("Talk to us", "Get in touch").replace("Start the intake", "Get in touch")
    html = html.replace("</head>", f"{FONTS}\n{SHELL_HEAD}\n</head>", 1)
    html = html.replace("</body>", f"{SHELL_JS}\n</body>", 1)
    return html


DOORS = """<div class="auds auds4">
  <div class="aud"><img src="/_shell/inst.svg?v=1" alt="" class="iso"><h3>Institutions</h3><p>Read and call mainnet contracts from your own chain, in the same transaction.</p><a class="pill" href="/use-cases/institutions"><span>For institutions</span><i aria-hidden="true">→</i></a></div>
  <div class="aud"><img src="assets/ops.svg?v=3" alt="" class="iso"><h3>Chains</h3><p>Keep your own rules, provers and proof threshold, and call Ethereum without a bridge.</p><a class="pill" href="/use-cases/chains"><span>For rollup teams</span><i aria-hidden="true">→</i></a></div>
  <div class="aud"><img src="assets/app.svg?v=3" alt="" class="iso"><h3>Apps</h3><p>Use Ethereum's liquidity from a cheap, fast zone without a bridge.</p><a class="pill" href="/use-cases/apps"><span>For app developers</span><i aria-hidden="true">→</i></a></div>
  <div class="aud"><img src="assets/infra.svg?v=3" alt="" class="iso"><h3>Infra</h3><p>Run a follower node, a prover or a block builder, or add EEZ chains to your wallet.</p><a class="pill" href="/use-cases/infra"><span>For infra &amp; wallets</span><i aria-hidden="true">→</i></a></div>
</div>
<style>.auds.auds4{grid-template-columns:repeat(4,minmax(0,1fr))}@media (max-width:980px){.auds.auds4{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:600px){.auds.auds4{grid-template-columns:1fr}}</style>"""


def get_in_touch(html):
    """Figma's one form (Contact frame): intent, about you, team (integrate's scoper), Alliance, message."""
    form = re.search(r'<form class="form" id="scoper".*?</form>', html, re.S).group(0)
    whens = "\n".join(re.findall(r'<div class="field when".*?</div>\s*(?=<div class="field|</form>)', form, re.S))
    main = GIT_MAIN.replace("@@WHEN_BLOCKS@@", whens)
    html = sub1(r'<main id="main" class="wrap">.*?</main>', main, html)
    html = re.sub(r'<script src="https://tally.so/widgets/embed.js"[^>]*></script>', '', html)
    html = re.sub(r'<title>[^<]*</title>', '<title>Get in touch · EEZ</title>', html, count=1)
    return html


def build_home():
    html = (MOCK / "index.html").read_text()
    html = sub1(r'<header class="top">.*?</header>', HEADER, html)
    html = sub1(r'<footer class="foot-site">.*?</footer>', FOOTER, html)
    html = sub1(r'<div class="ctas">.*?</div>',
                '<div class="ctas"><a class="pill solid" href="/use-cases/all"><span>Use cases</span><i aria-hidden="true">→</i></a>'
                '<a class="pill" href="https://build.eez.io/" target="_blank" rel="noopener"><span>Start building</span><i aria-hidden="true">→</i></a></div>', html)
    # "Start where you are": four cards, each opening its use-cases page
    html = sub1(r'<div class="auds">(?:(?!\n).)*?Read the specs</span><i aria-hidden="true">→</i></a></div></div>', DOORS, html)
    # 3: "Join the Alliance" opens Get in touch with the Alliance branch
    html = re.sub(r'<a class="mbtn" href="#">(?=(?:(?!</a>).)*Join the Alliance)', '<a class="mbtn" href="/get-in-touch?intent=alliance">', html, count=1, flags=re.S)
    i = html.find('<section class="sec" id="build">')
    j = html.rfind("</section>", 0, i)
    html = html[:j] + '<a class="more" href="/use-cases/all">All use cases →</a>\n' + html[j:]
    html = html.replace("</head>", f"{SHELL_HEAD}\n</head>", 1).replace("</body>", f"{SHELL_JS}\n</body>", 1)
    return html


def main():
    # keep dist/.vercel (the link to the eez-merge-demo project) across rebuilds
    link = OUT / ".vercel"
    saved = ROOT / ".vercel-link"
    if link.exists():
        shutil.rmtree(saved, ignore_errors=True)
        shutil.move(str(link), saved)
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    if saved.exists():
        shutil.move(str(saved), link)
    shutil.copytree(MOCK / "assets", OUT / "assets")
    shutil.copytree(SH, OUT / "_shell", ignore=shutil.ignore_patterns("*.html"))
    (OUT / "index.html").write_text(build_home())
    # integrate assets (everything except pages) under /use-cases/
    uc = OUT / "use-cases"
    uc.mkdir()
    for p in INT.iterdir():
        if p.suffix == ".html" or p.name in ("sitemap.xml", "robots.txt"):
            continue
        if p.is_dir():
            shutil.copytree(p, uc / p.name)
        else:
            shutil.copy2(p, uc / p.name)
    names = "|".join(map(re.escape, PAGES))
    for js in uc.glob("*.js"):
        t = js.read_text()
        t2 = re.sub(rf"'({names})\.html(#[^']*)?'", lambda m: f"'{PAGES[m.group(1)][1]}{m.group(2) or ''}'", t)
        if t2 != t:
            js.write_text(t2)
    for name, (dest, url) in PAGES.items():
        src = INT / f"{name}.html"
        out = OUT / dest
        out.parent.mkdir(parents=True, exist_ok=True)
        html = src.read_text()
        if name == "intake":
            html = get_in_touch(html)
        out.write_text(rewrite_integrate(html, url))
    (OUT / "vercel.json").write_text(json.dumps({
        "cleanUrls": True, "trailingSlash": False,
        "headers": [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]}],
    }, indent=2))
    print("dist ready:", sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*.html")))
    # match live eez.io on background, one-call diagram and progress timeline
    import runpy; runpy.run_path(str(ROOT / "tools/live_parity.py"), run_name="__main__")
    # agreed copy standards: audience names, chain not zone, devnet, three status labels
    runpy.run_path(str(ROOT / "tools/copy_fixes.py"), run_name="__main__")
    # Infra hero: same line motion as Apps and Chains
    runpy.run_path(str(ROOT / "tools/hero_fixes.py"), run_name="__main__")
    # accessibility and weight fixes from the Impeccable audit
    runpy.run_path(str(ROOT / "tools/audit_fixes.py"), run_name="__main__")
    # curly apostrophes and quotes in visible copy (eez.io uses ’ and “ ”)
    runpy.run_path(str(ROOT / "tools/smart_quotes.py"), run_name="__main__")


if __name__ == "__main__":
    main()
