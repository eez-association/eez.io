// "Start where you are" carousel, ported from the EEZ homepage mock-up’s "What you can build" ring:
// one row of cards, the centre one in focus (light), the others smaller and fading toward the edges.
// A side card brings itself to the centre; the centre card opens its page. Drag, wheel, arrows, dots
// and the keyboard all move it. Without this script the cards stay a plain grid.
(() => {
  const ring = document.getElementById("ring");
  if (!ring) return;
  const slides = [...ring.querySelectorAll(".slide")], n = slides.length;
  const cards = slides.map((s) => s.querySelector("a"));
  const cap = document.getElementById("ringcap"), dots = document.getElementById("rdots");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  ring.classList.add("js");
  // the cards are links: stop the browser’s own link drag and text selection, which would steal the gesture
  cards.forEach((a) => { a.draggable = false; });
  ring.addEventListener("dragstart", (e) => e.preventDefault());
  slides.forEach((s, i) => {
    const b = document.createElement("button");
    b.type = "button";
    b.setAttribute("aria-label", cards[i].querySelector("h3").textContent.replace(/[\[\]]/g, "").trim());
    b.addEventListener("click", () => go(i));
    dots.appendChild(b);
  });

  let cur = 0, pos = 0;
  const geo = () => {
    const w = ring.clientWidth, narrow = w < 720;
    const cw = narrow ? Math.min(270, w * 0.72) : 300;
    ring.style.setProperty("--cw", cw + "px");
    return { cw };
  };
  const wrap = (d) => { d = ((d % n) + n) % n; return d > n / 2 ? d - n : d; };
  const touch = () => matchMedia("(hover: none)").matches;

  function layout() {
    const g = geo();
    let tall = 0;
    slides.forEach((s, i) => {
      const d = wrap(i - pos), a = Math.abs(d);
      const x = d * (g.cw + 24), sc = 1 - 0.06 * Math.min(a, 3);
      s.style.transform = `translate(${x.toFixed(1)}px,0) scale(${sc.toFixed(3)})`;
      s.style.opacity = (a < 1.5 ? 1 : Math.max(0, 1 - (a - 1.5) * 0.9)).toFixed(2);
      s.style.zIndex = String(10 - Math.round(a));
      const on = i === cur;
      s.classList.toggle("center", on);
      s.setAttribute("aria-hidden", on ? "false" : "true");
      cards[i].tabIndex = on ? 0 : -1;
      tall = Math.max(tall, cards[i].offsetHeight);
    });
    ring.style.height = tall + 48 + "px"; // room for the lift and the shadow
    cap.textContent = touch() ? "Tap the card to open it" : "Click the card to open it";
    [...dots.children].forEach((d, i) => { d.classList.toggle("on", i === cur); d.setAttribute("aria-current", i === cur ? "true" : "false"); });
  }
  const closest = (i) => { let best = i, bd = 1e9; for (let k = -2; k <= 2; k++) { const v = i + k * n; if (Math.abs(v - pos) < bd) { bd = Math.abs(v - pos); best = v; } } return best; };
  function go(i) { cur = ((i % n) + n) % n; pos = closest(cur); layout(); }

  // drag (mouse or touch); a drag never counts as a click on a card
  let down = null, moved = false, suppress = false;
  ring.addEventListener("pointerdown", (e) => {
    if (e.button > 0) return;
    down = { x: e.clientX, p: pos, id: e.pointerId }; moved = false;
    if (e.pointerType === "mouse") e.preventDefault(); // no text selection; the click still fires
  });
  window.addEventListener("pointermove", (e) => {
    if (!down) return;
    const dx = e.clientX - down.x;
    if (!moved && Math.abs(dx) > 6) { moved = true; ring.classList.add("drag"); try { ring.setPointerCapture(down.id); } catch (_) {} }
    // one card per card-width of travel, so the card under the pointer moves with it
    if (moved) { pos = down.p - dx / (parseFloat(ring.style.getPropertyValue("--cw")) + 24); cur = ((Math.round(pos) % n) + n) % n; layout(); }
  });
  const end = () => {
    if (!down) return;
    const wasDrag = moved; down = null; ring.classList.remove("drag");
    if (wasDrag) { suppress = true; pos = Math.round(pos); cur = ((pos % n) + n) % n; layout(); setTimeout(() => (suppress = false), 0); }
  };
  window.addEventListener("pointerup", end);
  window.addEventListener("pointercancel", end);

  // a side card comes to the centre instead of opening; the centre card is a normal link
  ring.addEventListener("click", (e) => {
    const s = e.target.closest(".slide");
    if (!s) return;
    if (suppress) { e.preventDefault(); return; }
    const i = slides.indexOf(s);
    if (i !== cur) { e.preventDefault(); go(i); }
  }, true);

  // horizontal wheel / trackpad swipe
  let acc = 0;
  ring.addEventListener("wheel", (e) => {
    if (Math.abs(e.deltaX) < Math.abs(e.deltaY)) return;
    e.preventDefault(); acc += e.deltaX;
    if (Math.abs(acc) > 60) { go(cur + Math.sign(acc)); acc = 0; }
  }, { passive: false });

  // keyboard: arrows move while focus is on the centre card or the controls
  const nav = ring.parentElement;
  nav.addEventListener("keydown", (e) => {
    if (!e.target.closest(".ring, .ringnav")) return;
    if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
      go(cur + (e.key === "ArrowRight" ? 1 : -1));
      if (ring.contains(e.target)) cards[cur].focus({ preventScroll: true });
      e.preventDefault();
    }
  });
  document.getElementById("rp").addEventListener("click", () => go(cur - 1));
  document.getElementById("rn").addEventListener("click", () => go(cur + 1));

  if (reduce) ring.classList.add("still");
  addEventListener("resize", layout);
  layout();
  // the figures draw a little after load; re-measure the height once they have
  setTimeout(layout, 600);
})();
