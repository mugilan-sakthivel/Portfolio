// cursor-following project preview card for .v2-row[data-preview]
const fine = window.matchMedia("(hover: hover) and (pointer: fine)");
const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
const holder = document.createElement("div");
holder.className = "row-preview";
holder.setAttribute("aria-hidden", "true");
const card = document.createElement("span");
card.className = "row-preview__card";
const img = document.createElement("img");
img.alt = "";
img.decoding = "async";
card.appendChild(img);
holder.appendChild(card);
document.body.appendChild(holder);

let tx = 0, ty = 0, x = 0, y = 0, active = false, raf = 0;

const loop = () => {
  x += (tx - x) * 0.18;
  y += (ty - y) * 0.18;
  const tilt = Math.max(-7, Math.min(7, (tx - x) * 0.12));
  holder.style.transform = `translate3d(${x}px, ${y}px, 0)`;
  card.style.setProperty("--pt", `${tilt.toFixed(2)}deg`);
  if (active || Math.abs(tx - x) > 0.3) raf = requestAnimationFrame(loop);
  else raf = 0;
};

const start = () => { if (!raf) raf = requestAnimationFrame(loop); };

for (const row of document.querySelectorAll(".v2-row[data-preview]")) {
  row.addEventListener("pointerenter", (e) => {
    if (e.pointerType !== "mouse" || !fine.matches || reduced.matches) return;
    const src = row.getAttribute("data-preview");
    if (img.getAttribute("src") !== src) img.src = src;
    tx = e.clientX; ty = e.clientY;
    x = tx; y = ty + 6;
    active = true;
    holder.classList.add("is-visible");
    start();
  });
  row.addEventListener("pointermove", (e) => {
    if (!active) return;
    tx = e.clientX; ty = e.clientY;
    start();
  });
  row.addEventListener("pointerleave", () => {
    active = false;
    holder.classList.remove("is-visible");
  });
}
