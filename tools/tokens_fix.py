"""One token system (2026-11-20): every page's colours come from shared/tokens.css (--eez-*).

1. Use-case pages: their design-system names (--canvas, --screen, --edge, --ink-*, --muted …) are
   re-pointed at --eez-* by a :root:root block appended to system/tokens.css.
2. Hard-coded colours in page CSS (inline <style> blocks and site/shell CSS) are replaced by the
   matching --eez-* token, chosen by what the property does: fills -> surfaces, borders and strokes ->
   lines, color -> the text scale. Brand greens, gradients, alpha washes and SVG attribute fills are
   left alone. Custom-property definitions are left alone (step 1 and live_parity.py alias them).
Runs after the other build steps that edit CSS and before smart_quotes.py.
"""
import re, sys
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"

FILL = {  # background / fill
    "#090909": "page", "#0a0a0a": "page", "#0b0b0b": "page", "#0d0d0d": "page", "#101010": "page",
    "#111": "surface", "#111111": "surface", "#121212": "surface", "#131313": "surface",
    "#141414": "surface", "#151515": "surface", "#161616": "surface",
    "#1a1a1a": "raised", "#1c1c1c": "raised", "#1e1e1e": "raised", "#1f1f1f": "raised",
}
LINE = {  # border / outline / stroke
    "#1a1a1a": "line-soft", "#1c1c1c": "line-soft", "#1e1e1e": "line-soft",
    "#222": "line", "#222222": "line", "#262626": "line", "#2a2a2a": "line", "#2e2e2e": "line",
    "#333": "line", "#333333": "line",
    "rgba(255,255,255,.06)": "line-faint", "rgba(255,255,255,.08)": "line-faint",
    "rgba(255,255,255,.09)": "line-faint", "rgba(255,255,255,.1)": "line-faint",
}
TEXT = {  # color
    "#ffffff": "ink", "#f2f2ec": "ink-soft", "#f5f5f0": "ink-soft", "#dcdcdc": "heading", "#d8d8d8": "heading",
    "#c9cfda": "body", "#9aa3b3": "label",
    "#8f8f8f": "muted", "#8c8c86": "muted", "#8a8a85": "muted", "#888888": "muted", "#9a9a9a": "muted",
    "#7a7a76": "muted", "#6f6f6f": "muted", "#6a6a6a": "muted", "#5e5e5a": "muted", "#5f5f5a": "muted",
}
UC_ALIASES = """
/* One token system: these names now point at shared/tokens.css (added by tools/tokens_fix.py) */
:root:root, :root:root[data-theme="dark"] {
  --void: #000000; --canvas: var(--eez-page); --screen: var(--eez-surface); --chrome: var(--eez-raised);
  --edge: var(--eez-line); --edge-quiet: var(--eez-line-soft);
  --control: var(--eez-surface); --control-edge: var(--eez-line); --control-hover: var(--eez-raised);
  --ink: var(--eez-ink); --ink-soft: var(--eez-heading); --ink-body: var(--eez-body);
  --muted: var(--eez-label); --ink-quiet: var(--eez-muted); --card-num: var(--eez-muted);
  --pinned: var(--eez-mint); --grad-mint: var(--eez-grad-mint); --grad-steel: var(--eez-grad-steel); --grad-indigo: var(--eez-grad-indigo);
  --radius-card: var(--eez-radius-card); --radius-pill: var(--eez-radius-pill);
}
"""
DECL = re.compile(r"(?<![\w-])([a-z][a-z-]*)\s*:\s*([^;{}]*)")
COL = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba\([^)]*\)")


def norm(c):
    c = c.lower().replace(" ", "")
    if re.fullmatch(r"#[0-9a-f]{3}", c) and c not in FILL and c not in LINE:
        c = "#" + "".join(ch * 2 for ch in c[1:])
    return {"#fff": "#ffffff"}.get(c, c)


def fix_css(css):
    n = 0
    def decl(m):
        nonlocal n
        prop, val = m.group(1), m.group(2)
        if "gradient" in val or "url(" in val:
            return m.group(0)
        table = (FILL if prop in ("background", "background-color", "fill") else
                 LINE if prop.startswith(("border", "outline", "stroke")) or prop in ("column-rule",) else
                 TEXT if prop in ("color", "-webkit-text-fill-color", "caret-color") else None)
        if table is None:
            return m.group(0)
        def col(cm):
            nonlocal n
            role = table.get(norm(cm.group(0)))
            if not role:
                return cm.group(0)
            n += 1
            return f"var(--eez-{role})"
        return m.group(0).replace(val, COL.sub(col, val), 1) if COL.search(val) else m.group(0)
    return DECL.sub(decl, css), n


def main():
    total = 0
    for f in sorted(DIST.rglob("*")):
        if f.suffix not in (".html", ".css") or "vendor" in f.parts or f.name in ("tokens.css", "bundle.css"):
            continue
        s = f.read_text()
        if f.suffix == ".css":
            new, n = fix_css(s)
        else:
            n = 0
            def block(m):
                nonlocal n
                body, k = fix_css(m.group(2))
                n += k
                return m.group(1) + body + m.group(3)
            new = re.sub(r"(<style[^>]*>)(.*?)(</style>)", block, s, flags=re.S)
        if n:
            f.write_text(new)
            total += n
    sys_tokens = DIST / "use-cases/system/tokens.css"
    t = sys_tokens.read_text()
    if "One token system" not in t:
        sys_tokens.write_text(t + UC_ALIASES)
    print(f"tokens fix: {total} hard-coded colours -> --eez-* tokens")


if __name__ == "__main__":
    main()
