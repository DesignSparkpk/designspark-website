---
name: claymorphism
description: Build website UI in the Claymorphism style - soft, puffy 3D shapes with gentle inner and outer shadows and bright playful colours, like modelling clay. Use when the user asks for claymorphism, clay UI, playful 3D, cute/friendly, kids, games, music or lifestyle app looks.
---

# Claymorphism

Chunky, inflated, toy-like elements: large radii, double inner shadows, bright pastel-to-saturated colours, often with 3D illustrations.

## Core rules
- Big radius everywhere (24–40px), pill buttons.
- Each clay element = coloured fill + outer soft drop shadow + inner light top-left + inner dark bottom-right.
- Bright, warm, friendly palette (orange, peach, sky, mint, lilac) on a light cream background.
- Rounded, bold typography: Nunito, Fredoka, Baloo 2, Poppins (700–800 headings).
- Pair with 3D clay-style illustrations/icons (blobs, characters, emoji-style objects).
- Light bouncy motion: scale 1.03 on hover, squash on press.

## Tokens
```css
:root {
  --bg: #fff4e8; --text: #3d2c1e;
  --orange: #ff9a3c; --peach: #ffc49b; --sky: #6ec6ff; --mint: #7ee0b5; --lilac: #b79cff;
  --clay: 0 18px 30px -10px rgba(120,60,20,.35),
          inset 6px 6px 12px rgba(255,255,255,.55),
          inset -8px -8px 16px rgba(0,0,0,.12);
}
body { background: var(--bg); color: var(--text); font-family: "Nunito", system-ui, sans-serif; }
```

## Recipes
```css
.clay      { border-radius: 32px; box-shadow: var(--clay); padding: 24px; }
.clay-orange { background: var(--orange); color: #fff; }
.clay-sky    { background: var(--sky); }
.btn-clay  { border: 0; border-radius: 999px; padding: 14px 28px; font-weight: 800;
             background: var(--orange); color: #fff; box-shadow: var(--clay);
             transition: transform .15s cubic-bezier(.34,1.56,.64,1); }
.btn-clay:hover  { transform: translateY(-2px) scale(1.03); }
.btn-clay:active { transform: scale(.96); }
@media (prefers-reduced-motion: reduce) { .btn-clay { transition: none; } }
```

## Avoid
- Sharp corners, thin fonts, or dark grimy colours — breaks the playful feel.
- White text on pale pastels (fails contrast). Use dark text on light clay, white on saturated clay.
- Clay effect on every single tiny element; keep small text and lists flat.

## Accessibility
Contrast ≥ 4.5:1 for text. Focus ring with a dark colour (`outline: 3px solid var(--text)`).
