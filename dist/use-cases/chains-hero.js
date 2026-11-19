// Chains hero: your chain calls Ethereum’s apps, then other EEZ chains, each answer back in the same
// transaction. Wide layout on desktop, stacked on phones (rebuilt across the breakpoint). Loops while
// on screen. Reduced motion: final state.
(() => {
  const root = document.querySelector(".cx");
  if (!root) return;
  const fig = root.querySelector(".cx-fig"), status = root.querySelector(".cx-status");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const narrow = matchMedia("(max-width: 640px)");
  const APPS = ["Lending", "DEX", "Names"];

  const box = (k, x, y, w, h, name, sub, cls = "") =>
    `<g class="cx-box ${cls}" data-k="${k}" data-s=""><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9"/>` +
    `<text class="cx-name" x="${x + w / 2}" y="${y + h / 2 + (sub ? -3 : 5)}" text-anchor="middle">${name}</text>` +
    (sub ? `<text class="cx-sub" x="${x + w / 2}" y="${y + h / 2 + 14}" text-anchor="middle">${sub}</text>` : "") +
    `<text class="cx-ic" x="${x + w - 10}" y="${y + 17}" text-anchor="end"></text></g>`;

  const build = () => {
    let svg;
    if (narrow.matches) {
      svg = `<svg viewBox="0 0 320 400" role="img" aria-label="Your chain calls apps on Ethereum mainnet and other EEZ chains">` +
        `<path class="cx-edge" data-k="ee" d="M160 70 L160 112"/>` +
        `<path class="cx-edge" data-k="ec" d="M78 42 C18 42 18 344 40 344"/>` +
        box("you", 70, 8, 180, 62, "Your chain", "your sequencer · governance", "is-you") +
        `<rect class="cx-frame" x="40" y="112" width="270" height="168" rx="12"/><text class="cx-cap" x="56" y="136">Ethereum mainnet</text>` +
        APPS.map((a, i) => box("a" + i, 54, 150 + i * 42, 242, 34, a, "")).join("") +
        box("ch", 40, 312, 270, 64, "Other EEZ chains", "verified in the same L1 block") +
        `</svg>`;
    } else {
      svg = `<svg viewBox="0 0 680 270" role="img" aria-label="Your chain calls apps on Ethereum mainnet and other EEZ chains">` +
        `<path class="cx-edge" data-k="ee" d="M212 118 C252 118 252 92 300 92"/>` +
        `<path class="cx-edge" data-k="ec" d="M212 134 C252 134 252 226 300 226"/>` +
        box("you", 20, 92, 192, 68, "Your chain", "your sequencer · governance", "is-you") +
        `<rect class="cx-frame" x="300" y="12" width="360" height="160" rx="12"/><text class="cx-cap" x="318" y="38">Ethereum mainnet</text>` +
        APPS.map((a, i) => box("a" + i, 318 + i * 112, 74, 100, 70, a, "")).join("") +
        box("ch", 300, 194, 360, 64, "Other EEZ chains", "verified in the same L1 block") +
        `</svg>`;
    }
    fig.innerHTML = svg;
  };

  const ICON = { ok: "✓" };
  const F = window.HeroFlow(fig, "cx");
  const set = (k, st) => {
    const el = fig.querySelector(`.cx-box[data-k="${k}"]`); if (!el) return;
    el.dataset.s = st;
    const ic = el.querySelector(".cx-ic"); if (ic) ic.textContent = ICON[st] || "";
  };
  const boxes = () => [...fig.querySelectorAll(".cx-box")];
  // [kind, key, ms]: "box" lights a box, "line" draws a path, "pause" waits
  const SEQ = [["box", "you", 260, "on"], ["line", "ee", 820], ["box", "a0", 300, "ok"], ["box", "a1", 300, "ok"], ["box", "a2", 360, "ok"],
    ["line", "ec", 820], ["box", "ch", 200, "ok"]];
  const play = async () => {
    const id = F.next();
    boxes().forEach((el) => set(el.dataset.k, "")); F.reset(); status.classList.remove("on");
    if (reduce) { SEQ.forEach(([t, k, , st]) => t === "box" && set(k, st)); F.final(); status.classList.add("on"); return; }
    if (!(await F.wait(300, id))) return;
    for (const [t, k, ms, st] of SEQ) {
      if (t === "box") { set(k, st); if (!(await F.wait(ms, id))) return; }
      else if (t === "line") { if (!(await F.draw(k, ms, id))) return; }
      else if (!(await F.wait(ms, id))) return;
    }
    status.classList.add("on");
    if (!(await F.wait(3200, id))) return;
    // wind back without fading: boxes settle, lines retract, then run again
    boxes().forEach((el) => set(el.dataset.k, "")); status.classList.remove("on");
    if (!(await F.retract(700, id))) return;
    if (!(await F.wait(500, id))) return;
    play();
  };

  build(); F.enhance();
  narrow.addEventListener("change", () => { build(); F.enhance(); play(); });
  window.__cxPlay = play; // test hook
  const r = root.getBoundingClientRect();
  if (reduce || !("IntersectionObserver" in window) || (r.top < innerHeight && r.bottom > 0)) return play(); // already in view: start now
  const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { io.disconnect(); play(); } }, { threshold: 0.35 });
  io.observe(root);
})();
