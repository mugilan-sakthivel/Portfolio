// bio expander: collapsed -> stage1 -> stage2 -> stage1 -> collapsed
const btn = document.querySelector("[data-v2-more-btn]");
const s1 = document.querySelector("[data-v2-stage1]");
const s2 = document.querySelector("[data-v2-stage2]");
if (btn && s1 && s2) {
  const label = btn.querySelector("[data-v2-more-label]");
  const chev = btn.querySelector(".v2-more-btn__chev");
  let state = 0;   // 0 = only p1, 1 = p2+p3, 2 = p4+p5
  let dir = 1;     // 1 climbing, -1 descending

  const render = () => {
    s1.classList.toggle("is-open", state === 1);
    s2.classList.toggle("is-open", state === 2);
    s1.setAttribute("aria-hidden", String(state !== 1));
    s2.setAttribute("aria-hidden", String(state !== 2));
    btn.setAttribute("aria-expanded", String(state !== 0));
    const goingUp = state === 0 || (state === 1 && dir === 1);
    label.textContent = goingUp ? "more" : "less";
    if (chev) chev.style.transform = goingUp ? "rotate(0deg)" : "rotate(180deg)";
  };

  btn.addEventListener("click", () => {
    if (state === 0) { state = 1; dir = 1; }
    else if (state === 1) { state = (dir === 1) ? 2 : 0; if (state === 0) dir = 1; }
    else { state = 1; dir = -1; }
    render();
  });
  render();
}
