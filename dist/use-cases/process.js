// Tabbed process steps (port of hirael process-02). Click or arrow keys select a step.
document.querySelectorAll(".proc").forEach((proc) => {
  const tabs = [...proc.querySelectorAll(".proc-tab")];
  const select = (i, focus) => {
    tabs.forEach((t, k) => {
      const on = k === i;
      t.setAttribute("aria-selected", on);
      t.tabIndex = on ? 0 : -1;
      t.classList.toggle("done", k < i);
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    });
    if (focus) tabs[i].focus();
  };
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => select(i));
    t.addEventListener("keydown", (e) => {
      const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
      if (k) { e.preventDefault(); select((i + k + tabs.length) % tabs.length, true); }
      else if (e.key === "Home") { e.preventDefault(); select(0, true); }
      else if (e.key === "End") { e.preventDefault(); select(tabs.length - 1, true); }
    });
  });
});
