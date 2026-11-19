// Shared line motion for the audience-page heroes: a path draws itself while a soft light runs ahead
// along it, eased in and out. enhance() turns each `<prefix>-edge[data-k]` into a faint base line plus a
// drawable trace (keeps the data-k), a dot and a glow. One flow per hero; next() cancels any run in flight.
window.HeroFlow = (fig, prefix) => {
  const NS = "http://www.w3.org/2000/svg";
  const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  let run = 0;
  const enhance = () => {
    fig.querySelectorAll(`path.${prefix}-edge[data-k]`).forEach((base) => {
      const k = base.dataset.k, trace = base.cloneNode();
      base.removeAttribute("data-k");
      trace.setAttribute("class", `${prefix}-trace`);
      const mk = (cls, r) => { const c = document.createElementNS(NS, "circle"); c.setAttribute("class", cls); c.setAttribute("r", r); c.dataset.k = `${k}-${cls.slice(-3)}`; return c; };
      base.after(trace, mk(`${prefix}-glow`, 7), mk(`${prefix}-dot`, 2.6));
    });
  };
  const traces = () => [...fig.querySelectorAll(`.${prefix}-trace`)];
  const hide = (p) => { const L = p.getTotalLength(); p.style.strokeDasharray = `${L} ${L}`; p.style.strokeDashoffset = String(L); };
  const show = (p) => { p.style.strokeDasharray = "none"; p.style.strokeDashoffset = "0"; };
  const lights = (k) => [fig.querySelector(`[data-k="${k}-dot"]`), fig.querySelector(`[data-k="${k}-low"]`)];
  const tween = (ms, fn, id) => new Promise((done) => {
    const t0 = performance.now();
    const f = (now) => { if (id !== run) return done(false); const k = Math.min(1, (now - t0) / ms); fn(ease(k), k); k < 1 ? requestAnimationFrame(f) : done(true); };
    requestAnimationFrame(f);
  });
  const wait = (ms, id) => new Promise((done) => setTimeout(() => done(id === run), ms));
  const draw = (k, ms, id) => {
    const p = fig.querySelector(`.${prefix}-trace[data-k="${k}"]`), [d, g] = lights(k), L = p.getTotalLength();
    p.style.strokeDasharray = `${L} ${L}`;
    return tween(ms, (e, t) => {
      p.style.strokeDashoffset = String(L * (1 - e));
      const pt = p.getPointAtLength(L * e), o = Math.sin(Math.PI * Math.min(1, t * 1.08));
      [d, g].forEach((c) => { c.setAttribute("cx", pt.x); c.setAttribute("cy", pt.y); });
      d.style.opacity = String(o); g.style.opacity = String(o * 0.55);
    }, id);
  };
  const retract = (ms, id) => {
    const ps = traces(), Ls = ps.map((p) => p.getTotalLength());
    ps.forEach((p, i) => (p.style.strokeDasharray = `${Ls[i]} ${Ls[i]}`));
    return tween(ms, (e) => ps.forEach((p, i) => (p.style.strokeDashoffset = String(Ls[i] * e))), id);
  };
  const reset = () => { traces().forEach(hide); fig.querySelectorAll(`.${prefix}-dot, .${prefix}-glow`).forEach((c) => (c.style.opacity = "0")); };
  const final = () => traces().forEach(show);
  return { enhance, reset, final, draw, retract, wait, next: () => ++run };
};
