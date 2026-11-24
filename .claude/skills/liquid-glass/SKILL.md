---
name: liquid-glass
description: Build website UI in the Liquid Glass style - glossy, translucent, fluid surfaces with bright reflections, refraction and specular highlights that look like liquid glass (next step beyond glassmorphism, Apple-2025-like). Use when the user asks for liquid glass, glossy glass, fluid/refraction effects, iOS-26-like or premium futuristic tech looks.
---

# Liquid Glass

Thicker, shinier, more "physical" glass than glassmorphism: strong edge highlights, inner glow, refraction-like distortion, fluid rounded shapes and vivid blue/cyan light.

## Core rules
- Background: deep vivid gradient (blue → cyan → violet) or a 3D glossy blob/orb image.
- Surfaces: low-opacity fill + blur + **bright rim highlight** (inner white border/shadow on top edge) + soft inner glow at the bottom.
- Highly rounded, pill and capsule shapes; controls feel like droplets.
- Specular highlights: a diagonal white gradient sheen across the top of each glass element.
- Optional refraction: SVG `feTurbulence` + `feDisplacementMap` filter on the backdrop for a liquid wobble (desktop only).
- Smooth, springy motion (scale/morph on hover).

## Tokens
```css
:root {
  --bg-a: #0b3bff; --bg-b: #00c2ff; --bg-c: #7a3cff;
  --lg-fill: rgba(255,255,255,.12);
  --lg-rim: inset 0 1px 1px rgba(255,255,255,.9), inset 0 -1px 1px rgba(255,255,255,.25);
  --lg-glow: inset 0 -10px 30px rgba(120,200,255,.25), 0 20px 50px rgba(0,20,80,.35);
  --lg-blur: blur(24px) saturate(180%) brightness(1.1);
}
body { color: #fff; background: radial-gradient(circle at 70% 40%, var(--bg-b), transparent 50%),
                                 radial-gradient(circle at 20% 80%, var(--bg-c), transparent 50%), var(--bg-a); }
```

## Recipes
```css
.liquid {
  position: relative; border-radius: 28px; background: var(--lg-fill);
  -webkit-backdrop-filter: var(--lg-blur); backdrop-filter: var(--lg-blur);
  box-shadow: var(--lg-rim), var(--lg-glow); border: 1px solid rgba(255,255,255,.25);
}
.liquid::after { /* specular sheen */
  content:""; position:absolute; inset:0; border-radius:inherit; pointer-events:none;
  background: linear-gradient(160deg, rgba(255,255,255,.55) 0%, rgba(255,255,255,.08) 28%, transparent 55%);
  mix-blend-mode: screen;
}
.pill { border-radius: 999px; padding: 12px 26px; }
.liquid:hover { transform: scale(1.02); transition: transform .4s cubic-bezier(.2,.9,.3,1.3); }
@supports not (backdrop-filter: blur(1px)) { .liquid { background: rgba(10,40,140,.85); } }
@media (prefers-reduced-motion: reduce) { .liquid:hover { transform: none; } }
```
Refraction (optional, use sparingly):
```html
<svg width="0" height="0"><filter id="liquid"><feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="18"/></filter></svg>
```
Apply `filter:url(#liquid)` to a decorative background layer, never to text.

## Avoid
- Distortion on text or many elements (blurry, slow).
- White text on very light glass — add a darker tint behind text.
- Using it without a rich backdrop; it will look flat.

## Accessibility
Same as glassmorphism: test contrast on brightest backdrop area, provide fallbacks, visible focus ring (`outline: 2px solid #fff`).
