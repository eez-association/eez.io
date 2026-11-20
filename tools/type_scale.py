"""One type scale (2026-11-20): every font size on every page snaps to the 9 steps in shared/tokens.css.

Steps: 11 · 12.5 · 14 · 16 · 20 · 26 · 36 · 52 · 72 px (--eez-text-xs … --eez-text-hero).
- font-size and the size inside font: shorthands snap to the nearest step (ties: up below 20 px,
  down from 20 px), and nothing goes below 11 px.
- clamp(min, fluid, max): the min snaps down to a step, the max to the nearest step.
- A line-height in px in the same rule scales with its font size, so tight headings don't overlap.
Applies to page CSS (inline <style> blocks and the site's CSS files, use-case tokens.css and
bundle.css included); vendor files and SVG attributes are left alone. Runs before tokens_fix.py.
"""
import re, sys
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"
STEPS = [11, 12.5, 14, 16, 20, 26, 36, 52, 72]
NAMES = {11: "xs", 12.5: "sm", 14: "md", 16: "base", 20: "lg", 26: "xl", 36: "2xl", 52: "3xl", 72: "hero"}


def snap(v):
    v = max(v, 11)
    best = min(STEPS, key=lambda s: (abs(s - v), -s if v < 20 else s))
    return best


def floor_step(v):
    return max([s for s in STEPS if s <= v] or [11])


def var(step):
    return f"var(--eez-text-{NAMES[step]})"


def fmt(v):
    return ("%g" % v)


PX = r"([0-9]+(?:\.[0-9]+)?)px"


def fix_block(body):
    """body = the inside of one CSS rule. Returns (new_body, changes)."""
    n = 0
    ratio = None

    def clamp(m):
        nonlocal n
        lo, mid, hi = float(m.group(1)), m.group(2), float(m.group(3))
        n += 1
        return f"clamp({var(floor_step(lo))},{mid},{var(snap(hi))})"

    def size(m):
        nonlocal n, ratio
        old = float(m.group(2))
        new = snap(old)
        n += 1
        ratio = new / old
        return f"{m.group(1)}{var(new)}"

    body = re.sub(r"clamp\(\s*" + PX + r"\s*,([^,]+),\s*" + PX + r"\s*\)", clamp, body)
    # font-size: Npx
    body = re.sub(r"(font-size\s*:\s*)" + PX, size, body)
    # font: [style] [weight] Npx[/lh] family
    def short(m):
        nonlocal n, ratio
        pre, sz, lh = m.group(1), float(m.group(2)), m.group(3) or ""
        new = snap(sz)
        n += 1
        ratio = new / sz
        if lh.endswith("px"):
            lh = "/" + fmt(round(float(lh[1:-2]) * ratio, 1)) + "px"
        return f"{pre}{var(new)}{lh}"
    body = re.sub(r"(\bfont\s*:\s*(?:[a-z-]+\s+|[0-9]{3}\s+)*)" + PX + r"(/[0-9.]+(?:px)?)?", short, body)
    if ratio and abs(ratio - 1) > 1e-6:
        body = re.sub(r"(line-height\s*:\s*)" + PX, lambda m: f"{m.group(1)}{fmt(round(float(m.group(2)) * ratio, 1))}px", body)
    return body, n


def fix_css(css):
    total = 0
    def block(m):
        nonlocal total
        body, k = fix_block(m.group(2))
        total += k
        return m.group(1) + body + "}"
    css = re.sub(r"(\{)([^{}]*)\}", block, css)
    return css, total


def main():
    total = 0
    for f in sorted(DIST.rglob("*")):
        if f.suffix not in (".html", ".css") or "vendor" in f.parts:
            continue
        s = f.read_text()
        if f.suffix == ".css":
            new, n = fix_css(s)
        else:
            n = 0
            def style(m):
                nonlocal n
                body, k = fix_css(m.group(2))
                n += k
                return m.group(1) + body + m.group(3)
            new = re.sub(r"(<style[^>]*>)(.*?)(</style>)", style, s, flags=re.S)
        if new != s:
            f.write_text(new)
            total += n
    left = []
    for f in DIST.rglob("*"):
        if f.suffix in (".html", ".css") and "vendor" not in f.parts:
            t = f.read_text()
            css = t if f.suffix == ".css" else " ".join(re.findall(r"<style[^>]*>(.*?)</style>", t, re.S))
            for m in re.finditer(r"font-size\s*:\s*([0-9.]+)px|\bfont\s*:[^;{}]*?(?<![/.\d])([0-9.]+)px", css):
                left.append(f"{f.name}:{m.group(0)[:40]}")
    if left:
        sys.exit("type_scale: px font sizes left: " + "; ".join(left[:8]))
    print(f"type scale: {total} font sizes snapped to 9 steps")


if __name__ == "__main__":
    main()
