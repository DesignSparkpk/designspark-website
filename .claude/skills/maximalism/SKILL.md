---
name: maximalism
description: Build website UI in the Maximalism style - bold clashing colours, patterns, layered elements, stickers, collage and abundant visuals for a rich, expressive experience. Use when the user asks for maximalist, loud, creative, Gen-Z, collage, pop-art, "BIGGER DREAMS BOLDER IDEAS", festival, fashion or creative-agency looks.
---

# Maximalism

More is more — but organised. Vivid colours, patterns, overlapping layers, collage imagery, stickers, mixed type.

## Core rules
- Saturated clashing palette: purple, hot pink, electric yellow, orange, cyan. Use 4–6 colours confidently.
- Patterns: checkerboards, halftone dots, stripes, squiggles (CSS gradients or SVG).
- Layering: images cut out and overlapping text, rotated stickers/badges, elements breaking the grid.
- Type mixing: a massive display face (Bricolage Grotesque, Syne, Rubik Mono One) + outline text + a handwritten/script accent.
- Motion: marquees, rotating badges, hover wiggles (respect reduced-motion).
- Still keep ONE clear reading path and ONE clear CTA per section.

## Tokens
```css
:root {
  --purple: #6d28d9; --pink: #ff2e93; --yellow: #ffe14d; --orange: #ff7a1a; --cyan: #22d3ee; --ink: #12002b;
  --checker: conic-gradient(#000 25%, #fff 0 50%, #000 0 75%, #fff 0) 0 0 / 24px 24px;
  --dots: radial-gradient(#ffffff55 1.5px, transparent 1.6px) 0 0 / 14px 14px;
}
body { background: var(--purple); color: #fff; }
```

## Recipes
```css
.hero { background: var(--dots), linear-gradient(120deg, var(--purple), var(--pink)); position: relative; overflow: hidden; }
.mega { font-family: "Rubik Mono One", sans-serif; font-size: clamp(3rem, 11vw, 9rem); line-height: .85; color: var(--yellow);
        text-shadow: 4px 4px 0 var(--ink); }
.outline { color: transparent; -webkit-text-stroke: 2px #fff; }
.sticker { position:absolute; background: var(--yellow); color: var(--ink); border: 3px solid var(--ink);
           border-radius: 999px; padding: 8px 16px; font-weight: 900; transform: rotate(-8deg); }
.checker { background: var(--checker); }
.badge-spin { animation: spin 12s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .badge-spin { animation: none; } }
```

## Avoid
- Noise without hierarchy: the headline and CTA must still win.
- Text on patterns without a solid backing block.
- Huge unoptimised images; compress, use WebP/AVIF, lazy-load.
- Overlaps that cover content on mobile — re-stack layers at small widths.

## Accessibility
Check contrast for every colour pair actually used for text. Never convey meaning by colour alone. Give decorative images `alt=""`.
