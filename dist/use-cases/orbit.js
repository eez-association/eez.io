// Landing orbit. One scroll position drives every piece, so they move together:
//   0.00       opening: eyebrow, headline and the small colour EEZ mark, centred
//   0.01-0.07  the first scroll brings in the subtitle and the partner line; the mark steps down under them
//   0.07-0.24  hold: the reader has time to read them before anything else moves (about three wheel ticks)
//   0.24-0.40  the mark grows and travels to the figure’s centre, the headline rises, the layer list slides in
//   0.38-0.52  the mark opens into three rings; Ethereum mainnet appears in the centre
//   0.54-0.65  public rollups move out onto ring 1
//   0.68-0.79  new chains onto ring 2
//   0.82-0.94  permissioned networks onto ring 3, then the full picture holds
// The stage is pinned under the site header while the section scrolls. Reduced motion: no pinning,
// the full picture at once.
(() => {
  const root = document.querySelector(".orb");
  if (!root) return;
  const stage = root.querySelector(".orb-stage"), head = root.querySelector(".page-head"), fig = root.querySelector(".orb-fig");
  const say = () => [...head.querySelectorAll(".lede, .orb-with")];
  const side = root.querySelector(".orb-side"), cue = root.querySelector(".orb-cue"), cta = root.querySelector(".orb-cta"), legend = [...root.querySelectorAll(".orb-legend li")];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // three tiles per ring, 60° apart from the neighbouring ring’s tiles, and every ring turns at the
  // same speed, so tiles on different rings never run into each other
  const RINGS = [
    { r: 0.52, n: 3, a0: 90, labels: ["RollupX", "EEZ-X Devnet", "Your rollup"] },
    { r: 0.72, n: 2, a0: 0, labels: ["App chain", "Non-EVM chain"] },
    { r: 0.92, n: 2, a0: 60, labels: ["Bank network", "Consortium"] },
  ];
  const CORE = 0.28; // the Ethereum core’s radius, as a share of the figure’s half-width
  const TEXT = [0.01, 0.07], INTRO = [0.24, 0.4], OPEN = [0.38, 0.52];
  const WIN = [OPEN, [0.54, 0.65], [0.68, 0.79], [0.82, 0.94]]; // per layer: 0 = Ethereum
  const MARK = 0.26; // the mark’s width in the figure, as a share of the figure, just before it opens
  const clamp = (x) => Math.max(0, Math.min(1, x));
  const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const span = (p, [a, b]) => ease(clamp((p - a) / (b - a)));
  const mix = (a, b, t) => a + (b - a) * t;

  // ---------- build ----------
  fig.insertAdjacentHTML("beforeend",
    `<svg class="orb-rings" viewBox="-100 -100 200 200" aria-hidden="true"><defs><linearGradient id="orb-g" x1="0" y1="0" x2="1" y2="1">` +
    `<stop offset="0" stop-color="var(--grad-mint)"/><stop offset=".5" stop-color="var(--grad-steel)"/><stop offset="1" stop-color="var(--grad-indigo)"/></linearGradient></defs>` +
    RINGS.map((g, i) => `<circle class="orb-ring" data-i="${i}" r="${g.r * 100}"/>`).join("") + `</svg>` +
    `<div class="orb-core"><span class="k">Settles to</span><b>Ethereum mainnet</b></div>`);
  stage.insertAdjacentHTML("beforeend", `<img class="orb-mark" src="system/logos/eez-mark-color.svg" alt="">`);
  const tiles = [];
  RINGS.forEach((g, i) => {
    const orbit = document.createElement("div");
    orbit.className = "orb-orbit"; orbit.dataset.i = i;
    for (let k = 0; k < g.n; k++) {
      const t = document.createElement("span");
      t.className = "orb-tile"; t.textContent = g.labels ? g.labels[k] : g.label;
      t.dataset.a = g.a0 + (360 / g.n) * k;
      orbit.appendChild(t); tiles.push({ el: t, ring: i });
    }
    fig.appendChild(orbit);
  });
  const mark = stage.querySelector(".orb-mark"), core = fig.querySelector(".orb-core"), rings = [...fig.querySelectorAll(".orb-ring")];
  const RATIO = 428 / 271; // the mark’s height / width

  // ---------- layout: where everything sits at the end, and where the opening lockup sits ----------
  let L = null;
  const measure = () => {
    [head, side].forEach((e) => (e.style.transform = ""));
    // on phones the figure fills the height the text leaves; keep it square, or tiles drift off their rings
    fig.style.width = fig.style.height = "";
    const r0 = fig.getBoundingClientRect();
    if (Math.abs(r0.width - r0.height) > 1) fig.style.width = fig.style.height = `${Math.min(r0.width, r0.height)}px`;
    const s = stage.getBoundingClientRect(), h = head.getBoundingClientRect(), f = fig.getBoundingClientRect();
    const w0 = Math.max(48, Math.min(96, s.width * 0.08)); // the mark at the start: small, and it scales with the screen
    const gap = Math.max(18, s.height * 0.035);
    const mh = w0 * RATIO, h1 = head.querySelector("h1").getBoundingClientRect();
    // two opening lockups, both centred: A = eyebrow + headline + mark (first screen),
    // B = the same with the subtitle and partner line, which the first scroll brings in
    const hA = h1.bottom - h.top, hB = h.height;
    const topA = Math.max(16, (s.height - (hA + gap + mh)) / 2), topB = Math.max(16, (s.height - (hB + gap + mh)) / 2);
    L = {
      half: f.width / 2,
      dyA: topA - (h.top - s.top), dyB: topB - (h.top - s.top), // headline: from the centred lockup up to its place
      m0: { x: s.width / 2, yA: topA + hA + gap + mh / 2, yB: topB + hB + gap + mh / 2, w: w0 },
      m1: { x: f.left - s.left + f.width / 2, y: f.top - s.top + f.height / 2, w: f.width * MARK },
    };
  };

  // ---------- one frame for progress p ----------
  let active = -2;
  let kb = false; // a keyboard user gets the header at once, so Tab never lands on something unseen
  addEventListener("keydown", (e) => { if (e.key === "Tab" && !kb) { kb = true; document.documentElement.classList.remove("hdr-away"); } });
  const draw = (p) => {
    // the legend first: on phones the active layer’s note changes the figure’s room, so re-measure
    const now = p < OPEN[0] ? -1 : p < 0.53 ? 0 : p < 0.67 ? 1 : p < 0.81 ? 2 : 3;
    if (now !== active) {
      active = now;
      legend.forEach((li, i) => { li.classList.toggle("on", i === now); li.classList.toggle("did", i < now); });
      L = null;
    }
    if (!L) measure();
    const k = span(p, INTRO), open = span(p, OPEN), t = span(p, TEXT);
    say().forEach((e) => { e.style.opacity = String(t); e.style.transform = `translateY(${8 * (1 - t)}px)`; });
    const m0y = mix(L.m0.yA, L.m0.yB, t);
    // the scroll cue stays through the whole build and leaves once the full picture holds
    cue.style.opacity = String(1 - span(p, [0.92, 0.98]));
    // the buttons come last, once every layer is on its ring
    if (cta && !root.classList.contains("still")) { const c = span(p, [0.88, 0.97]); cta.style.opacity = String(c); cta.style.visibility = c ? "visible" : "hidden"; cta.style.transform = `translateY(${10 * (1 - c)}px)`; }
    // the site header stays away on the opening scene; the first scroll (or the first Tab) brings it in
    document.documentElement.classList.toggle("hdr-away", p < 0.015 && scrollY < 12 && !kb);
    // headline and layer list
    head.style.transform = `translateY(${mix(L.dyA, L.dyB, t) * (1 - k)}px)`;
    const sk = span(p, [0.3, 0.46]);
    side.style.opacity = String(sk);
    side.style.visibility = sk ? "visible" : "hidden"; // no focus stops on an invisible list
    side.style.transform = `translateX(${24 * (1 - sk)}px)`;
    // the mark: small above the headline, then large at the figure’s centre, then it opens into the rings
    const w = mix(L.m0.w, L.m1.w, k) * (1 + open * 1.2);
    mark.style.width = `${w}px`;
    mark.style.transform = `translate(${mix(L.m0.x, L.m1.x, k) - w / 2}px, ${mix(m0y, L.m1.y, k) - (w * RATIO) / 2}px)`;
    mark.style.opacity = String(1 - clamp(open * 1.5));
    rings.forEach((c, i) => {
      const on = span(p, WIN[i + 1]);
      c.style.opacity = String(open * (0.35 + 0.65 * on));
      c.setAttribute("transform", `scale(${0.18 + 0.82 * open})`); // around the centre: the viewBox origin
    });
    core.style.opacity = String(clamp((open - 0.45) / 0.55));
    core.style.transform = `translate(-50%, -50%) scale(${0.85 + 0.15 * open})`;
    tiles.forEach(({ el, ring }) => {
      const t = span(p, WIN[ring + 1]), a = (+el.dataset.a * Math.PI) / 180, r = (CORE + (RINGS[ring].r - CORE) * t) * L.half; // out from the core’s edge
      el.style.opacity = String(clamp(t * 1.4));
      el.style.setProperty("--x", `${r * Math.cos(a)}px`); el.style.setProperty("--y", `${r * Math.sin(a)}px`);
    });
  };

  const hdr = () => { const h = document.querySelector("header"); root.style.setProperty("--hdr", `${h && getComputedStyle(h).position === "sticky" ? h.offsetHeight : 0}px`); };
  hdr();
  if (reduce) { root.classList.add("still"); addEventListener("resize", () => { L = null; draw(1); }); draw(1); return; }

  // scroll progress through the pinned section, eased toward the target so wheel steps glide
  let target = 0, cur = 0, raf = 0;
  const off = () => parseFloat(root.style.getPropertyValue("--hdr")) || 0;
  const read = () => { const b = root.getBoundingClientRect(), run = root.offsetHeight - (innerHeight - off()); target = clamp((off() - b.top) / Math.max(1, run)); };
  const tick = () => { cur += (target - cur) * 0.14; if (Math.abs(target - cur) < 0.0005) cur = target; draw(cur); raf = cur === target ? 0 : requestAnimationFrame(tick); };
  const kick = () => { read(); if (!raf) raf = requestAnimationFrame(tick); };
  addEventListener("scroll", kick, { passive: true });
  addEventListener("resize", () => { hdr(); L = null; kick(); });
  draw(0); kick();

  // a layer in the list scrolls to the point where that layer has arrived
  legend.forEach((li, i) => li.querySelector(".lg").addEventListener("click", () => {
    const run = root.offsetHeight - (innerHeight - off()), top = root.getBoundingClientRect().top + scrollY - off();
    scrollTo({ top: top + run * (WIN[i][1] + 0.01), behavior: "smooth" });
  }));
})();
