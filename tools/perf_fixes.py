"""Home page CPU and GPU load (2026-11-20). A teammate's computer slowed down, Google Meet included,
with eez.io open. The partner-logo ticker ran a requestAnimationFrame loop forever, even off screen,
and measured the track (a forced layout) on every frame. Now it measures once (again on resize, font
and image load) and only runs while the ticker is on screen. The blurred background glows are fixed
in live_parity.py. Each edit must apply once or the build stops.
"""
import sys
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"

OLD = """  const step = now => { if (last !== null) { const dt = Math.min(64, now - last) / 1000; v += (target - v) * Math.min(1, dt * 4);
      const L = set.getBoundingClientRect().width; x = (x + v * dt) % L; t.style.transform = `translateX(${-x}px)`; }
    last = now; requestAnimationFrame(step); };
  requestAnimationFrame(step);"""

NEW = """  let L = 0, on = false, raf = 0;
  const measure = () => { L = set.getBoundingClientRect().width; };
  measure(); addEventListener("resize", measure);
  if (document.fonts) document.fonts.ready.then(measure);
  t.querySelectorAll("img").forEach(i => i.addEventListener("load", measure));
  const step = now => { if (last !== null && L) { const dt = Math.min(64, now - last) / 1000; v += (target - v) * Math.min(1, dt * 4);
      x = (x + v * dt) % L; t.style.transform = `translate3d(${-x}px,0,0)`; }
    last = now; raf = on ? requestAnimationFrame(step) : 0; };
  new IntersectionObserver(([e]) => { on = e.isIntersecting; if (on && !raf) { last = null; raf = requestAnimationFrame(step); } }).observe(mq);"""


def main():
    f = DIST / "index.html"
    s = f.read_text()
    if s.count(OLD) != 1:
        sys.exit("perf_fixes: ticker loop not found in index.html")
    f.write_text(s.replace(OLD, NEW))
    print("perf fixes: ticker runs only on screen")


if __name__ == "__main__":
    main()
