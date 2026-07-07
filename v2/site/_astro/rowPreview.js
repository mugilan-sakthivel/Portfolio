// TinkerHub-style tilted preview flyer for .v2-row[data-preview]
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

let hideTimer = 0;
const rows = [...document.querySelectorAll(".v2-row[data-preview]")];
rows.forEach((row, i) => {
  row.addEventListener("pointerenter", (e) => {
    if (e.pointerType !== "mouse" || !fine.matches || reduced.matches) return;
    if (window.innerWidth < 1024) return;
    const src = row.getAttribute("data-preview");
    if (img.getAttribute("src") !== src) img.src = src;

    const r = row.getBoundingClientRect();
    const table = row.closest(".v2-index__table")?.getBoundingClientRect() ?? r;
    const cardW = Math.min(400, window.innerWidth * 0.32) + 16;
    const roomRight = window.innerWidth - table.right;
    // sit to the right of the table when there's room, overlap its right edge when not
    const x = roomRight > cardW + 24
      ? table.right + 28
      : Math.max(table.left + table.width * 0.45, window.innerWidth - cardW - 16);
    const y = Math.min(Math.max(r.top + r.height / 2, 170), window.innerHeight - 170);

    const wasVisible = holder.classList.contains("is-visible");
    if (!wasVisible) holder.style.transition = "none";
    holder.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    if (!wasVisible) { holder.offsetWidth; holder.style.transition = ""; }

    card.style.setProperty("--pt", `${i % 2 ? -4.5 : 4.5}deg`);
    clearTimeout(hideTimer);
    holder.classList.add("is-visible");
  });
  row.addEventListener("pointerleave", () => {
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => holder.classList.remove("is-visible"), 60);
  });
});
