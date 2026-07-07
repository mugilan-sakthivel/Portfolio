// bio "more" expander
const btn = document.querySelector("[data-v2-more-btn]");
const box = document.querySelector("[data-v2-more]");
if (btn && box) {
  const label = btn.querySelector("[data-v2-more-label]");
  btn.addEventListener("click", () => {
    const open = !box.classList.contains("is-open");
    box.classList.toggle("is-open", open);
    box.setAttribute("aria-hidden", String(!open));
    btn.setAttribute("aria-expanded", String(open));
    label.textContent = open ? "less" : "more";
  });
}
