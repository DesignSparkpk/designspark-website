---
name: skeuomorphism
description: Build website UI in the Skeuomorphism style - realistic textures, materials (wood, leather, brushed metal, paper) and physical details that mimic real-world objects. Use when the user asks for skeuomorphic, realistic, retro-physical, vintage-device, "real object" or heritage/luxury-crafted looks.
---

# Skeuomorphism

Interfaces that imitate physical objects: knobs, stitched leather, wood panels, engraved metal plates, paper cards.

## Core rules
- Every surface is a *material*. Pick 1 base material (e.g. dark walnut) + 1 accent material (brass/gold) + paper/cream for reading areas.
- Light comes from the top-left. Highlights on top edges, shadows below/right, consistently.
- Controls look pressable: raised bevels at rest, inset when active.
- Typography: a serif or script display face for headings (Playfair Display, Cormorant, "Heritage" style), clean serif/sans for body text. Engraved/embossed headings via text-shadow.
- Keep reading text on flat, high-contrast paper/cream surfaces. Texture never sits under body copy.

## Tokens
```css
:root {
  --wood-dark: #3b2416; --wood: #5a3721; --wood-light: #7a4b2c;
  --brass: #c9a24a; --brass-light: #f1d27a; --brass-dark: #8a6a24;
  --paper: #f4ead5; --ink: #2a1a10;
  --bevel: inset 0 1px 0 rgba(255,255,255,.25), inset 0 -2px 0 rgba(0,0,0,.35);
  --drop: 0 6px 14px rgba(0,0,0,.45), 0 2px 3px rgba(0,0,0,.4);
}
```

## Recipes
```css
.panel {               /* wood panel */
  background:
    repeating-linear-gradient(92deg, rgba(0,0,0,.06) 0 2px, transparent 2px 9px),
    linear-gradient(180deg, var(--wood-light), var(--wood) 40%, var(--wood-dark));
  border-radius: 14px; box-shadow: var(--bevel), var(--drop);
  border: 1px solid #22140b;
}
.btn-brass {
  background: linear-gradient(180deg, var(--brass-light), var(--brass) 50%, var(--brass-dark));
  color: #3a2808; text-shadow: 0 1px 0 rgba(255,255,255,.5);
  border: 1px solid var(--brass-dark); border-radius: 8px;
  box-shadow: var(--bevel), 0 3px 6px rgba(0,0,0,.4);
}
.btn-brass:active { box-shadow: inset 0 3px 6px rgba(0,0,0,.45); transform: translateY(1px); }
.stitched { outline: 2px dashed rgba(241,210,122,.5); outline-offset: -8px; }
.engraved { color: #2a1a10; text-shadow: 0 1px 0 rgba(255,255,255,.35); }
.knob { border-radius: 50%; background: radial-gradient(circle at 35% 30%, #fff8 0, var(--brass) 35%, var(--brass-dark) 100%); box-shadow: var(--drop); }
```
- Real texture images (wood/leather/noise) may be used as `background-image` at low size (<100 KB, tiled), always with a gradient fallback.

## Avoid
- Mixing too many materials. Max 3.
- Inconsistent light direction.
- Texture behind paragraphs; low-contrast engraved body text.
- Heavy images that slow the page: prefer CSS gradients.

## Accessibility
Body text contrast ≥ 4.5:1. Focus ring: `outline: 3px solid var(--brass-light); outline-offset: 3px;`. Respect `prefers-reduced-motion` for knob/needle animations.
