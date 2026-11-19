"""Accessibility and weight fixes from the Impeccable audit (2026-11-20), applied to dist/.

- Home: a "Skip to content" link (the other pages already have one) that jumps past the header.
- All use cases: a visually hidden h2 so headings go h1 -> h2 -> h3.
- Home: Alliance, talk and Latest images load lazily (they sit far below the first screen).
- bermuda-bay.png: resized from 852 px to 300 px wide (shown at about 142 px).
- The unused one-transaction video and poster are removed from dist.
Runs after copy_fixes.py; each edit must apply once or the build stops.
"""
import re, subprocess, sys
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"
HIDE = "position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap"


def sub(s, pat, new, what, count=1, flags=0):
    s2, n = re.subn(pat, new, s, count=count, flags=flags)
    if not n:
        sys.exit(f"audit_fixes: not found: {what}")
    return s2


def main():
    idx = DIST / "index.html"
    s = idx.read_text()
    if 'class="skip"' not in s:
        s = sub(s, r'<section class="hero sec"', '<section class="hero sec" id="content" tabindex="-1"', "home hero section")
        s = sub(s, r"<body([^>]*)>", r'<body\1>\n<a class="skip" href="#content">Skip to content</a>', "home <body>")
    s, n = re.subn(r'<img (?![^>]*loading=)([^>]*src="assets/(?:logos|media)/[^"]*"[^>]*)>', r'<img loading="lazy" \1>', s)
    # keep the hero marquee eager: it is in the first screen
    s = re.sub(r'(<div class="mq[^"]*"[\s\S]*?</div>\s*</div>)', lambda m: m[1].replace('<img loading="lazy" ', '<img '), s, count=1)
    idx.write_text(s)
    allp = DIST / "use-cases/all.html"
    a = allp.read_text()
    if "<h2" not in a.split('class="blk" style="border-top:none;padding-top:8px">', 1)[-1][:200]:
        a = sub(a, r'(<section class="blk" style="border-top:none;padding-top:8px">)',
                r'\1<h2 style="' + HIDE + r'">Use cases</h2>', "All use cases list section")
    allp.write_text(a)
    logo = DIST / "assets/logos/bermuda-bay.png"
    w = int(re.search(r"pixelWidth: (\d+)", subprocess.run(["sips", "-g", "pixelWidth", str(logo)], capture_output=True, text=True).stdout)[1])
    if w > 300:
        subprocess.run(["sips", "--resampleWidth", "300", str(logo)], capture_output=True, check=True)
    for f in (DIST / "assets/media").glob("d39-one-transaction.*"):
        if not any(f.name in x.read_text() for x in DIST.rglob("*.html")):
            f.unlink()
    print(f"audit fixes applied ({n} images lazy)")


if __name__ == "__main__":
    main()
