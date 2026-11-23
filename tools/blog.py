"""Blog pages from blog/ (posts moved off Framer on 23 Nov 2026): /blog/ and /blog/<slug>.

Source: blog/posts.json (newest first) and blog/posts/<slug>.html (the post body). To add a post,
add its entry and body there, its images under pages/assets/blog/, and its link preview in
tools/og/pages.json (id "blog-<slug>").

Runs after copy_fixes, type_scale and tokens_fix on purpose: those rewrite wording ("Testnet",
"zone", "&") on every page, and dated posts must keep the words they were published with. So
this CSS uses the --eez-* tokens and type steps directly. social_meta (link previews) and
smart_quotes still run on these pages afterwards.
"""
import html, json, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from assemble import FONTS, SHELL_HEAD, SHELL_JS  # noqa: E402

SRC, OUT = ROOT / "blog", ROOT / "dist/blog"
esc = html.escape

CSS = """
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--eez-page);color:var(--eez-ink);font:400 var(--eez-text-base)/1.6 "Geist",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.glow{position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:radial-gradient(700px 520px at 18% 30%,rgba(59,229,126,.07),transparent 70%),radial-gradient(760px 560px at 86% 58%,rgba(84,66,205,.08),transparent 70%)}
.skip{position:absolute;left:16px;top:-80px;z-index:300;padding:10px 14px;border-radius:8px;background:var(--eez-ink);color:var(--eez-page);font:500 var(--eez-text-sm)/1 "Geist Mono",monospace;letter-spacing:.06em;text-transform:uppercase;text-decoration:none}
.skip:focus{top:12px}
.wrap{width:min(1136px,100% - 32px);margin:0 auto}
.eb{margin:0;font:400 var(--eez-text-sm)/1.3 "Geist Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--eez-label)}
.meta{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin:0;font:400 var(--eez-text-sm)/1.3 "Geist Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--eez-label)}
.meta .cat{color:var(--eez-green)}
/* index */
.page{padding:96px 0 120px;display:grid;gap:56px}
.head{display:grid;gap:16px;justify-items:center;text-align:center}
h1{margin:0;font:300 var(--eez-text-3xl)/1.05 "Geist",sans-serif;letter-spacing:-.01em;color:var(--eez-ink);text-wrap:balance}
h1 .lite{color:var(--eez-heading)}
.lede{margin:0;max-width:600px;font-size:var(--eez-text-lead);line-height:1.55;color:var(--eez-body);text-wrap:pretty}
.posts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}
.post{background:var(--eez-surface);border:1px solid var(--eez-line-soft);border-radius:var(--eez-radius-card);padding:18px 20px 22px;display:grid;gap:12px;align-content:start;color:inherit;text-decoration:none;transition:border-color .2s;min-width:0}
.post:hover{border-color:var(--eez-line)}
.post:focus-visible{outline:2px solid var(--eez-green);outline-offset:3px}
.post img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:8px;display:block;background:var(--eez-page)}
.post b{font:500 var(--eez-text-lg)/1.3 "Geist",sans-serif;color:var(--eez-ink);text-wrap:balance}
.post p{margin:0;font-size:var(--eez-text-md);line-height:1.5;color:var(--eez-muted)}
/* post */
.article{padding:72px 0 96px;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:64px;align-items:start}
.cover{position:sticky;top:96px;margin:0}
.cover img{width:100%;height:auto;display:block;border-radius:var(--eez-radius-card);border:1px solid var(--eez-line-soft)}
.back{display:inline-block;margin-bottom:28px;font:400 var(--eez-text-sm)/1 "Geist Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--eez-label);text-decoration:none}
.back:hover{color:var(--eez-green)}
.article h1{margin:18px 0 0;font:400 var(--eez-text-2xl)/1.15 "Geist",sans-serif;letter-spacing:-.01em}
.sum{margin:16px 0 0;font-size:var(--eez-text-lead);line-height:1.55;color:var(--eez-body)}
.by{display:flex;flex-wrap:wrap;gap:16px 28px;margin:28px 0 0;padding:0 0 32px;border-bottom:1px solid var(--eez-line-soft)}
.by div{display:flex;align-items:center;gap:12px}
.by img{width:44px;height:44px;border-radius:50%;object-fit:cover;display:block}
.by b{display:block;font:500 var(--eez-text-md)/1.3 "Geist",sans-serif;color:var(--eez-ink)}
.by small{display:block;font:400 var(--eez-text-xs)/1.3 "Geist Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--eez-label)}
.body{margin-top:32px;font-size:var(--eez-text-base);line-height:1.7;color:var(--eez-body);overflow-wrap:anywhere}
.body>*:first-child{margin-top:0}
.body p{margin:0 0 18px}
.body h2{margin:40px 0 14px;font:500 var(--eez-text-lg)/1.3 "Geist",sans-serif;color:var(--eez-ink)}
.body ul,.body ol{margin:0 0 18px;padding-left:22px}
.body li{margin:0 0 8px}
.body li::marker{color:var(--eez-label)}
.body strong{font-weight:600;color:var(--eez-ink-soft)}
.body a{color:var(--eez-mint);text-decoration:underline;text-decoration-color:rgba(168,243,206,.35);text-underline-offset:3px}
.body a:hover{color:var(--eez-green);text-decoration-color:currentColor}
.body code{font:400 .9em "Geist Mono",monospace;padding:1px 5px;border-radius:4px;background:var(--eez-raised)}
.video{position:relative;aspect-ratio:16/9;margin:0 0 24px;border-radius:var(--eez-radius-tile);overflow:hidden;background:var(--eez-surface)}
.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.more{padding:0 0 120px;display:grid;gap:24px;border-top:1px solid var(--eez-line-soft);padding-top:56px}
@media (max-width:900px){.posts{grid-template-columns:repeat(2,minmax(0,1fr))}.article{grid-template-columns:1fr;gap:32px}.cover{position:static;max-width:420px}}
@media (max-width:600px){.page{padding-top:64px}.posts{grid-template-columns:1fr}h1{font-size:var(--eez-text-2xl)}.article{padding-top:40px}.article h1{font-size:var(--eez-text-xl)}}
"""


def iso(date):
    return datetime.strptime(date, "%b %d, %Y").date().isoformat()


def meta(p):
    return f'<p class="meta"><time datetime="{iso(p["date"])}">{esc(p["date"])}</time><span class="cat">{esc(p["category"])}</span></p>'


def card(p):
    return (f'<a class="post" href="/blog/{p["slug"]}"><img src="{p["cover"]}" alt="" loading="lazy">'
            f'{meta(p)}<b>{esc(p["title"])}</b><p>{esc(p["summary"])}</p></a>')


def shell_parts():
    """Devcon bar, header and footer as the copy pass left them on another page (it fixes their wording too)."""
    built = (ROOT / "dist/brand.html").read_text()
    parts = []
    for pat in (r'<div class="eh-devcon">.*?</div>', r'<header class="eh".*?</header>', r'<footer class="ef".*?</footer>'):
        m = re.search(pat, built, re.S)
        if not m:
            sys.exit(f"blog: {pat[:24]} not found in dist/brand.html")
        parts.append(m[0])
    return parts


def page(title, main):
    devcon, header, footer = shell_parts()
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="theme-color" content="#0a0a0a">
<link rel="icon" type="image/svg+xml" href="/assets/eez-mark.svg">
<style>{CSS}</style>
{FONTS}
{SHELL_HEAD}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="glow" aria-hidden="true"></div>
{devcon}
{header}
{main}
{footer}
{SHELL_JS}
</body>
</html>
"""


def main():
    posts = json.loads((SRC / "posts.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    index = f"""<main id="main" class="wrap page">
  <div class="head">
    <p class="eb">[ Blog ]</p>
    <h1>Perspectives<span class="lite">.</span></h1>
    <p class="lede">A space for updates and perspectives from key contributors.</p>
  </div>
  <div class="posts">{"".join(card(p) for p in posts)}</div>
</main>"""
    (OUT / "index.html").write_text(page("EEZ · Blog", index))
    for i, p in enumerate(posts):
        body = (SRC / "posts" / f'{p["slug"]}.html').read_text()
        by = ""
        for a in p["authors"]:
            photo = f'<img src="{a["photo"]}" alt="">' if a["photo"] else ""
            role = f'<small>{esc(a["role"])}</small>' if a["role"] else ""
            by += f'<div>{photo}<span><b>{esc(a["name"])}</b>{role}</span></div>'
        others = [q for q in posts if q is not p][:3]
        main_html = f"""<main id="main">
<article class="wrap article">
  <figure class="cover"><img src="{p["cover"]}" alt=""></figure>
  <div>
    <a class="back" href="/blog/">← All posts</a>
    {meta(p)}
    <h1>{esc(p["title"])}</h1>
    <p class="sum">{esc(p["summary"])}</p>
    <div class="by">{by}</div>
    <div class="body">
{body}    </div>
  </div>
</article>
<section class="wrap more" aria-labelledby="more">
  <p class="eb" id="more">[ More posts ]</p>
  <div class="posts">{"".join(card(q) for q in others)}</div>
</section>
</main>"""
        (OUT / f'{p["slug"]}.html').write_text(page(f'{p["title"]} · EEZ', main_html))
    print(f"blog: index + {len(posts)} posts")


if __name__ == "__main__":
    main()
