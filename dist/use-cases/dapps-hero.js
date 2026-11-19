// Dapps hero: one app, deployed once, reached by users on Ethereum mainnet, on your chain and on other
// EEZ chains. Each call lights up in turn and lands in the user’s own transaction. Wide layout on
// desktop, stacked on phones. Loops while on screen. Reduced motion: final state.
(() => {
  const root = document.querySelector(".dx");
  if (!root) return;
  const fig = root.querySelector(".dx-fig"), status = root.querySelector(".dx-status");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const narrow = matchMedia("(max-width: 640px)");
  const USERS = [
    ["Users on Ethereum mainnet", "one transaction"],
    ["Users on your chain", "a local call"],
    ["Users on other EEZ chains", "verified in the same L1 block"],
  ];
  const box = (k, x, y, w, h, name, sub, cls = "") =>
    `<g class="dx-box ${cls}" data-k="${k}" data-s=""><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9"/>` +
    `<text class="dx-name" x="${x + w / 2}" y="${y + h / 2 - 3}" text-anchor="middle">${name}</text>` +
    `<text class="dx-sub" x="${x + w / 2}" y="${y + h / 2 + 14}" text-anchor="middle">${sub}</text>` +
    `<text class="dx-ic" x="${x + w - 10}" y="${y + 17}" text-anchor="end"></text></g>`;
  const ARIA = "Users on Ethereum mainnet, your chain and other EEZ chains call your app, deployed once";

  const build = () => {
    fig.innerHTML = narrow.matches
      ? `<svg viewBox="0 0 320 330" role="img" aria-label="${ARIA}">` +
        USERS.map((_, i) => `<path class="dx-edge" data-k="e${i}" d="M${80 + i * 80} 156 L160 88"/>`).join("") +
        box("app", 70, 20, 180, 68, "Your app", "deployed once", "is-app") +
        USERS.map(([n, s], i) => box("u" + i, 20, 156 + i * 58, 280, 48, n, s)).join("") + `</svg>`
      : `<svg viewBox="0 0 680 250" role="img" aria-label="${ARIA}">` +
        USERS.map((_, i) => `<path class="dx-edge" data-k="e${i}" d="M272 ${49 + i * 76} C344 ${49 + i * 76} 360 125 440 125"/>`).join("") +
        USERS.map(([n, s], i) => box("u" + i, 20, 18 + i * 76, 252, 62, n, s)).join("") +
        box("app", 440, 88, 220, 74, "Your app", "deployed once", "is-app") + `</svg>`;
  };

  const ICON = { ok: "✓" };
  const F = window.HeroFlow(fig, "dx");
  const set = (k, st) => {
    const el = fig.querySelector(`.dx-box[data-k="${k}"]`); if (!el) return;
    el.dataset.s = st;
    const ic = el.querySelector(".dx-ic"); if (ic) ic.textContent = ICON[st] || "";
  };
  const boxes = () => [...fig.querySelectorAll(".dx-box")];
  // [kind, key, ms]: "box" lights a box, "line" draws a path, "pause" waits
  const SEQ = [["box", "app", 260, "on"], ["line", "e0", 820], ["box", "u0", 220, "ok"], ["line", "e1", 820], ["box", "u1", 220, "ok"],
    ["line", "e2", 820], ["box", "u2", 200, "ok"]];
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
  window.__dxPlay = play; // test hook
  const r = root.getBoundingClientRect();
  if (reduce || !("IntersectionObserver" in window) || (r.top < innerHeight && r.bottom > 0)) return play(); // already in view: start now
  const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { io.disconnect(); play(); } }, { threshold: 0.35 });
  io.observe(root);
})();
