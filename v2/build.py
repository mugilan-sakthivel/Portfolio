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
MARK_RE = re.compile(r"==([^=]+)==")


def with_marks(escaped_text):
    return MARK_RE.sub(r'<mark class="v2-mark">\1</mark>', escaped_text)


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
    text = with_marks(text)
    return f"<p data-astro-cid-j7pv25f6>\n{text}\n</p>"


def journey_strip():
    """the path so far, as its own strip: Frontend → … → ==ML (now)=="""
    j = DATA["journey"]
    parts = []
    for i, st in enumerate(j["stages"]):
        if i:
            parts.append('<span class="v2-journey__arrow" aria-hidden="true" data-astro-cid-j7pv25f6>→</span>')
        cls = "v2-journey__stage v2-journey__stage--now" if st.get("now") else "v2-journey__stage"
        label = escape(st["label"])
        if st.get("now"):
            label = f'<mark class="v2-mark">{label}</mark><span class="v2-journey__now">now</span>'
        parts.append(f'<span class="{cls}" data-astro-cid-j7pv25f6>{label}</span>')
    return (
        f'<p class="v2-journey" aria-label="{escape(j["aria_label"])}" data-astro-cid-j7pv25f6>'
        f'{"".join(parts)}</p>'
    )


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
    desc = (
        f'<span class="v2-row__desc" data-astro-cid-xurrqhsc>{with_marks(escape(row["desc"]))}</span>'
        if row.get("desc") else ""
    )
    inner = (
        f' <span class="v2-row__year" data-astro-cid-xurrqhsc>{escape(row.get("year") or "")}</span> '
        f'<span class="v2-row__title" data-astro-cid-xurrqhsc> {escape(row["title"])}{tag}{desc}</span> '
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
            f'<q data-astro-cid-pfgrcgrj>{with_marks(escape(q["q"]))}</q> '
            f'<span class="v2-proof__who" data-astro-cid-pfgrcgrj>\n—  {who}, {escape(q["org"])} </span> </li>'
        )
    return (
        f'<aside class="v2-proof" aria-label="{escape(p["aria_label"])}" data-astro-cid-pfgrcgrj> '
        f'<p class="v2-proof__stats" data-astro-cid-pfgrcgrj> '
        f'<a class="v2-proof__lib" href="{p["label_href"]}" target="_blank" rel="noopener noreferrer" '
        f'data-hover-sound="tick" data-press-sound="press" data-astro-cid-pfgrcgrj>{escape(p["label"])}</a> '
        f'<span class="v2-proof__figures" data-astro-cid-pfgrcgrj>{stats}</span> </p> '
        + (f'<ul class="v2-proof__quotes" data-astro-cid-pfgrcgrj>{"".join(quotes)}</ul> ' if quotes else '')
        + '</aside>'
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
    cat_svg = """<svg class="v2-pet__svg" viewBox="0 0 40 32" fill="none" aria-hidden="true"> <g class="cat-dreams" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" fill="none"> <g class="cat-z-1" stroke-width="1.5"> <path d="M34 1 L38 1 L34 5 L38 5"></path> </g> <g class="cat-z-2" stroke-width="1.3"> <path d="M37 -1.2 L40 -1.2 L37 1.8 L40 1.8"></path> </g> </g> <g class="cat-body"> <g class="cat-whiskers" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" fill="none"> <path d="M7.5 12 L4.5 12"></path> <path d="M26.5 12 L29.5 12"></path> </g> <path class="cat-tail" d="M17 7.5 C17 5.8 17 4.6 17 3.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"></path> <circle cx="17" cy="2.6" r="1.5" fill="currentColor"></circle> <path fill="currentColor" d="M10.5 7 L23.5 7 C25.4 7 26.5 8.1 26.5 10 L26.5 16 C26.5 17.9 25.4 19 23.5 19 L22 19 L22 20.5 L23.8 20.5 C26 20.5 27.2 21.7 27.2 23.9 L27.2 25.6 C27.2 27.4 26 28.6 24.2 28.6 L9.8 28.6 C8 28.6 6.8 27.4 6.8 25.6 L6.8 23.9 C6.8 21.7 8 20.5 10.2 20.5 L12 20.5 L12 19 L10.5 19 C8.6 19 7.5 17.9 7.5 16 L7.5 10 C7.5 8.1 8.6 7 10.5 7 Z"></path> <g class="cat-eyes"> <circle class="cat-eye" cx="13.6" cy="12.6" r="2" fill="rgb(251, 250, 249)"></circle> <circle class="cat-eye" cx="20.4" cy="12.6" r="2" fill="rgb(251, 250, 249)"></circle> </g> <rect x="14.6" y="24" width="4.8" height="1.4" rx="0.7" fill="rgb(251, 250, 249)"></rect> </g> </svg>"""
    fish_svg = """<svg class="v2-feed__fish" viewBox="0 0 16 10" fill="none" aria-hidden="true"> <path d="M2 5 L9.2 0.8 L7.4 4 L14 5 L6.8 9.2 L8.6 6 Z" fill="currentColor"></path> </svg>"""
    return (
        f'<footer class="v2-footer" data-astro-cid-f5r2mlfl> '
        f'<span class="v2-footer__line" data-astro-cid-f5r2mlfl> '
        f'<span class="v2-clock slot-text" data-v2-clock data-astro-cid-f5r2mlfl>{char_slots("0:00am")}</span> '
        f'<span data-v2-loc>{escape(S["location_label"])}</span>'
        f'<span class="v2-pet" data-v2-pet aria-hidden="true" data-astro-cid-fevfxcpg> '
        f'<span class="bubble v2-pet__bubble" data-v2-bubble="true" data-astro-cid-fevfxcpg="true" '
        f'data-astro-cid-erjq6yp3>{pet_bubble}</span> {cat_svg} </span>'
        f'<button type="button" class="v2-feed" data-v2-feed aria-label="Charge the robot" '
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


def build_body():
    lead = "".join(prose_paragraph(p) for p in DATA["prose_lead"])
    stage1 = "".join(prose_paragraph(p) for p in DATA["prose_stage1"])
    stage2 = "".join(prose_paragraph(p) for p in DATA["prose_stage2"])
    tail = "".join(prose_paragraph(p) for p in DATA["prose_tail"])
    prose = (
        f"{lead}"
        f'<div class="v2-prose__more" data-v2-stage1 aria-hidden="true">{stage1}</div>'
        f'<div class="v2-prose__more" data-v2-stage2 aria-hidden="true">{stage2}</div>'
        f'<button type="button" class="basic-link v2-more-btn" data-v2-more-btn aria-expanded="false" '
        f'data-hover-sound="tick" data-press-sound="press" data-astro-cid-j7pv25f6>'
        f'<span data-v2-more-label>more</span> <span class="v2-more-btn__chev" aria-hidden="true">↓</span></button>'
        f"{journey_strip()}"
        f"{tail}"
    )
    body = (
        f'<main class="v2" data-astro-cid-j7pv25f6> '
        f'<h3 data-astro-cid-j7pv25f6>{escape(S["author"])}</h3> '
        f'<p class="v2-updated" data-astro-cid-j7pv25f6>{escape(S["updated"])}</p> '
        f'<div class="v2-prose" data-astro-cid-j7pv25f6>{prose}</div> '
        + ((proof_section() + '<script type="module" src="/_astro/ProofStrip.js"></script>') if DATA.get("proof") else "") +
        f'{index_section(DATA["projects"], "projects")}'
        f'{index_section(DATA["experience"], "experience")}'
        f"{shelf_section()}"
        f"{footer_section()}"
        f'<script type="module" src="/_astro/SiteFooter.js"></script>'
        f'<script type="module" src="/_astro/index-page.js"></script>'
        f'<script type="module" src="/_astro/locLive.js"></script>'
        f'<script type="module" src="/_astro/moreToggle.js"></script>'
        f'<!-- preview cards disabled for now: <script type="module" src="/_astro/rowPreview.js"></script> -->'
        f"</main>"
    )
    return body


def build_html():
    return (
        f'<!DOCTYPE html><html lang="{S["lang"]}"> <head>{head_section()}</head> '
        f"<body> {build_body()} </body></html>"
    )


# ------------------------------------------------------- row hover preview

PREVIEW_CSS = """
.v2-mark{background:linear-gradient(100deg,#ffe9a800 1%,#ffe9a8 3.5%,#ffe9a8d9 96%,#ffe9a800 99%);border-radius:.25em .05em;padding:0 .18em;margin:0 -.05em;color:inherit;box-decoration-break:clone;-webkit-box-decoration-break:clone}

.v2-row__desc{display:block;font-size:.85em;line-height:1.45;opacity:.58;font-weight:400;margin-top:2px;max-width:34em}

.row-preview{position:fixed;left:0;top:0;z-index:60;pointer-events:none;will-change:transform;transition:transform .38s cubic-bezier(.22,1,.36,1)}
.row-preview__card{display:block;width:min(280px,22vw);padding:7px 7px 7px;background:var(--white,#fff);border:1px solid var(--v2-hairline,#e4e2de);box-shadow:#00000029 0 18px 44px,#00000014 0 4px 12px;transform-origin:center center;opacity:0;transform:translateY(-50%) scale(.84) rotate(calc(var(--pt,4deg)*1.6));transition:opacity .16s ease,transform .42s cubic-bezier(.34,1.4,.64,1)}
.row-preview.is-visible .row-preview__card{opacity:1;transform:translateY(-50%) scale(1) rotate(var(--pt,4deg))}
.row-preview__card img,.row-preview__card video{display:block;width:100%;height:auto;max-height:200px;object-fit:cover;background:#eceae7}
@media (hover:none),(prefers-reduced-motion:reduce),(max-width:1023px){.row-preview{display:none}}

.v2-prose__more{overflow:hidden;max-height:0;opacity:0;transition:max-height .55s cubic-bezier(.22,1,.36,1),opacity .3s ease}
.v2-prose__more.is-open{max-height:60em;opacity:1;transition:max-height .55s cubic-bezier(.22,1,.36,1),opacity .45s ease .12s}
.v2-more-btn{display:inline-flex;align-items:baseline;gap:.35em;background:none;border:0;padding:0;margin:0;font:inherit;cursor:pointer;color:inherit;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:4px;text-decoration-color:color-mix(in srgb,currentColor 38%,transparent);transition:text-decoration-color .2s ease}
.v2-more-btn:hover{text-decoration-color:currentColor}
.v2-more-btn__chev{font-size:.85em;opacity:.6;transition:transform .3s ease}
.v2-more-btn[aria-expanded="true"] .v2-more-btn__chev{transform:rotate(180deg)}
.v2-prose[data-astro-cid-j7pv25f6] p.v2-journey{display:flex;flex-wrap:wrap;align-items:baseline;gap:.3em .55em;margin:38px 0 26px;font-size:.92em}
.v2-journey__stage{opacity:.6}
.v2-journey__stage--now{opacity:1;font-weight:560}
.v2-journey__stage--now .v2-journey__now{margin-left:.35em}
.v2-journey__now{font-size:.72em;font-weight:640;text-transform:uppercase;letter-spacing:.08em;opacity:.55}
.v2-journey__arrow{opacity:.3}
"""

MORE_JS = """// bio expander: collapsed -> stage1 -> stage2 -> stage1 -> collapsed
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
const vid = document.createElement("video");
vid.muted = true;
vid.loop = true;
vid.playsInline = true;
vid.preload = "metadata";
vid.style.display = "none";
card.appendChild(img);
card.appendChild(vid);
holder.appendChild(card);
document.body.appendChild(holder);

let hideTimer = 0;
const rows = [...document.querySelectorAll(".v2-row[data-preview]")];
rows.forEach((row, i) => {
  row.addEventListener("pointerenter", (e) => {
    if (e.pointerType !== "mouse" || !fine.matches || reduced.matches) return;
    if (window.innerWidth < 1024) return;
    const src = row.getAttribute("data-preview");
    const isVideo = /[.](mp4|webm)$/i.test(src);
    img.style.display = isVideo ? "none" : "block";
    vid.style.display = isVideo ? "block" : "none";
    if (isVideo) {
      if (vid.getAttribute("src") !== src) vid.src = src;
      vid.currentTime = 0;
      vid.play().catch(() => {});
    } else {
      vid.pause();
      if (img.getAttribute("src") !== src) img.src = src;
    }

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
    hideTimer = setTimeout(() => { holder.classList.remove("is-visible"); vid.pause(); }, 60);
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
            code = code.replace('timeZone:"Europe/London"', f'timeZone:(window.__LOC_TZ||"{S["timezone"]}")')
            import json as _json, re as _re
            idle = [
                "capturing this moment. for training data.",
                "I can see you smiling. noted.",
                "you've been here a while. impressive attention span.",
                "working on this footer 24/7. no PTO.",
                "he says 100-hour weeks. I do 168.",
                "beep boop? I would never say that.",
                "I saw you scroll past the projects. rude.",
                "this site passed my code review. barely.",
                "I'm not spying. I'm 'observing user behavior'.",
                "hire him so I can get a GPU upgrade.",
                "I dream in JSON.",
                "the clock is real. I wind it myself.",
                "53rd of 12,885. I did the math. twice.",
                "he talks to users. I talk to you.",
                "you hovered that link. I felt it.",
                "this bubble cost 0 tokens. efficient.",
                "I run on synthesized sounds and spite.",
                "the cat quit. I'm the upgrade.",
                "pixel-perfect or it doesn't ship.",
                "he A/B tested my personality. this is B.",
                "you're my favorite visitor today. low bar.",
                "1000+ commits at Kalvium. I counted every one.",
                "real engineers verify pixel by pixel.",
                "this footer is load-bearing.",
                "powered by 0.02 watts of pure ambition.",
                "my memory is three-tier. I never forget a visitor.",
                "I refuse to hallucinate. mostly.",
                "deployed on Cloud Run. emotionally on edge.",
                "he ships. I judge. the system works.",
                "screenshotting this? hold on, let me pose.",
                "I blink so you know I'm alive.",
                "scroll up. the good stuff is up there.",
                "insert coin. sorry — bolt.",
                "don't mind me. rendering feelings.",
                "everything here ships by hand. I checked.",
                "say hi. he actually replies.",
                "I own this footer. he pays hosting.",
                "he sleeps. I keep watch.",
                "agents built this site. I built character.",
                "my other job is being a status indicator.",
                "you scrolled all the way down. commitment.",
                "the polaroids are real. I verified the pixels.",
                "Salem → Bengaluru → your screen.",
                "latency is my love language.",
                "fun fact: I have exactly one fact.",
            ]
            boop = [
                "boop registered. filed under affection.",
                "careful. fresh circuits.",
                "recalibrating... nope, still adorable.",
                "I felt that in my capacitors.",
                "one boop = one bug fixed. promise.",
                "my antenna. my rules.",
                "ok that was nice. don't tell him.",
                "affection.exe is running.",
                "static electricity says hi back.",
                "warranty void. worth it.",
                "do that again and I purr. wait. wrong pet.",
                "noted. continue.",
                "I allow this. once.",
                "that's one volt you owe me.",
            ]
            asleep = [
                "asleep. Derby time.",
                "recharging. dreaming of electric sheep. confirmed.",
                "low power mode. like him at 4am.",
                "shh. compiling dreams.",
                "five more minutes. or hours.",
                "do not disturb. seriously.",
                "training run in progress. zzz.",
                "even robots need sleep mode.",
                "offline-ish. leave a message.",
                "zzz... committing to the dream branch.",
            ]
            fed = [
                "charge received. loyalty +1.",
                "crunchy. 240 volts of love.",
                "five stars. one bolt.",
                "battery at 101%. show-off.",
                "delicious. tastes like uptime.",
                "you may stay. forever.",
                "zap. thank you.",
                "bolt accepted. invoice cancelled.",
                "mmm. renewable.",
                "I was at 1%. you're a hero.",
                "fully charged. now what.",
                "powered by your generosity.",
            ]
            arrays = (
                "const f=" + _json.dumps(idle)
                + ",w=" + _json.dumps(boop)
                + ",v=" + _json.dumps(asleep)
                + ",b=" + _json.dumps(fed)
                + ",a="
            )
            code = _re.sub(r'const f=\[.*?\],w=\[.*?\],v=\[.*?\],b=\[.*?\],a=', lambda m: arrays, code, count=1)
            code = code.replace("Derby time.", f'{S["city_short"]} time.')
            # no-repeat picker: shuffled deck per array, refills when empty
            picker = "const __pick=(()=>{const d=new Map();return a=>{let q=d.get(a);if(!q||!q.length){q=[...a];for(let i=q.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[q[i],q[j]]=[q[j],q[i]]}d.set(a,q)}return q.pop()}})();"
            code = code.replace("const f=", picker + "const f=")
            code = _re.sub(r'([fwvb])\[Math\.floor\(Math\.random\(\)\*\1\.length\)\]', lambda m: "__pick(" + m.group(1) + ")", code)
            code = code.replace("I'm full. save it.", "battery full. save it for the blackout.")
            code = code.replace("asleep. leave it by the door.", "recharging. leave it by the dock.")
        if new == "ProofStrip.js":
            p = DATA.get("proof") or {}
            if p.get("live_stars_repo"):
                code = code.replace("Danilaa1/slot-text", p["live_stars_repo"])
            if p.get("live_npm_package"):
                code = code.replace("slot-text", p["live_npm_package"])

        if new == "index.css":
            code += PREVIEW_CSS
        (astro_out / new).write_text(code)
    (astro_out / "rowPreview.js").write_text(PREVIEW_JS)
    (astro_out / "moreToggle.js").write_text(MORE_JS)
    (astro_out / "locLive.js").write_text(
        'const u="' + S["location_source"] + '";\n'
        'fetch(u,{cache:"no-store"}).then(r=>r.ok?r.json():null).then(d=>{if(!d)return;'
        'if(d.tz)window.__LOC_TZ=d.tz;'
        'const el=document.querySelector("[data-v2-loc]");'
        'if(el&&d.city)el.textContent="in "+d.city;}).catch(()=>{});\n')

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
    for row in DATA["projects"]["rows"] + DATA["experience"]["rows"]:
        if not row.get("preview"):
            continue
        target = OUT / row["preview"].lstrip("/")
        if target.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
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


# ------------------------------------------- Next.js export (production site)
# The same body + assets, emitted as a React-consumable module so the Next app
# at the repo root serves v2 at "/". Scripts don't execute inside
# dangerouslySetInnerHTML, so they're stripped here and loaded by v2-site.tsx.

NEXT_SRC = HERE.parent / "src"
NEXT_PUBLIC = HERE.parent / "public"


def export_next():
    body = build_body()
    body = re.sub(r"<script[^>]*></script>", "", body)
    gen = (
        "// AUTO-GENERATED by v2/build.py — do not edit; edit v2/data.json and rebuild.\n"
        f"export const V2_BODY = {json.dumps(body)};\n"
        f"export const V2_TITLE = {json.dumps(S['title'])};\n"
        f"export const V2_DESCRIPTION = {json.dumps(S['description'])};\n"
    )
    (NEXT_SRC / "components" / "v2-body.generated.ts").write_text(gen)
    for d in ("_astro", "fonts", "images"):
        shutil.copytree(OUT / d, NEXT_PUBLIC / d, dirs_exist_ok=True)
    if (OUT / "resume.pdf").exists():
        shutil.copy(OUT / "resume.pdf", NEXT_PUBLIC / "resume.pdf")
    print(f"exported Next component data + assets -> src/components/v2-body.generated.ts, public/")


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
    import hashlib
    stamp = hashlib.md5(b"".join(sorted(
        f.read_bytes() for f in (OUT / "_astro").iterdir()
    ))).hexdigest()[:8]
    html = re.sub(r'(/_astro/[A-Za-z-]+\.(?:js|css))', r'\1?v=' + stamp, html)
    (OUT / "index.html").write_text(html)
    print(f"built {OUT / 'index.html'} ({len(html)} bytes)")
    export_next()


if __name__ == "__main__":
    main()
