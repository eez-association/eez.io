"""Redirect pages for old URLs (GitHub Pages can't send 301s, so each is a small HTML page).

- /use-cases has no page of its own: it forwards to /use-cases/all.
- /old-home (a Framer page) forwards to /.
- The blog stays on Framer, served from blog.eez.io. /blog and every old /blog/<slug> on eez.io
  forward to the same path there, so old links and search results keep working.
A refresh of 0 plus a canonical tag is what Google reads as a permanent move.
Add new posts here only if they were ever published under eez.io/blog.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
BLOG = "https://blog.eez.io"
POSTS = [  # from the eez.io Framer sitemap, 23 Nov 2026
    "monthly-update---october-devcon-mumbai",
    "monthly-update---september",
    "monthly-update-august-2026",
    "introducing-the-eez",
    "monthly-update-digest-july-2026",
    "the-case-for-eez",
    "zkvm-for-next-generation-apps",
]
REDIRECTS = {
    "use-cases/index.html": "/use-cases/all",
    "old-home.html": "/",
    "blog/index.html": f"{BLOG}/blog",
    **{f"blog/{s}.html": f"{BLOG}/blog/{s}" for s in POSTS},
}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>EEZ · Moved</title>
<link rel="canonical" href="{to}">
<meta http-equiv="refresh" content="0; url={to}">
<script>location.replace("{to}" + location.search + location.hash)</script>
</head>
<body><p>This page has moved to <a href="{to}">{to}</a>.</p></body>
</html>
"""


def main():
    for rel, to in REDIRECTS.items():
        f = DIST / rel
        if f.exists():
            raise SystemExit(f"redirects: {rel} is a real page, not overwriting it")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(PAGE.format(to=to))
    print(f"redirects: {len(REDIRECTS)} pages")


if __name__ == "__main__":
    main()
