---
name: minimalism
description: Build website UI in the Minimalism style - simplicity, clean typography, plenty of whitespace and very few elements. Use when the user asks for minimal, clean, simple, elegant, Apple-like, Scandinavian, "simple ideas, beautiful results", portfolio or premium product looks.
---

# Minimalism

Less but better. Content and typography carry the design; whitespace is the main tool.

## Core rules
- Whitespace first: section padding 96–160px desktop, 64px mobile. Max content width ~1100px, text ≤ 65ch.
- Neutral palette: off-white background, near-black text, one muted accent (or none). 2–3 colours total.
- Typography does the work: one family (Inter, Manrope, Satoshi, or a refined serif for headings), clear scale, light/regular weights for large type.
- One idea per section, one primary CTA per screen.
- Imagery: few, high quality, lots of space around (a single plant, product shot).
- Subtle details only: 1px hairlines, tiny radius, gentle fade-in.

## Tokens
```css
:root {
  --bg: #fafaf8; --text: #111; --muted: #6b6b6b; --line: #e7e5e0; --accent: #111;
  --space: clamp(64px, 10vw, 160px);
  --font: "Inter", system-ui, sans-serif;
}
body { background: var(--bg); color: var(--text); font: 400 1.0625rem/1.7 var(--font); }
h1 { font-weight: 500; font-size: clamp(2.5rem, 6vw, 4.5rem); line-height: 1.05; letter-spacing: -.03em; }
section { padding-block: var(--space); }
```

## Recipes
```css
.container { max-width: 1100px; margin-inline: auto; padding-inline: 24px; }
.btn { background: var(--text); color: var(--bg); border-radius: 999px; padding: 12px 26px; border: 0; }
.btn-link { color: var(--text); text-decoration: underline; text-underline-offset: 4px; }
.divider { border-top: 1px solid var(--line); }
.nav { display:flex; justify-content:space-between; padding-block: 28px; font-size: .9rem; }
```

## Avoid
- Empty = unfinished. Every element must be intentional and perfectly aligned.
- Too-light grey text (keep muted text ≥ 4.5:1).
- Decorative clutter: gradients, multiple shadows, icon overload, many fonts.

## Accessibility
Ensure links are recognisable without colour alone (underline). Visible focus ring: `outline: 2px solid var(--text); outline-offset: 4px`.
