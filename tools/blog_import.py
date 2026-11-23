#!/usr/bin/env python3
"""One-time import of the Framer blog into this repo (23 Nov 2026). Kept as the record of how
blog/ was made; re-running overwrites blog/ and pages/assets/blog/ with what Framer serves now.

For each post at https://blog.eez.io/blog/<slug> it writes:
  blog/posts.json          title, date, category, summary, authors, cover, newest first
  blog/posts/<slug>.html   the post body, reduced to plain tags (p, h2, ul, ol, li, a, strong, em,
                           code, br) plus a YouTube embed where Framer had one
  blog/originals/          cover and author images as downloaded from framerusercontent.com (archive,
                           not served: those URLs stop working once Framer is cancelled)
  pages/assets/blog/       the served copies: JPEG (WebP if transparent), covers at most 1200 px, photos 192 px
After that, blog/ is the source: edit the files there, not Framer. tools/blog.py builds the pages.
"""
import html, json, re, subprocess, sys, urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = "https://blog.eez.io/blog/"
SLUGS = ["monthly-update---october-devcon-mumbai", "monthly-update---september", "monthly-update-august-2026",
         "introducing-the-eez", "monthly-update-digest-july-2026", "the-case-for-eez", "zkvm-for-next-generation-apps"]
OUT, BODIES, ORIG, IMG = ROOT / "blog", ROOT / "blog/posts", ROOT / "blog/originals", ROOT / "pages/assets/blog"
VOID = {"img", "br", "hr", "meta", "link", "input", "source", "path"}
UA = {"User-Agent": "Mozilla/5.0 (site migration)"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def containers(h):
    """Inner HTML of every Framer RichTextContainer, in page order."""
    out = []
    for m in re.finditer(r'<div[^>]*data-framer-component-type="RichTextContainer"[^>]*>', h):
        depth = 0
        for t in re.finditer(r"<(/?)([a-zA-Z0-9]+)[^>]*?(/?)>", h[m.start():]):
            if t.group(2).lower() in VOID or t.group(3):
                continue
            depth += -1 if t.group(1) else 1
            if depth == 0:
                out.append(h[m.end():m.start() + t.start()])
                break
    return out


def text(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


class Clean(HTMLParser):
    """Keep only plain content tags; Framer's h4 section heads become h2."""
    KEEP = {"p": "p", "h4": "h2", "h3": "h2", "h2": "h2", "ul": "ul", "ol": "ol", "li": "li",
            "strong": "strong", "b": "strong", "em": "em", "i": "em", "code": "code", "a": "a"}
    SKIP = {"button", "svg", "script", "style"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out, self.stack, self.skip = [], [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.skip or tag in self.SKIP:
            self.skip += tag in self.SKIP and tag not in VOID
            return
        if tag == "iframe" and "youtube.com/embed/" in (a.get("src") or ""):
            vid = re.search(r"embed/([\w-]+)", a["src"])[1]
            self.out.append(f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="YouTube video" '
                            'loading="lazy" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen" '
                            'allowfullscreen></iframe></div>')
            return
        if tag == "br":
            self.out.append("<br>")
            return
        new = self.KEEP.get(tag)
        self.stack.append(new)
        if not new:
            return
        if new == "a":
            href = a.get("href") or ""
            ext = href.startswith("http") and "eez.io" not in href.split("/")[2]
            self.out.append(f'<a href="{html.escape(href)}"' + (' target="_blank" rel="noopener"' if ext else "") + ">")
        else:
            self.out.append(f"<{new}>")

    def handle_endtag(self, tag):
        if self.skip:
            self.skip -= tag in self.SKIP
            return
        if tag in VOID or tag in ("iframe",) or not self.stack:
            return
        new = self.stack.pop()
        if new:
            self.out.append(f"</{new}>")

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)

    def handle_entityref(self, n):
        self.handle_data(f"&{n};")

    def handle_charref(self, n):
        self.handle_data(f"&#{n};")


def clean(body):
    p = Clean()
    p.feed(body)
    s = "".join(p.out)
    s = re.sub(r"<h2><strong>(.*?)</strong></h2>", r"<h2>\1</h2>", s)   # heads are bold already
    s = re.sub(r"<li><p>(.*?)</p></li>", r"<li>\1</li>", s, flags=re.S)   # Framer wraps list text in <p>
    s = re.sub(r"<(p|h2|li|strong|em)>\s*</\1>", "", s)                    # empty blocks
    s = re.sub(r"(?=<(?:p|h2|ul|ol|li|div)[ >])", "\n", s).strip()
    return s + "\n"


def image(name, size):
    src = ORIG / name
    if not src.exists():
        src.write_bytes(get(f"https://framerusercontent.com/images/{name}"))
    info = subprocess.run(["sips", "-g", "hasAlpha", "-g", "pixelWidth", "-g", "pixelHeight", str(src)],
                          check=True, capture_output=True, text=True).stdout
    if "hasAlpha: yes" in info:   # JPEG would turn transparent edges light; WebP keeps them transparent
        w, h = (int(re.search(rf"{k}: (\d+)", info)[1]) for k in ("pixelWidth", "pixelHeight"))
        r = min(1, size / max(w, h))
        out = IMG / (src.stem + ".webp")
        subprocess.run(["cwebp", "-quiet", "-q", "82", "-resize", str(round(w * r)), str(round(h * r)), str(src), "-o", str(out)], check=True)
    else:
        out = IMG / (src.stem + ".jpg")
        subprocess.run(["sips", "-Z", str(size), "-s", "format", "jpeg", "-s", "formatOptions", "82", str(src), "--out", str(out)],
                       check=True, capture_output=True)
    return f"/assets/blog/{out.name}"


def main():
    BODIES.mkdir(parents=True, exist_ok=True)
    for d in (ORIG, IMG):
        d.mkdir(parents=True, exist_ok=True)
    posts = []
    for slug in SLUGS:
        h = get(SRC + slug).decode()
        cs = containers(h)
        body = max(cs, key=len)
        head = [text(c) for c in cs[:cs.index(body)]]   # date, category, title, summary, author, role
        date, cat, title, summary, author, role = head[:6]
        start = h.find('data-framer-component-type="RichTextContainer"')
        imgs, seen = [], set()   # (position relative to the first text block, file), first use only
        for m in re.finditer(r'<img[^>]*framerusercontent\.com/images/([A-Za-z0-9]+\.\w+)[^>]*>', h):
            if m[1] not in seen:
                seen.add(m[1])
                imgs.append((m.start() - start, m[1]))
        cover = [n for pos, n in imgs if pos < 0][-1]                       # the image left of the title
        names = [n.strip() for n in author.split("&")]
        faces = [n for pos, n in imgs if 0 < pos < 6000][:len(names)]   # photos next to the byline
        posts.append({
            "slug": slug, "title": title, "date": date, "category": cat, "summary": summary,
            "authors": [{"name": n, "role": role, "photo": image(f, 192) if f else None}
                        for i, (n, f) in enumerate(zip(names, faces + [None] * len(names)))],
            "cover": image(cover, 1200),
        })
        (BODIES / f"{slug}.html").write_text(clean(body))
        print("imported", slug, "|", title, "|", date, "|", author, "| photos", len(faces))
    (OUT / "posts.json").write_text(json.dumps(posts, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    sys.exit(main())
