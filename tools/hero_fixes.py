"""Infra hero: the same line motion as the Apps and Chains heroes (2026-11-20).

Apps and Chains draw each line with the shared HeroFlow helper (hero-flow.js): a solid trace draws
itself while a soft light runs ahead, then everything retracts and loops. Infra still swapped dashed
lines to solid on a timer. This step loads hero-flow.js on the Infra page, gives the ix- diagram the
dx- line and box styles, and replaces infra-hero.js's timer loop with the same sequence player.
Each edit must apply once or the build stops.
"""
import sys
from pathlib import Path

UC = Path(__file__).resolve().parent.parent / "dist/use-cases"


def rep(s, old, new, what):
    if s.count(old) != 1:
        sys.exit(f"hero_fixes: expected one match for {what}, found {s.count(old)}")
    return s.replace(old, new)


def main():
    page = UC / "infra.html"
    h = page.read_text()
    if "hero-flow.js" not in h:
        h = rep(h, '<script src="/use-cases/infra-hero.js" defer>',
                '<script src="/use-cases/hero-flow.js" defer></script>\n<script src="/use-cases/infra-hero.js" defer>', "infra-hero script tag")
        h = rep(h, '.ix-edge { fill: none; stroke: var(--edge); stroke-width: 1.3; stroke-dasharray: 4 5; transition: stroke .35s; }',
                '.ix-edge { fill: none; stroke: var(--edge); stroke-width: 1; }\n'
                '  .ix-trace { fill: none; stroke: url(#eez-g); stroke-width: 1.6; stroke-linecap: round; }\n'
                '  .ix-dot { fill: #eef2ff; opacity: 0; }\n'
                '  .ix-glow { fill: var(--grad-steel); opacity: 0; filter: blur(4px); }', "ix-edge rule")
        h = rep(h, '.ix-edge[data-s="run"] { stroke: url(#eez-g); stroke-dasharray: none; }', "", "ix-edge run rule")
        h = rep(h, '.ix-box rect { fill: #121212; stroke: var(--edge); transition: stroke .35s, fill .35s; }',
                '.ix-box { transform-box: fill-box; transform-origin: center; transition: transform .5s cubic-bezier(.2,.8,.2,1), filter .5s ease; }\n'
                '  .ix-box rect { fill: #121212; stroke: var(--edge); transition: stroke .5s ease, fill .5s ease; }', "ix-box rect rule")
        h = rep(h, '.ix-box[data-s="ok"] rect { stroke: var(--eez-green); fill: color-mix(in oklab, var(--eez-green) 8%, #121212); }',
                '.ix-box[data-s="ok"] { transform: scale(1.02); filter: drop-shadow(0 0 7px rgba(98,131,189,.35)); }\n'
                '  .ix-box[data-s="ok"] rect { stroke: url(#eez-g); stroke-width: 1.4; fill: color-mix(in oklab, var(--grad-steel) 12%, #121212); }', "ix-box ok rule")
        page.write_text(h)

    js = UC / "infra-hero.js"
    s = js.read_text()
    if "HeroFlow" not in s:
        s = rep(s, '  const set = (k, st) => {\n    const el = fig.querySelector(`[data-k="${k}"]`); if (!el) return;',
                '  const F = window.HeroFlow(fig, "ix");\n  const set = (k, st) => {\n    const el = fig.querySelector(`.ix-box[data-k="${k}"]`); if (!el) return;', "set()")
        start = s.index("  const STEPS = ")
        end = s.index("  build();")
        player = '''  const boxes = () => [...fig.querySelectorAll(".ix-box")];
  // [kind, key, ms, state]: "box" lights a box, "line" draws a path (same player as the Apps and Chains heroes)
  const SEQ = [["box", "you", 260, "on"], ["line", "er", 820], ["box", "c0", 200, "ok"], ["box", "c1", 200, "ok"],
    ["box", "c2", 260, "ok"], ["line", "ec", 820], ["box", "cmp", 220, "ok"]];
  const play = async () => {
    const id = F.next();
    boxes().forEach((el) => set(el.dataset.k, "")); F.reset(); status.classList.remove("on");
    if (reduce) { SEQ.forEach(([t, k, , st]) => t === "box" && set(k, st)); F.final(); status.classList.add("on"); return; }
    if (!(await F.wait(300, id))) return;
    for (const [t, k, ms, st] of SEQ) {
      if (t === "box") { set(k, st); if (!(await F.wait(ms, id))) return; }
      else if (!(await F.draw(k, ms, id))) return;
    }
    status.classList.add("on");
    if (!(await F.wait(3200, id))) return;
    boxes().forEach((el) => set(el.dataset.k, "")); status.classList.remove("on");
    if (!(await F.retract(700, id))) return;
    if (!(await F.wait(500, id))) return;
    play();
  };

'''
        s = s[:start] + player + s[end:]
        s = rep(s, '  build();\n  narrow.addEventListener("change", () => { build(); play(); });',
                '  build(); F.enhance();\n  narrow.addEventListener("change", () => { build(); F.enhance(); play(); });', "build/enhance")
        js.write_text(s)
    print("hero fixes: Infra uses the shared line motion")


if __name__ == "__main__":
    main()
