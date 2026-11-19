// Infra hero: the stack you already run serves Ethereum mainnet and every EEZ chain over standard RPC;
// only cross-chain calls go to the composer. Wide layout on desktop, stacked on phones. Loops while on
// screen. Reduced motion: final state.
(() => {
  const root = document.querySelector(".ix");
  if (!root) return;
  const fig = root.querySelector(".ix-fig"), status = root.querySelector(".ix-status");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const narrow = matchMedia("(max-width: 640px)");
  const CHAINS = ["Ethereum mainnet", "EEZ chain A", "EEZ chain B"];
  const box = (k, x, y, w, h, name, sub, cls = "") =>
    `<g class="ix-box ${cls}" data-k="${k}" data-s=""><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9"/>` +
    `<text class="ix-name" x="${x + w / 2}" y="${y + h / 2 + (sub ? -3 : 5)}" text-anchor="middle">${name}</text>` +
    (sub ? `<text class="ix-sub" x="${x + w / 2}" y="${y + h / 2 + 14}" text-anchor="middle">${sub}</text>` : "") +
    `<text class="ix-ic" x="${x + w - 10}" y="${y + 17}" text-anchor="end"></text></g>`;
  const ARIA = "Your wallet, RPC or indexer serves Ethereum mainnet and every EEZ chain over standard RPC; cross-chain calls go to the composer";

  const build = () => {
    fig.innerHTML = narrow.matches
      ? `<svg viewBox="0 0 320 400" role="img" aria-label="${ARIA}">` +
        `<path class="ix-edge" data-k="er" d="M160 70 L160 112"/>` +
        `<path class="ix-edge" data-k="ec" d="M78 42 C18 42 18 344 40 344"/>` +
        box("you", 70, 8, 180, 62, "Your stack", "wallet · RPC · indexer", "is-you") +
        `<rect class="ix-frame" x="40" y="112" width="270" height="168" rx="12"/><text class="ix-cap" x="56" y="136">Standard RPC</text>` +
        CHAINS.map((c, i) => box("c" + i, 54, 150 + i * 42, 242, 34, c, "")).join("") +
        box("cmp", 40, 312, 270, 64, "Composer", "cross-chain calls only") + `</svg>`
      : `<svg viewBox="0 0 680 270" role="img" aria-label="${ARIA}">` +
        `<path class="ix-edge" data-k="er" d="M212 118 C252 118 252 92 300 92"/>` +
        `<path class="ix-edge" data-k="ec" d="M212 134 C252 134 252 226 300 226"/>` +
        box("you", 20, 92, 192, 68, "Your stack", "wallet · RPC · indexer", "is-you") +
        `<rect class="ix-frame" x="300" y="12" width="360" height="160" rx="12"/><text class="ix-cap" x="318" y="38">Standard RPC · chain ID, blocks, logs, receipts</text>` +
        CHAINS.map((c, i) => box("c" + i, 318 + i * 112, 74, 100, 70, c.replace("Ethereum mainnet", "Ethereum"), "")).join("") +
        box("cmp", 300, 194, 360, 64, "Composer", "cross-chain calls only") + `</svg>`;
  };

  const ICON = { ok: "✓" };
  const set = (k, st) => {
    const el = fig.querySelector(`[data-k="${k}"]`); if (!el) return;
    el.dataset.s = st;
    const ic = el.querySelector(".ix-ic"); if (ic) ic.textContent = ICON[st] || "";
  };
  const STEPS = [[200, "you", "on"], [400, "er", "run"], [800, "c0", "ok"], [1200, "c1", "ok"], [1600, "c2", "ok"], [2100, "ec", "run"], [2500, "cmp", "ok"]];
  let timers = [], loop = 0;
  const play = () => {
    timers.forEach(clearTimeout); timers = []; clearTimeout(loop);
    fig.querySelectorAll("[data-k]").forEach((el) => set(el.dataset.k, ""));
    status.classList.remove("on");
    const at = (ms, fn) => (reduce ? fn() : timers.push(setTimeout(fn, ms)));
    STEPS.forEach(([ms, k, st]) => at(ms, () => set(k, st)));
    at(2700, () => status.classList.add("on"));
    if (!reduce) loop = setTimeout(play, 6000);
  };

  build();
  narrow.addEventListener("change", () => { build(); play(); });
  window.__ixPlay = play; // test hook
  const r = root.getBoundingClientRect();
  if (reduce || !("IntersectionObserver" in window) || (r.top < innerHeight && r.bottom > 0)) return play(); // already in view: start now
  const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { io.disconnect(); play(); } }, { threshold: 0.35 });
  io.observe(root);
})();
