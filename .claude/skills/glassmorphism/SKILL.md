---
name: glassmorphism
description: Build website UI in the Glassmorphism style - translucent frosted-glass panels with background blur and subtle gradients over a colourful backdrop, creating a layered modern feel. Use when the user asks for glassmorphism, frosted glass, blurred translucent cards, or a modern layered travel/weather/fintech look.
---

# Glassmorphism

Frosted-glass panels floating over a vivid background (photo, gradient or blurred colour blobs).

## Core rules
- The background makes it work: use a colourful photo or gradient mesh. Glass over a flat white page looks like nothing.
- Panels: semi-transparent white (10–25% opacity), `backdrop-filter: blur()`, 1px light border, soft shadow.
- Layering: 2–3 depth levels max (background → main glass card → small chips/widgets).
- Text is white or very dark depending on backdrop; add a subtle text-shadow or darker overlay where needed.
- Clean sans-serif (Inter, Poppins, SF-like), medium weights.

## Tokens
```css
:root {
  --glass: rgba(255,255,255,.16); --glass-strong: rgba(255,255,255,.28);
  --glass-border: rgba(255,255,255,.35); --text: #fff; --text-muted: rgba(255,255,255,.78);
  --blur: blur(18px) saturate(160%);
  --shadow: 0 8px 32px rgba(15,23,42,.25);
}
body {
  min-height: 100vh; color: var(--text);
  background: radial-gradient(circle at 15% 20%, #7c3aed 0, transparent 45%),
              radial-gradient(circle at 85% 30%, #ec4899 0, transparent 40%),
              radial-gradient(circle at 50% 90%, #06b6d4 0, transparent 45%), #1e1b4b;
}
```

## Recipes
```css
.glass {
  background: var(--glass);
  -webkit-backdrop-filter: var(--blur); backdrop-filter: var(--blur);
  border: 1px solid var(--glass-border); border-radius: 20px; box-shadow: var(--shadow);
}
.glass::before { /* top sheen */
  content:""; position:absolute; inset:0; border-radius:inherit; pointer-events:none;
  background: linear-gradient(135deg, rgba(255,255,255,.35), transparent 40%);
}
.btn-glass { background: var(--glass-strong); border: 1px solid var(--glass-border); border-radius: 999px; padding: 10px 22px; color: #fff; }
@supports not (backdrop-filter: blur(1px)) { .glass { background: rgba(30,27,75,.85); } }
```
(`.glass` needs `position: relative` for the sheen.)

## Avoid
- Too many blurred layers (performance on phones). Keep backdrop-filter elements few.
- Unreadable text over busy photos: add a dark overlay to the photo or increase panel opacity.
- Opacity on the whole element (`opacity:.5`) — that fades the text too. Use rgba backgrounds.

## Accessibility
Check contrast against the *worst* part of the background. Provide the `@supports` fallback. Visible focus: `outline: 2px solid #fff; outline-offset: 3px`.
