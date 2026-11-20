#!/usr/bin/env python3
"""Build the GitHub Pages copy of dist/ into _site/.

The site links with root paths (/use-cases/..., /_shell/..., href="/").
A project Pages site is served under /<repo>/, so every root path gets BASE
in front. BASE comes from the environment: "/eez.io" for owner.github.io/eez.io,
"" for a custom domain or an <owner>.github.io repo.
Also adds a noindex robots meta (Pages can't send the X-Robots-Tag header
that dist/vercel.json sets) and .nojekyll (Jekyll would drop _shell/).
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
HOME = re.compile(r"""(href=["'])/(["'#])""")
PREVIEW = re.compile(r'(<(?:link rel="canonical" href|meta (?:property="og:(?:url|image)"|name="twitter:image") content)=")https://eez\.io(?=[/"])')
NOINDEX = '<meta name="robots" content="noindex, nofollow">'

count = 0
for f in OUT.rglob("*"):
    if f.suffix not in (".html", ".js", ".css") or "vendor" in f.parts:
        continue
    s = f.read_text()
    t, n1 = PREFIX.subn(lambda m: f"{m[1]}{BASE}/{m[2]}", s)
    t, n2 = HOME.subn(lambda m: f"{m[1]}{BASE}/{m[2]}", t)
    if f.suffix == ".html" and SITE_URL and SITE_URL != "https://eez.io":
        t = PREVIEW.sub(lambda m: m[1] + SITE_URL, t)
    if f.suffix == ".html" and NOINDEX not in t:
        t = t.replace("<head>", "<head>" + NOINDEX, 1)
    if t != s:
        f.write_text(t)
    count += n1 + n2
print(f"_site built, BASE={BASE!r}, SITE_URL={SITE_URL!r}, {count} paths rewritten")
