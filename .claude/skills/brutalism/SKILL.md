---
name: brutalism
description: Build website UI in the (Neo-)Brutalism style - raw, high-contrast layouts, bold oversized typography, minimal styling, thick black borders and hard offset shadows. Use when the user asks for brutalist, neo-brutalism, bold/raw, editorial, "BIGGER BOLDER BRAVER", agency or anti-design looks.
---

# Brutalism / Neo-Brutalism

Honest, loud, raw. Visible structure, black outlines, hard (unblurred) shadows, huge type, flat colours.

## Core rules
- Thick solid borders: `2–4px solid #000`.
- Hard offset shadows with zero blur: `6px 6px 0 #000`.
- Huge, tight, uppercase or condensed headlines (Archivo Black, Anton, Space Grotesk, Inter 900), letter-spacing slightly negative.
- Monospace accents for labels/nav (Space Mono, JetBrains Mono).
- Palette: black, white + 1–2 loud flat colours (acid yellow `#ffe600`, hot pink, electric blue). No gradients.
- Grid is visible: split layouts, rules/lines between sections, asymmetric blocks.
- Interaction: on hover the shadow shrinks and element moves into it.

## Tokens
```css
:root {
  --ink: #000; --paper: #fff; --pop: #ffe600; --pop-2: #ff4fa3; --pop-3: #2f5bff;
  --border: 3px solid var(--ink); --shadow: 6px 6px 0 var(--ink);
}
body { background: var(--paper); color: var(--ink); font-family: "Space Grotesk", system-ui, sans-serif; }
h1 { font-family: "Archivo Black", sans-serif; font-size: clamp(3rem, 10vw, 8rem); line-height: .9; letter-spacing: -.03em; text-transform: uppercase; }
```

## Recipes
```css
.box { border: var(--border); box-shadow: var(--shadow); background: var(--paper); padding: 24px; border-radius: 0; }
.btn { border: var(--border); box-shadow: 4px 4px 0 var(--ink); background: var(--pop);
       font-weight: 800; text-transform: uppercase; padding: 12px 22px; transition: transform .1s, box-shadow .1s; }
.btn:hover  { transform: translate(2px,2px); box-shadow: 2px 2px 0 var(--ink); }
.btn:active { transform: translate(4px,4px); box-shadow: none; }
.tag   { font-family: "Space Mono", monospace; border: 2px solid var(--ink); padding: 2px 8px; }
.marquee { white-space: nowrap; overflow: hidden; border-block: var(--border); }
```

## Avoid
- Soft shadows, gradients, glass, rounded pill shapes (small radius 0–8px is ok in neo-brutalism).
- Chaos without a grid — raw does not mean broken; alignment must still be precise.
- Huge headlines that overflow on phones: always use `clamp()` and test at 360px wide.

## Accessibility
Naturally high contrast — keep it. Focus: `outline: 3px solid var(--pop-3); outline-offset: 3px`. Avoid auto-playing marquees without `prefers-reduced-motion` handling.
