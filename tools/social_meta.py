"""Link previews (2026-11-20): one set of title, description, canonical, Open Graph and Twitter tags
per page, from tools/og/pages.json. Old tags (and the old integrate-site preview images) are removed
first, so every page ends up with exactly one set. Images are pages/assets/og/<id>.png, made by
tools/og/render.mjs. URLs are written as https://eez.io/...; tools/pages.py points them at the
github.io address until eez.io is served from Pages.
"""
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SITE = "https://eez.io"
OLD = re.compile(r'\s*<(?:meta (?:name|property)="(?:description|og:[a-z:_]+|twitter:[a-z:_]+)"|link rel="canonical")[^>]*>')
TITLE = re.compile(r"<title>[^<]*</title>")


def attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def main():
    pages = json.loads((ROOT / "tools/og/pages.json").read_text())
    for p in pages:
        f = DIST / p["file"]
        img = ROOT / "pages/assets/og" / f"{p['id']}.png"
        if not img.exists():
            sys.exit(f"social_meta: missing {img.relative_to(ROOT)} (run tools/og/render.mjs)")
        html = f.read_text()
        head, sep, rest = html.partition("</head>")
        if not sep or len(TITLE.findall(head)) != 1:
            sys.exit(f"social_meta: {p['file']} needs one <title> in <head>")
        head = OLD.sub("", head)
        url = SITE + p["path"]
        v = hashlib.sha1(img.read_bytes()).hexdigest()[:10]  # new URL when the image changes, so previews refresh
        image = f"{SITE}/assets/og/{p['id']}.png?v={v}"
        alt = f"{p['h']} {p['lite']}"
        t, d = attr(p["title"]), attr(p["description"])
        tags = "\n".join([
            f"<title>{p['title']}</title>",
            f'<meta name="description" content="{d}">',
            f'<link rel="canonical" href="{url}">',
            '<meta property="og:type" content="website">',
            '<meta property="og:site_name" content="EEZ">',
            f'<meta property="og:title" content="{t}">',
            f'<meta property="og:description" content="{d}">',
            f'<meta property="og:url" content="{url}">',
            f'<meta property="og:image" content="{image}">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            f'<meta property="og:image:alt" content="{attr(alt)}">',
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{t}">',
            f'<meta name="twitter:description" content="{d}">',
            f'<meta name="twitter:image" content="{image}">',
        ])
        head = TITLE.sub(lambda m: tags, head, count=1)
        f.write_text(head + sep + rest)
    left = [str(f.relative_to(DIST)) for f in DIST.rglob("*.html") if "integrate-site-chi" in f.read_text()]
    if left:
        sys.exit("social_meta: old preview URLs left in " + ", ".join(left))
    print(f"social meta: {len(pages)} pages")


if __name__ == "__main__":
    main()
