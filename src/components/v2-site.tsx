"use client";

import { useEffect } from "react";
import { V2_BODY } from "./v2-body.generated";

// The v2 page's behaviors (lenis scroll, hover sounds, slot-text clock, cat
// footer, proof strip, bio expander) live in vanilla ES modules under
// /_astro. They query the DOM at eval time, so they're appended after the
// markup has mounted. Script tags inside dangerouslySetInnerHTML never
// execute — this effect is the loader.
const V2_SCRIPTS = [
  "page.js",
  "layout.js",
  "ProofStrip.js",
  "SiteFooter.js",
  "index-page.js",
  "locLive.js",
  "moreToggle.js",
];

export default function V2Site() {
  useEffect(() => {
    document.documentElement.classList.add("no-transition");
    const t = setTimeout(
      () => document.documentElement.classList.remove("no-transition"),
      100
    );
    const loaded: HTMLScriptElement[] = [];
    for (const name of V2_SCRIPTS) {
      if (document.querySelector(`script[src="/_astro/${name}"]`)) continue;
      const s = document.createElement("script");
      s.type = "module";
      s.src = `/_astro/${name}`;
      document.body.appendChild(s);
      loaded.push(s);
    }
    return () => {
      clearTimeout(t);
      loaded.forEach((s) => s.remove());
    };
  }, []);

  return (
    <>
      {/* eslint-disable-next-line @next/next/no-css-tags */}
      <link rel="stylesheet" href="/_astro/BasicLink.css" />
      {/* eslint-disable-next-line @next/next/no-css-tags */}
      <link rel="stylesheet" href="/_astro/index.css" />
      <link
        rel="preload"
        href="/fonts/InterVariable.woff2"
        as="font"
        type="font/woff2"
        crossOrigin="anonymous"
      />
      <div dangerouslySetInnerHTML={{ __html: V2_BODY }} />
    </>
  );
}
