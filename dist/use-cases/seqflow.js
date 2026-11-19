// Step sections as a sequence diagram (optional) + timeline + one caption for the current step.
// Markup: <div class="sqf"><script type="application/json">{spec}</script></div>
(() => {
  const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const STEP = 5200; // ms per step while it plays on its own: long enough to read the caption

  const mount = (root) => {
    const spec = JSON.parse(root.querySelector("script[type='application/json']").textContent);
    const steps = spec.steps, n = steps.length;
    let svg = null, chip = null, X = {}, rows = [];

    // ---------- diagram ----------
    if (!spec.timeline) {
      const lanes = spec.lanes, sides = { a: lanes.filter((l) => l.side === "a"), b: lanes.filter((l) => l.side === "b") };
      Object.entries(sides).forEach(([side, list]) => list.forEach((l, k) => { X[l.id] = (side === "a" ? 0 : 480) + 480 * (k + 0.5) / list.length; }));
      const w = Math.min(180, 480 / Math.max(sides.a.length, sides.b.length) - 24);
      let y = 110, body = "";
      const b = spec.band;
      steps.forEach((s, i) => {
        if (b && i === b.from) y += 8;
        const x1 = X[s.frm], x2 = X[s.to], d = x2 > x1 ? 1 : -1, ly = y + 38;
        rows.push({ x1: x1 + 12 * d, x2: x2 - 14 * d, y: ly });
        body += `<g class="step" data-s="${i}"><text class="lbl" x="${(x1 + x2) / 2}" y="${y + 24}" text-anchor="middle">${esc(s.label)}</text>` +
          `<path class="ln" d="M${x1 + 12 * d} ${ly}H${x2 - 14 * d}" marker-end="url(#sqf-ah)"/><circle class="dot" cx="${x1}" cy="${ly}" r="7"/></g>`;
        y += 60;
        if (b && i === b.to) y += 34;
      });
      const H = y + 4;
      let band = "";
      if (b) {
        const y0 = 110 + 4, y1 = y - 8;
        band = `<g class="band"><rect x="20" y="${y0}" width="920" height="${y1 - y0}" rx="12"/><text class="bl" x="930" y="${y1 - 12}" text-anchor="end">${esc(b.label)}</text></g>`;
      }
      const hdr = lanes.map((l) => `<g class="hdr${l.ct ? " ct" : ""}"><rect x="${X[l.id] - w / 2}" y="34" width="${w}" height="56" rx="10"/><text x="${X[l.id]}" y="67" text-anchor="middle">${esc(l.name)}</text></g>`).join("");
      const life = lanes.map((l) => `<line class="life" x1="${X[l.id]}" y1="90" x2="${X[l.id]}" y2="${H}"/>`).join("");
      root.insertAdjacentHTML("beforeend", `<p class="sqf-legend"><span><i></i>A call or a step</span>${b ? `<span><i class="b"></i>One transaction</span>` : ""}</p>` +
        `<svg class="sqf-dia" viewBox="0 0 960 ${H + 4}" role="img" xmlns="http://www.w3.org/2000/svg"><title>${esc(spec.left)} on the left, ${esc(spec.right)} on the right: ${esc(steps.map((s) => s.title).join(", then "))}.</title>` +
        `<defs><marker id="sqf-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--ink-body)"/></marker></defs>` +
        `${band}<text class="grp" x="20" y="18">${esc(spec.left)}</text><text class="grp" x="940" y="18" text-anchor="end">${esc(spec.right)}</text>` +
        `<line class="bound" x1="480" y1="6" x2="480" y2="${H}"/>${life}${hdr}${body}<circle class="chip" cx="0" cy="0" r="5"/></svg>`);
      svg = root.querySelector(".sqf-dia"); chip = svg.querySelector(".chip");
    }

    // ---------- timeline + caption ----------
    root.insertAdjacentHTML("beforeend", `<div class="sqf-bottom${spec.timeline ? " only" : ""}"><ol class="sqf-track" role="none" style="grid-template-columns:repeat(${n},minmax(0,1fr)) auto">` +
      steps.map((s, i) => `<li data-s="${i}" tabindex="0" role="button" aria-label="${esc(s.title)}"><span class="time">${esc(s.top)}</span><span class="short">${esc(s.short)}</span><span class="bar"></span></li>`).join("") +
      `<li class="rp" role="none"><button class="sqf-replay" type="button" aria-label="Replay">↻</button></li></ol><div class="sqf-cap" aria-live="polite"></div></div>`);
    const items = [...root.querySelectorAll(".sqf-track li[data-s]")], cap = root.querySelector(".sqf-cap");
    const groups = svg ? [...svg.querySelectorAll(".step")] : [];
    const capHTML = (s) => `<div class="hd"><h3>${s.title}</h3><span class="tag">${s.tag}</span></div>` +
      `<p>${s.lead ? `<span class="lead">${s.lead}.</span> ` : ""}${s.detail}</p>` + (s.why ? `<p class="why"><b>Why:</b> ${s.why}</p>` : "") +
      (s.bullets.length ? `<ul>${s.bullets.map(([t, gate]) => `<li${gate ? ' class="gate"' : ""}>${t}</li>`).join("")}</ul>` : "");
    // keep the box as tall as the longest caption, so the page doesn't jump between steps
    const fit = () => { cap.style.minHeight = ""; let h = 0; steps.forEach((s) => { cap.innerHTML = capHTML(s); h = Math.max(h, cap.offsetHeight); }); cap.style.minHeight = h + "px"; cap.innerHTML = capHTML(steps[Math.max(0, shown)]); };

    let timers = [], shown = -1, played = false, io = null;
    const stop = () => { played = true; io && io.disconnect(); };
    const clear = () => { timers.forEach(clearTimeout); timers = []; chip && chip.getAnimations().forEach((a) => a.cancel()); };
    const set = (i) => {
      [groups, items].forEach((list) => list.forEach((el) => { const k = +el.dataset.s; el.classList.toggle("on", k === i); el.classList.toggle("did", k < i); }));
      if (svg && spec.band) svg.querySelector(".band").classList.toggle("on", i >= spec.band.from);
      const k = Math.min(i, n - 1);
      if (k < 0 || k === shown) return;
      shown = k; cap.classList.add("fade");
      setTimeout(() => { cap.innerHTML = capHTML(steps[k]); cap.classList.remove("fade"); }, 180);
    };
    const draw = (i) => {
      if (!svg || reduce) return;
      const g = groups[i], ln = g.querySelector(".ln"), r = rows[i];
      const L = ln.getTotalLength(); ln.style.transition = "none"; ln.style.strokeDasharray = `${L}`; ln.style.strokeDashoffset = `${L}`;
      ln.getBoundingClientRect(); ln.style.transition = "stroke-dashoffset .9s cubic-bezier(.2,.7,.2,1)"; ln.style.strokeDashoffset = "0";
      timers.push(setTimeout(() => { ln.style.strokeDasharray = ""; ln.style.strokeDashoffset = ""; ln.style.transition = ""; }, 1000));
      chip.animate([{ transform: `translate(${r.x1}px, ${r.y}px)`, opacity: 0 }, { opacity: 1, offset: .15 }, { opacity: 1, offset: .85 }, { transform: `translate(${r.x2}px, ${r.y}px)`, opacity: 0 }],
        { duration: 1800, easing: "cubic-bezier(.4,0,.2,1)", fill: "forwards" });
    };
    const play = () => {
      clear();
      if (reduce) { set(n); return; }
      set(-1);
      steps.forEach((s, i) => timers.push(setTimeout(() => { set(i); draw(i); }, 300 + i * STEP)));
      timers.push(setTimeout(() => set(n), 300 + n * STEP));
    };
    const pick = (i) => { clear(); stop(); set(i); draw(i); };
    items.forEach((li) => {
      li.addEventListener("click", () => pick(+li.dataset.s));
      li.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(+li.dataset.s); } });
    });
    root.querySelector(".sqf-replay").addEventListener("click", () => { stop(); play(); });

    shown = 0; fit(); shown = -1;
    addEventListener("resize", () => { clearTimeout(fit.t); fit.t = setTimeout(fit, 200); });
    if (reduce) { set(n); return; }
    set(0); shown = 0;
    // play once, the first time the section scrolls into view, unless the reader has already picked a step
    io = new IntersectionObserver(([en]) => { if (en.isIntersecting && !played) { stop(); play(); } }, { threshold: 0.35 });
    io.observe(root);
  };
  document.querySelectorAll(".sqf").forEach(mount);
})();
