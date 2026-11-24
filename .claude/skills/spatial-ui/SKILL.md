---
name: spatial-ui
description: Build website UI in the Spatial UI style - floating panels, layered depth and perspective that create a sense of 3D space and immersion (visionOS-like). Use when the user asks for spatial UI, 3D depth, floating windows, perspective cards, immersive, futuristic, AR/VR or visionOS-style looks.
---

# Spatial UI

Interfaces that feel placed in 3D space: floating translucent windows at different depths, perspective tilt, parallax and depth-of-field.

## Core rules
- Dark, atmospheric backdrop (deep navy/purple space or blurred environment photo).
- Panels float: translucent dark glass, large radius (24–32px), large soft shadows that suggest distance.
- Depth layers: background (blurred, dim) → mid panels → foreground focused panel (sharper, brighter, larger).
- Perspective: `perspective` on the container, slight `rotateY/rotateX` on side panels; pointer-driven tilt/parallax on desktop.
- Sidebar/tab bar as a floating vertical "ornament" detached from the window.
- Clean sans type (SF Pro-like: Inter), white text, soft accent (violet/blue).

## Tokens
```css
:root {
  --space-bg: radial-gradient(ellipse at 60% 30%, #3b2a7a 0, #120d2e 55%, #07051a 100%);
  --panel: rgba(30,26,60,.55); --panel-border: rgba(255,255,255,.14);
  --accent: #8b7cff; --text: #f5f3ff; --muted: rgba(245,243,255,.7);
  --float: 0 40px 80px -20px rgba(0,0,0,.6), 0 10px 25px rgba(0,0,0,.35);
}
body { background: var(--space-bg); color: var(--text); min-height: 100vh; }
```

## Recipes
```css
.stage { perspective: 1400px; transform-style: preserve-3d; }
.window {
  background: var(--panel); border: 1px solid var(--panel-border); border-radius: 28px;
  -webkit-backdrop-filter: blur(30px) saturate(150%); backdrop-filter: blur(30px) saturate(150%);
  box-shadow: var(--float); transition: transform .5s cubic-bezier(.2,.8,.2,1);
}
.window.left  { transform: translateZ(-120px) rotateY(18deg); opacity: .85; }
.window.right { transform: translateZ(-120px) rotateY(-18deg); opacity: .85; }
.window.focus { transform: translateZ(40px); }
.ornament { position: fixed; left: 24px; top: 50%; transform: translateY(-50%);
            display:flex; flex-direction:column; gap:12px; padding: 12px; border-radius: 999px;
            background: var(--panel); border: 1px solid var(--panel-border); }
@media (max-width: 768px) { .window.left, .window.right { transform: none; opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .window { transition: none; } }
```
Pointer tilt (desktop only):
```js
document.querySelectorAll('[data-tilt]').forEach(el => el.addEventListener('pointermove', e => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const r = el.getBoundingClientRect(), x = (e.clientX - r.left)/r.width - .5, y = (e.clientY - r.top)/r.height - .5;
  el.style.transform = `rotateY(${x*10}deg) rotateX(${-y*10}deg)`;
}));
```

## Avoid
- Heavy 3D on mobile: flatten into a normal stacked layout.
- Too many blurred panels at once (performance).
- Text on tilted panels that becomes hard to read — keep reading content on the front, un-tilted panel.

## Accessibility
Motion must be optional (reduced-motion). Contrast ≥ 4.5:1 on panels. Keyboard focus must bring the focused panel to the front.
