// Site header. Below 900px the nav folds behind a Menu button; this opens and closes it.
// Closes on Escape (focus returns to the button), on a click outside, on following a link,
// and when the window grows back past the breakpoint.
(() => {
  const btn = document.querySelector(".nav-toggle"), nav = document.getElementById("site-nav");
  if (!btn || !nav) return;
  const head = btn.closest(".site-head");
  const set = (open) => { btn.setAttribute("aria-expanded", String(open)); head.classList.toggle("nav-open", open); };
  btn.addEventListener("click", () => set(btn.getAttribute("aria-expanded") !== "true"));
  nav.addEventListener("click", (e) => { if (e.target.closest("a")) set(false); });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && head.classList.contains("nav-open")) { set(false); btn.focus(); }
  });
  document.addEventListener("click", (e) => { if (!head.contains(e.target)) set(false); });
  matchMedia("(min-width: 901px)").addEventListener("change", (m) => { if (m.matches) set(false); });
})();

// First-touch source for this visit (utm_source, else the referring site, else "direct"), and the
// landing card or button the visitor chose. The intake sends both to Tally as hidden fields.
(() => {
  const store = (k, v) => { try { sessionStorage.setItem(k, v); } catch (e) {} };
  const has = (k) => { try { return !!sessionStorage.getItem(k); } catch (e) { return true; } };
  if (!has("eez-source")) {
    const utm = new URLSearchParams(location.search).get("utm_source");
    let ref = "";
    try { const u = new URL(document.referrer); if (u.host !== location.host) ref = u.host; } catch (e) {}
    store("eez-source", utm || ref || "direct");
  }
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-door]");
    if (a) store("eez-door", a.dataset.door);
  });
})();
