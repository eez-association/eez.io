// Institutions hero: one transaction zigzags across permissioned parties and Ethereum. Lanes: Bank,
// Exchange, Ethereum, Custodian (each party keeps its own rules: lock). The transaction steps
// Bank → Ethereum → Exchange → Ethereum → Custodian inside one frame, and the whole frame lands in one
// block. Rows on desktop, columns on phones. Loops while on screen. Reduced motion: final state.
(() => {
  const root = document.querySelector(".nx");
  if (!root) return;
  const fig = root.querySelector(".nx-fig"), status = root.querySelector(".nx-status");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const narrow = matchMedia("(max-width: 640px)");
  const LANES = [["Issuer", 1, "bond · own chain"], ["Ethereum", 0, "mainnet · USDC"]]; // [name, permissioned, sub]
  // [lane, label, short label]
  const STEPS = [[0, "Lock 1,000 units", "Lock"], [1, "Check eligibility", "Eligible"], [1, "Buyer pays $1m", "Pay $1m"], [0, "Deliver to buyer", "Deliver"]];
  const ARIA = "Delivery versus payment: the issuer locks 1,000 bond units on its own chain, Ethereum checks the buyer is eligible, the buyer pays $1m in USDC on mainnet, and the units are delivered to the buyer on the issuer chain, in one transaction and one block";
  const lock = (x, y) => `<g class="nx-lock" transform="translate(${x} ${y})"><rect x="0" y="4" width="8" height="6.5" rx="1.2"/><path d="M1.8 4V2.6a2.2 2.2 0 0 1 4.4 0V4"/></g>`;
  const step = (k, x, y, w, h, t) => `<g class="nx-step" data-k="${k}" data-s=""><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8"/><text x="${x + w / 2}" y="${y + h / 2 + 4}" text-anchor="middle">${t}</text></g>`;
  const edge = (i, d) => `<path class="nx-edge" d="${d}"/><path class="nx-trace" data-k="l${i}" d="${d}"/>` +
    `<circle class="nx-glow" data-k="g${i}" r="7"/><circle class="nx-dot" data-k="d${i}" r="2.6"/>`;
  const frame = (x, y, w, h) => `<rect class="nx-frame" x="${x}" y="${y}" width="${w}" height="${h}" rx="12"/><rect class="nx-frame-on" data-k="fr" x="${x}" y="${y}" width="${w}" height="${h}" rx="12"/>`;
  const defs = (w) => `<defs><linearGradient id="nx-g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="${w}" y2="0"><stop offset="0" stop-color="#8ae5ac"/><stop offset=".55" stop-color="#6283bd"/><stop offset="1" stop-color="#4439cb"/></linearGradient></defs>`;

  const build = () => {
    let o = "";
    const nL = LANES.length, nS = STEPS.length;
    if (narrow.matches) {
      const W = 320, bandW = (W - 12 - (nL - 1) * 6) / nL, cx = LANES.map((_, i) => 6 + bandW / 2 + i * (bandW + 6)), cw = bandW - 12, top = 96, dy = 58, bh = 32;
      const H = top + dy * (nS - 1) + bh + 48;
      o += `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${ARIA}">` + defs(W);
      LANES.forEach(([n, p, sub], i) => {
        o += `<rect class="nx-band b${i}" data-k="band${i}" x="${cx[i] - bandW / 2}" y="6" width="${bandW}" height="${H - 12}" rx="10"/>`;
        o += (p ? lock(cx[i] - 4, 14) : `<text class="nx-l1tag" x="${cx[i]}" y="23" text-anchor="middle">L1</text>`) +
          `<text class="nx-lane is-sm${p ? "" : " is-l1"}" x="${cx[i]}" y="42" text-anchor="middle">${n.replace("Buyer's custodian", "Custodian")}</text>` +
          `<text class="nx-lsub" x="${cx[i]}" y="56" text-anchor="middle">${sub}</text>`;
      });
      o += frame(3, top - 14, W - 6, dy * (nS - 1) + bh + 28);
      const pos = STEPS.map(([l], i) => [cx[l] - cw / 2, top + i * dy]);
      pos.slice(1).forEach(([x, y], i) => { const [px, py] = pos[i]; o += edge(i, `M${px + cw / 2} ${py + bh} C${px + cw / 2} ${py + bh + 18} ${x + cw / 2} ${y - 18} ${x + cw / 2} ${y}`); });
      o += STEPS.map(([, , t], i) => step("s" + i, pos[i][0], pos[i][1], cw, bh, t)).join("");
      o += `<text class="nx-block" data-k="blk" data-s="" x="${W / 2}" y="${H - 18}" text-anchor="middle">one transaction · block n</text></svg>`;
    } else {
      const W = 700, gap = 72, ry = LANES.map((_, i) => 44 + i * gap), x0 = 130, dx = 144, bw = 118, bh = 36, bandH = 56;
      const H = ry[nL - 1] + bandH / 2 + 40, fx = 116, fw = dx * (nS - 1) + bw + 32;
      o += `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${ARIA}">` + defs(W);
      LANES.forEach(([n, p, sub], i) => {
        o += `<rect class="nx-band b${i}" data-k="band${i}" x="6" y="${ry[i] - bandH / 2}" width="${W - 12}" height="${bandH}" rx="10"/>`;
        o += (p ? lock(18, ry[i] - 14) : `<text class="nx-l1tag" x="18" y="${ry[i] - 4}">L1</text>`) +
          `<text class="nx-lane${p ? "" : " is-l1"}" x="${p ? 32 : 36}" y="${ry[i] - 4}">${n}</text>` +
          `<text class="nx-lsub" x="18" y="${ry[i] + 12}">${sub}</text>`;
      });
      o += frame(fx, 8, fw, ry[nL - 1] + bandH / 2 - 2);
      const pos = STEPS.map(([l], i) => [x0 + i * dx, ry[l] - bh / 2]);
      pos.slice(1).forEach(([x, y], i) => { const [px, py] = pos[i], a = [px + bw, py + bh / 2], b = [x, y + bh / 2], m = (a[0] + b[0]) / 2;
        o += edge(i, `M${a[0]} ${a[1]} C${m} ${a[1]} ${m} ${b[1]} ${b[0]} ${b[1]}`); });
      o += STEPS.map(([, t], i) => step("s" + i, pos[i][0], pos[i][1], bw, bh, t)).join("");
      o += `<text class="nx-block" data-k="blk" data-s="" x="${fx + fw}" y="${H - 12}" text-anchor="end">one transaction · block n</text></svg>`;
    }
    fig.innerHTML = o;
  };

  const $ = (k) => fig.querySelector(`[data-k="${k}"]`);
  const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  let run = 0, hold = 0;
  const tween = (ms, fn, id) => new Promise((done) => {
    const t0 = performance.now();
    const f = (now) => { if (id !== run) return done(false); const k = Math.min(1, (now - t0) / ms); fn(ease(k), k); k < 1 ? requestAnimationFrame(f) : done(true); };
    requestAnimationFrame(f);
  });
  const wait = (ms, id) => new Promise((done) => setTimeout(() => done(id === run), ms));
  // a path draws itself while a soft light runs ahead along it
  const draw = (i, ms, id) => {
    const p = $("l" + i), d = $("d" + i), g = $("g" + i), L = p.getTotalLength();
    p.style.strokeDasharray = `${L} ${L}`;
    return tween(ms, (e, k) => {
      p.style.strokeDashoffset = String(L * (1 - e));
      const pt = p.getPointAtLength(L * e), o = String(Math.sin(Math.PI * Math.min(1, k * 1.08)));
      [d, g].forEach((c) => { c.setAttribute("cx", pt.x); c.setAttribute("cy", pt.y); }); d.style.opacity = o; g.style.opacity = String(o * 0.55);
    }, id);
  };
  const lane = (l) => fig.querySelectorAll(".nx-band").forEach((b, i) => (b.dataset.on = l === "all" ? "soft" : i === l ? "1" : ""));
  const reset = () => {
    fig.querySelectorAll(".nx-trace").forEach((p) => { const L = p.getTotalLength(); p.style.strokeDasharray = `${L} ${L}`; p.style.strokeDashoffset = String(L); });
    fig.querySelectorAll(".nx-dot, .nx-glow").forEach((c) => (c.style.opacity = "0"));
    fig.querySelectorAll("[data-s]").forEach((el) => (el.dataset.s = ""));
    $("fr").dataset.on = ""; const b = $("blk"); b.textContent = b.textContent.replace(/ ✓$/, ""); b.dataset.s = "";
    status.classList.remove("on"); lane(-1);
  };
  const final = () => {
    fig.querySelectorAll(".nx-trace").forEach((p) => (p.style.strokeDashoffset = "0"));
    fig.querySelectorAll(".nx-step").forEach((el) => (el.dataset.s = "ok"));
    $("fr").dataset.on = "1"; const b = $("blk"); b.textContent = b.textContent.replace(/ ✓$/, "") + " ✓"; b.dataset.s = "ok";
    status.classList.add("on"); lane("all");
  };
  const play = async () => {
    const id = ++run; clearTimeout(hold);
    reset();
    if (reduce) return final();
    if (!(await wait(300, id))) return;
    $("s0").dataset.s = "ok"; lane(STEPS[0][0]);
    for (let i = 0; i < STEPS.length - 1; i++) {
      if (!(await wait(i ? 160 : 360, id))) return;
      if (!(await draw(i, 820, id))) return;
      $("s" + (i + 1)).dataset.s = "ok"; lane(STEPS[i + 1][0]);
    }
    if (!(await wait(320, id))) return;
    $("fr").dataset.on = "1"; lane("all");
    const b = $("blk"); b.textContent += " ✓"; b.dataset.s = "ok"; status.classList.add("on");
    if (!(await wait(3200, id))) return;
    // wind back: lines retract, steps and bands settle, then the transaction runs again
    fig.querySelectorAll(".nx-step").forEach((el) => (el.dataset.s = ""));
    $("fr").dataset.on = ""; lane(-1); b.dataset.s = ""; b.textContent = b.textContent.replace(/ ✓$/, "");
    const traces = [...fig.querySelectorAll(".nx-trace")], lens = traces.map((p) => p.getTotalLength());
    if (!(await tween(700, (e) => traces.forEach((p, i) => (p.style.strokeDashoffset = String(lens[i] * e))), id))) return;
    if (!(await wait(500, id))) return;
    hold = setTimeout(() => id === run && play(), 0);
  };

  build();
  narrow.addEventListener("change", () => { build(); play(); });
  window.__nxPlay = play; // test hook
  const r = root.getBoundingClientRect();
  if (reduce || !("IntersectionObserver" in window) || (r.top < innerHeight && r.bottom > 0)) return play(); // already in view: start now
  const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { io.disconnect(); play(); } }, { threshold: 0.35 });
  io.observe(root);
})();
