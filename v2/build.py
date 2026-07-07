#!/usr/bin/env python3
"""1:1 rebuild of danielwhite.uk with content driven by data.json.

Usage: python3 build.py
Reads:  v2/data.json + ../reference/danielwhite (scraped assets)
Writes: v2/site/ (index.html, _astro/, fonts/, images/)
"""
import json
import re
import shutil
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
REF = HERE.parent / "reference" / "danielwhite"
OUT = HERE / "site"
DATA = json.loads((HERE / "data.json").read_text())

S = DATA["site"]

# ---------------------------------------------------------------- helpers

def char_slots(text):
    """char-slot spans used by slot-text (email link, clock)."""
    out = []
    for c in text:
        ch = escape(c)
        out.append(
            f'<span class="char-slot" data-char="{ch}">'
            f'<span class="char-sizer">{ch}</span>'
            f'<span class="char-face">{ch}</span></span>'
        )
    return "".join(out)


def bubble_spans(text, with_semis=False):
    """per-char spans for speech bubbles (--i stagger)."""
    out = []
    for i, c in enumerate(text):
        ch = "&nbsp;" if c == " " else escape(c)
        style = f"--i: {i};" if with_semis else f"--i: {i}"
        out.append(f'<span style="{style}" data-astro-cid-erjq6yp3>{ch}</span>')
    return "".join(out)


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def basic_link(text, href):
    return (
        f'<a class="basic-link" href="{href}" target="_blank" rel="noopener noreferrer" '
        f'data-hover-sound="tick" data-press-sound="press" '
        f'data-astro-cid-j7pv25f6="true" data-astro-cid-rq52bn6l>{escape(text)}</a>'
    )


def email_link():
    em = S["email"]
    return (
        f'<a class="basic-link slot-text" href="mailto:{em}" data-hover-sound="tick" '
        f'data-press-sound="press" data-v2-email="true" data-email="{em}" '
        f'data-astro-cid-j7pv25f6="true" data-astro-cid-rq52bn6l>{char_slots("email")}</a>'
    )


def prose_paragraph(text):
    text = escape(text).replace("{email}", "\x00EMAIL\x00")
    # un-escape the markdown link syntax we still need to parse
    text = LINK_RE.sub(lambda m: basic_link(m.group(1), m.group(2)), text)
    text = text.replace("\x00EMAIL\x00", email_link())
    return f"<p data-astro-cid-j7pv25f6>\n{text}\n</p>"


def tag_html(tag):
    return (
        f'<span class="tag" style="--tag-color: {tag["color"]};" aria-label="{escape(tag["label"])}" '
        f'data-astro-cid-joucddzy> <span class="tag__sweep" data-astro-cid-joucddzy></span> '
        f'<span class="tag__label" data-astro-cid-joucddzy>{escape(tag["label"])}</span> </span>'
    )


def index_row(i, row):
    year_start = " v2-row--year-start" if row.get("year") else ""
    tag = f' {tag_html(row["tag"])}' if row.get("tag") else " "
    preview = f' data-preview="{row["preview"]}"' if row.get("preview") else ""
    inner = (
        f' <span class="v2-row__year" data-astro-cid-xurrqhsc>{escape(row.get("year") or "")}</span> '
        f'<span class="v2-row__title" data-astro-cid-xurrqhsc> {escape(row["title"])}{tag}</span> '
        f'<span class="v2-row__meta" data-astro-cid-xurrqhsc>{escape(row["meta"])}</span> '
    )
    if row.get("href"):
        ext = ' target="_blank" rel="noopener noreferrer"' if row["href"].startswith("http") else ""
        return (
            f'<a style="--row-i: {i}" data-hover-sound="tick" data-press-sound="press" '
            f'href="{row["href"]}"{ext}{preview} data-astro-cid-xurrqhsc="true" '
            f'class="v2-row{year_start}">{inner}</a>'
        )
    return (
        f'<div style="--row-i: {i}" aria-disabled="true"{preview} data-astro-cid-xurrqhsc="true" '
        f'class="v2-row{year_start} v2-row--disabled">{inner}</div>'
    )


def index_section(cfg, slug):
    rows = "".join(index_row(i, r) for i, r in enumerate(cfg["rows"]))
    return (
        f'<section class="v2-index" aria-labelledby="v2-{slug}-heading" data-astro-cid-q257azvz> '
        f'<h2 id="v2-{slug}-heading" data-astro-cid-q257azvz>{escape(cfg["heading"])}</h2> '
        f'<div class="v2-index__table" data-astro-cid-q257azvz>{rows}</div> </section>'
    )


def proof_stat(st, first):
    num = (
        f'<span class="v2-proof__num" data-astro-cid-pfgrcgrj>{escape(st["num"])}</span>'
        if st.get("num")
        else ""
    )
    body = f'{num}{escape(st["text"])}'
    if st.get("href"):
        item = (
            f'<a class="v2-proof__stat" href="{st["href"]}" target="_blank" rel="noopener noreferrer" '
            f'data-hover-sound="tick" data-press-sound="press" data-astro-cid-pfgrcgrj>{body}</a>'
        )
    else:
        item = f'<span class="v2-proof__stat" data-astro-cid-pfgrcgrj>{body}</span>'
    dot = '' if first else '<span class="v2-proof__dot" aria-hidden="true" data-astro-cid-pfgrcgrj>·</span> '
    return dot + item


def proof_section():
    p = DATA["proof"]
    stats = " ".join(proof_stat(s, i == 0) for i, s in enumerate(p["stats"]))
    quotes = []
    for q in p["quotes"]:
        who = (
            f'<a href="{q["who_href"]}" target="_blank" rel="noopener noreferrer" '
            f'data-hover-sound="tick" data-press-sound="press" '
            f'data-astro-cid-pfgrcgrj>{escape(q["who"])}</a>'
            if q.get("who_href")
            else escape(q["who"])
        )
        quotes.append(
            f'<li class="v2-proof__quote" data-astro-cid-pfgrcgrj> '
            f'<q data-astro-cid-pfgrcgrj>{escape(q["q"])}</q> '
            f'<span class="v2-proof__who" data-astro-cid-pfgrcgrj>\n—  {who}, {escape(q["org"])} </span> </li>'
        )
    return (
        f'<aside class="v2-proof" aria-label="{escape(p["aria_label"])}" data-astro-cid-pfgrcgrj> '
        f'<p class="v2-proof__stats" data-astro-cid-pfgrcgrj> '
        f'<a class="v2-proof__lib" href="{p["label_href"]}" target="_blank" rel="noopener noreferrer" '
        f'data-hover-sound="tick" data-press-sound="press" data-astro-cid-pfgrcgrj>{escape(p["label"])}</a> '
        f'<span class="v2-proof__figures" data-astro-cid-pfgrcgrj>{stats}</span> </p> '
        f'<ul class="v2-proof__quotes" data-astro-cid-pfgrcgrj>{"".join(quotes)}</ul> </aside>'
    )


def shelf_frame(i, n, fr):
    # rotation spread ±14deg, quadratic lift, linear x-shift — same maths as source
    t = (2 * i / (n - 1) - 1) if n > 1 else 0  # -1..1
    r = 14 * t
    y = 8 * t * t
    sx = 24 * t
    return (
        f'<button type="button" class="v2-frame" '
        f'style="--r: {r}deg; --y: {y}px; --sx: {sx}px; --z: {i + 1};" '
        f'data-hover-sound="tick" data-press-sound="press" aria-label="{escape(fr["alt"])}" '
        f'data-astro-cid-da7pukvc> '
        f'<span class="bubble v2-frame__bubble" data-astro-cid-da7pukvc="true" data-astro-cid-erjq6yp3> '
        f'{bubble_spans(fr["bubble"])} </span> '
        f'<span class="v2-frame__paper" data-astro-cid-da7pukvc> '
        f'<img src="{fr["img"]}" alt="{escape(fr["alt"])}" width="{fr["width"]}" height="{fr["height"]}" '
        f'loading="eager" decoding="async" data-astro-cid-da7pukvc> </span> </button>'
    )


def shelf_section():
    sh = DATA["shelf"]
    n = len(sh["frames"])
    frames = "".join(shelf_frame(i, n, f) for i, f in enumerate(sh["frames"]))
    return (
        f'<section class="v2-shelf" aria-label="{escape(sh["aria_label"])}" data-astro-cid-yks6mgkh> '
        f'<h2 data-astro-cid-yks6mgkh>{escape(sh["heading"])}</h2> '
        f'<div class="v2-shelf__row" data-astro-cid-yks6mgkh>{frames}</div> </section>'
    )


def footer_section():
    """Footer copied structurally 1:1 from the source (clock, cat, fish)."""
    pet_bubble = bubble_spans(DATA["footer"]["pet_bubble"], with_semis=True)
    cat_svg = """<svg class="v2-pet__svg" viewBox="0 0 40 32" fill="none" aria-hidden="true"> <g class="cat-dreams" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" fill="none"> <g class="cat-z-1" stroke-width="1.5"> <path d="M34 1 L38 1 L34 5 L38 5"></path> </g> <g class="cat-z-2" stroke-width="1.3"> <path d="M37 -1.2 L40 -1.2 L37 1.8 L40 1.8"></path> </g> </g> <g class="cat-body"> <g class="cat-whiskers" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" fill="none"> <path d="M8.5 10.5 L2 8.6"></path> <path d="M8 12.8 L1.2 12.6"></path> <path d="M8.5 15 L2.2 16.8"></path> <path d="M25.5 10.5 L32 8.6"></path> <path d="M26 12.8 L32.8 12.6"></path> <path d="M25.5 15 L31.8 16.8"></path> </g> <path class="cat-tail" d="M26.8 26 C30.2 25 32 21 31.2 16.8" stroke="currentColor" stroke-width="2.7" stroke-linecap="round" fill="none"></path> <path fill="currentColor" d="M10.3 9 L8.6 2.8 L13.6 5 C15.6 4.3 18.4 4.3 20.4 5 L25.4 2.8 L23.7 9 C24.6 10.8 24.9 13 24.2 15 C26.3 17.2 27.4 20.4 27.3 23.6 C27.3 25.8 26 27.6 23.5 28.3 C19.5 29.3 14.5 29.3 11.5 28.2 C8.9 27 7.8 24 8.2 21 C8.5 18.5 9.3 16.4 10.6 14.9 C9.6 12.9 9.7 10.9 10.3 9 Z"></path> <g class="cat-eyes"> <circle class="cat-eye" cx="13.9" cy="11.6" r="2.1" fill="rgb(251, 250, 249)"></circle> <circle class="cat-eye" cx="20.1" cy="11.6" r="2.1" fill="rgb(251, 250, 249)"></circle> </g> </g> </svg>"""
    fish_svg = """<svg class="v2-feed__fish" viewBox="0 0 16 10" fill="none" aria-hidden="true"> <path d="M1.5 5 C4 1.5 8 1 11 3.2 L14.5 1 L13.5 5 L14.5 9 L11 6.8 C8 9 4 8.5 1.5 5 Z" fill="currentColor"></path> <circle cx="4.5" cy="4.2" r="0.7" fill="rgb(251, 250, 249)"></circle> </svg>"""
    return (
        f'<footer class="v2-footer" data-astro-cid-f5r2mlfl> '
        f'<span class="v2-footer__line" data-astro-cid-f5r2mlfl> '
        f'<span class="v2-clock slot-text" data-v2-clock data-astro-cid-f5r2mlfl>{char_slots("0:00am")}</span> '
        f'{escape(S["location_label"])}'
        f'<span class="v2-pet" data-v2-pet aria-hidden="true" data-astro-cid-fevfxcpg> '
        f'<span class="bubble v2-pet__bubble" data-v2-bubble="true" data-astro-cid-fevfxcpg="true" '
        f'data-astro-cid-erjq6yp3>{pet_bubble}</span> {cat_svg} </span>'
        f'<button type="button" class="v2-feed" data-v2-feed aria-label="Feed the cat" '
        f'data-hover-sound="tick" data-astro-cid-f5r2mlfl> {fish_svg} </button> </span> </footer>'
    )


def head_section():
    social = S["social"]
    jsonld = json.dumps(
        [
            {
                "@context": "https://schema.org",
                "@type": "Person",
                "name": S["author"],
                "jobTitle": S["job_title"],
                "url": S["url"],
                "email": S["email"],
                "description": S["description"],
                "sameAs": list(social.values()),
            },
            {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": f'{S["author"]} Portfolio',
                "url": S["url"],
                "description": S["description"],
            },
        ]
    )
    return f"""<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(S["title"])}</title><meta name="description" content="{escape(S["description"])}"><meta name="author" content="{escape(S["author"])}"><meta name="theme-color" content="#0E0E0E"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><meta name="keywords" content="{escape(S["keywords"])}"><link rel="canonical" href="{S["url"]}/"><link rel="me" href="{social["github"]}"><link rel="me" href="{social["linkedin"]}"><link rel="preload" href="/fonts/InterVariable.woff2" as="font" type="font/woff2" crossorigin><link rel="icon" type="image/png" href="{S["favicon"]}"><link rel="apple-touch-icon" href="{S["favicon"]}"><meta property="og:type" content="website"><meta property="og:title" content="{escape(S["title"])}"><meta property="og:description" content="{escape(S["description"])}"><meta property="og:url" content="{S["url"]}/"><meta property="og:image" content="{S["url"]}{S["og_image"]}"><meta property="og:site_name" content="{escape(S["author"])} Portfolio"><meta property="og:locale" content="{S["locale"]}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(S["title"])}"><meta name="twitter:description" content="{escape(S["description"])}"><meta name="twitter:image" content="{S["url"]}{S["og_image"]}"><script type="application/ld+json">{jsonld}</script><script>
         (function () {{
            document.documentElement.classList.add("no-transition");
            window.addEventListener("DOMContentLoaded", () => {{
               setTimeout(() => {{
                  document.documentElement.classList.remove("no-transition");
               }}, 100);
            }});
         }})();
      </script><link rel="stylesheet" href="/_astro/BasicLink.css"><link rel="stylesheet" href="/_astro/index.css"><script type="module" src="/_astro/page.js"></script>"""


def build_html():
    prose = "".join(prose_paragraph(p) for p in DATA["prose"])
    body = (
        f'<main class="v2" data-astro-cid-j7pv25f6> '
        f'<h3 data-astro-cid-j7pv25f6>{escape(S["author"])}</h3> '
        f'<p class="v2-updated" data-astro-cid-j7pv25f6>{escape(S["updated"])}</p> '
        f'<div class="v2-prose" data-astro-cid-j7pv25f6>{prose}</div> '
        f"{proof_section()}"
        f'<script type="module" src="/_astro/ProofStrip.js"></script>'
        f'{index_section(DATA["work"], "work")}'
        f'{index_section(DATA["learning"], "learning")}'
        f"{shelf_section()}"
        f"{footer_section()}"
        f'<script type="module" src="/_astro/SiteFooter.js"></script>'
        f'<script type="module" src="/_astro/index-page.js"></script>'
        f'<script type="module" src="/_astro/rowPreview.js"></script>'
        f"</main>"
    )
    return (
        f'<!DOCTYPE html><html lang="{S["lang"]}"> <head>{head_section()}</head> '
        f"<body> {body} </body></html>"
    )


# ------------------------------------------------------- row hover preview

PREVIEW_CSS = """
.row-preview{position:fixed;left:0;top:0;z-index:60;pointer-events:none;will-change:transform;transition:transform .38s cubic-bezier(.22,1,.36,1)}
.row-preview__card{display:block;width:min(280px,22vw);padding:7px 7px 7px;background:var(--white,#fff);border:1px solid var(--v2-hairline,#e4e2de);box-shadow:#00000029 0 18px 44px,#00000014 0 4px 12px;transform-origin:center center;opacity:0;transform:translateY(-50%) scale(.84) rotate(calc(var(--pt,4deg)*1.6));transition:opacity .16s ease,transform .42s cubic-bezier(.34,1.4,.64,1)}
.row-preview.is-visible .row-preview__card{opacity:1;transform:translateY(-50%) scale(1) rotate(var(--pt,4deg))}
.row-preview__card img{display:block;width:100%;height:auto;max-height:200px;object-fit:cover;background:#eceae7}
@media (hover:none),(prefers-reduced-motion:reduce),(max-width:1023px){.row-preview{display:none}}
"""

PREVIEW_JS = """// TinkerHub-style tilted preview flyer for .v2-row[data-preview]
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
    const cardW = Math.min(280, window.innerWidth * 0.22) + 16;
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
"""


# ---------------------------------------------------------------- assets

ASSET_MAP = {
    "BasicLink.DCZKXELH.css": "BasicLink.css",
    "index.5Q_DAhmd.css": "index.css",
    "hoverClick.B_FQABsh.js": "hoverClick.js",
    "index.DZjfvDz3.js": "slotText.js",
    "preload-helper.CVfkMyKi.js": "preload-helper.js",
    "Layout.astro_astro_type_script_index_0_lang.BrD-YCue.js": "layout.js",
    "page.DubX8lW0.js": "page.js",
    "ProofStrip.astro_astro_type_script_index_0_lang.DUyDG-23.js": "ProofStrip.js",
    "SiteFooter.astro_astro_type_script_index_0_lang.BIBZxi8H.js": "SiteFooter.js",
    "index.astro_astro_type_script_index_0_lang.Zg-lYZek.js": "index-page.js",
}


def rewrite_imports(code):
    for old, new in ASSET_MAP.items():
        code = code.replace(f"./{old}", f"./{new}")
    return code


def copy_assets():
    astro_out = OUT / "_astro"
    astro_out.mkdir(parents=True, exist_ok=True)
    for old, new in ASSET_MAP.items():
        code = (REF / "_astro" / old).read_text()
        code = rewrite_imports(code)

        if new == "SiteFooter.js":
            code = code.replace("Europe/London", S["timezone"])
            code = code.replace("Derby time.", f'{S["city_short"]} time.')
        if new == "ProofStrip.js":
            p = DATA["proof"]
            if p.get("live_stars_repo"):
                code = code.replace("Danilaa1/slot-text", p["live_stars_repo"])
            if p.get("live_npm_package"):
                code = code.replace("slot-text", p["live_npm_package"])

        if new == "index.css":
            code += PREVIEW_CSS
        (astro_out / new).write_text(code)
    (astro_out / "rowPreview.js").write_text(PREVIEW_JS)

    # layout.js is loaded by the built page as a module script
    fonts = OUT / "fonts"
    fonts.mkdir(exist_ok=True)
    shutil.copy(REF / "fonts" / "InterVariable.woff2", fonts / "InterVariable.woff2")

    images = OUT / "images"
    images.mkdir(exist_ok=True)
    # missing photos get neutral gray placeholders until real ones are supplied
    for fr in DATA["shelf"]["frames"]:
        name = Path(fr["img"]).name
        target = images / name
        if not target.exists():
            candidate = HERE.parent / "public" / name
            if candidate.exists():
                shutil.copy(candidate, target)
            else:
                from PIL import Image, ImageDraw
                img = Image.new("RGB", (fr["width"], fr["height"]), "#e3e0dc")
                ImageDraw.Draw(img).text(
                    (fr["width"] // 2 - 40, fr["height"] // 2 - 8), "photo soon", fill="#a8a49e"
                )
                img.save(target, quality=85)
    # row hover previews: gray placeholders with the project name until real shots land
    previews = images / "previews"
    previews.mkdir(exist_ok=True)
    for row in DATA["work"]["rows"] + DATA["learning"]["rows"]:
        if not row.get("preview"):
            continue
        target = OUT / row["preview"].lstrip("/")
        if not target.exists():
            candidate = HERE.parent / "public" / Path(row["preview"]).name
            if candidate.exists():
                shutil.copy(candidate, target)
            else:
                from PIL import Image, ImageDraw
                img = Image.new("RGB", (720, 470), "#e9e7e3")
                d = ImageDraw.Draw(img)
                label = row["meta"] if row["meta"] not in ("Open source", "Work", "Hackathon") else row["title"]
                d.text((28, 220), label, fill="#8f8b85")
                img.save(target, quality=85)

    logo = images / "website-logo.png"
    if not logo.exists():
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (256, 256), "#0E0E0E")
        ImageDraw.Draw(img).text((108, 112), "M", fill="#FBFAF9")
        img.save(logo)


def main():
    OUT.mkdir(exist_ok=True)
    copy_assets()
    html = build_html()
    # the layout module (lenis + sound bindings) must load on the page
    html = html.replace(
        '<script type="module" src="/_astro/page.js"></script>',
        '<script type="module" src="/_astro/page.js"></script>'
        '<script type="module" src="/_astro/layout.js"></script>',
    )
    (OUT / "index.html").write_text(html)
    print(f"built {OUT / 'index.html'} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
