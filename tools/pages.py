#!/usr/bin/env python3
"""Build the GitHub Pages copy of dist/ into _site/.

The site links with root paths (/use-cases/..., /_shell/..., href="/").
A project Pages site is served under /<repo>/, so every root path gets BASE
in front. BASE comes from the environment: "/eez.io" for owner.github.io/eez.io,
"" for a custom domain or an <owner>.github.io repo.
Also adds .nojekyll (Jekyll would drop _shell/). Search engines: on the eez.io build
(SITE_URL=https://eez.io, i.e. the CUSTOM_DOMAIN variable is set) pages stay indexable and
robots.txt + sitemap.xml are written; on any other build (the github.io preview) every page
gets a noindex meta (Pages can't send the X-Robots-Tag header that dist/vercel.json sets)
and robots.txt disallows everything.
Link-preview tags (canonical, og:url, og:image, twitter:image) say https://eez.io; SITE_URL
(e.g. https://eez-association.github.io/eez.io) replaces that while eez.io is not on Pages.
"""
import os, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "dist", ROOT / "_site"
BASE = os.environ.get("BASE", "").rstrip("/")
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")
if BASE and not BASE.startswith("/"):
    sys.exit(f"BASE must start with / (got {BASE!r})")

shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(SRC, OUT, ignore=shutil.ignore_patterns(".vercel", "vercel.json", ".DS_Store"))
(OUT / ".nojekyll").write_text("")

PREFIX = re.compile(r"""(["'(=])/(use-cases|_shell|get-in-touch|assets|brand|media)(?=[/"'?#)\s])""")
HOME = re.compile(r"""((?:href=["']|url=|replace\(["']))/(["'#])""")  # links, refresh and JS redirects to /
PREVIEW = re.compile(r'(<(?:link rel="canonical" href|meta (?:property="og:(?:url|image)"|name="twitter:image") content)=")https://eez\.io(?=[/"])')
NOINDEX = '<meta name="robots" content="noindex, nofollow">'
LIVE = SITE_URL == "https://eez.io"
CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')

count = 0
for f in OUT.rglob("*"):
    if f.suffix not in (".html", ".js", ".css") or "vendor" in f.parts:
        continue
    s = f.read_text()
    t, n1 = PREFIX.subn(lambda m: f"{m[1]}{BASE}/{m[2]}", s)
    t, n2 = HOME.subn(lambda m: f"{m[1]}{BASE}/{m[2]}", t)
    if f.suffix == ".html" and SITE_URL and SITE_URL != "https://eez.io":
        t = PREVIEW.sub(lambda m: m[1] + SITE_URL, t)
    if f.suffix == ".html" and not LIVE and NOINDEX not in t:
        t = t.replace("<head>", "<head>" + NOINDEX, 1)
    if t != s:
        f.write_text(t)
    count += n1 + n2
# sitemap: every real page by its canonical URL (skips 404 and redirect pages)
urls = []
for f in sorted(OUT.rglob("*.html")):
    t = f.read_text()
    if f.name == "404.html" or 'http-equiv="refresh"' in t or "<html" not in t:  # not a page (e.g. Google verification)
        continue
    m = CANON.search(t)
    if not m:
        sys.exit(f"pages: {f.relative_to(OUT)} has no canonical link")
    urls.append(m[1])
if LIVE:
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
else:
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
print(f"_site built, BASE={BASE!r}, SITE_URL={SITE_URL!r}, {count} paths rewritten, "
      f"{'indexable, sitemap ' + str(len(urls)) + ' URLs' if LIVE else 'noindex preview'}")
