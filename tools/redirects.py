"""Redirect pages for old URLs (GitHub Pages can't send 301s, so each is a small HTML page).

- /use-cases has no page of its own: it forwards to /use-cases/all.
- /old-home (a Framer page) forwards to /.
A refresh of 0 plus a canonical tag is what Google reads as a permanent move.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
REDIRECTS = {
    "use-cases/index.html": "/use-cases/all",
    "old-home.html": "/",
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
