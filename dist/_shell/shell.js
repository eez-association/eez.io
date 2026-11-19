// Shared header: dropdowns open on hover (pointer) or click/Enter; mobile menu behind a toggle.
(() => {
  const eh = document.getElementById("eh");
  if (!eh) return;
  const menus = [...eh.querySelectorAll(".eh-menu")];
  const close = (except) => menus.forEach((m) => {
    if (m === except) return;
    m.classList.remove("is-open");
    m.querySelector(".eh-trigger").setAttribute("aria-expanded", "false");
  });
  const open = (m) => { close(m); m.classList.add("is-open"); m.querySelector(".eh-trigger").setAttribute("aria-expanded", "true"); };
  const fine = matchMedia("(hover: hover) and (min-width: 761px)");
  let timer;
  menus.forEach((m) => {
    const t = m.querySelector(".eh-trigger");
    // On hover devices the menu is already open when the click lands, so a click keeps it open.
    t.addEventListener("click", () => (fine.matches || !m.classList.contains("is-open") ? open(m) : close()));
    // Short grace period on leave, so a diagonal move into the menu doesn’t close it.
    m.addEventListener("mouseenter", () => { if (!fine.matches) return; clearTimeout(timer); open(m); });
    m.addEventListener("mouseleave", () => { if (!fine.matches) return; clearTimeout(timer); timer = setTimeout(() => close(), 250); });
    // Keyboard: Down arrow from the button moves into the menu.
    t.addEventListener("keydown", (e) => { if (e.key === "ArrowDown") { e.preventDefault(); open(m); m.querySelector(".eh-drop a").focus(); } });
  });
  document.addEventListener("click", (e) => { if (!eh.contains(e.target)) { close(); eh.classList.remove("is-open"); } });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { close(); eh.classList.remove("is-open"); } });
  const tg = eh.querySelector(".eh-toggle");
  tg.addEventListener("click", () => { const o = !eh.classList.contains("is-open"); eh.classList.toggle("is-open", o); tg.setAttribute("aria-expanded", String(o)); });
  // Mark where we are.
  const p = location.pathname.replace(/\.html$/, "").replace(/\/$/, "");
  eh.querySelectorAll(".eh-drop a[href^='/']").forEach((a) => { if (a.getAttribute("href") === p) { a.setAttribute("aria-current", "page"); a.closest(".eh-menu").classList.add("is-here"); } });
})();
