---
name: neumorphism
description: Build website UI in the Neumorphism (soft UI) style - soft dual shadows and subtle highlights create raised and inset elements on a single monochrome surface. Use when the user asks for neumorphic, soft UI, soft shadow, "extruded" or calm monochrome dashboard/control-panel looks.
---

# Neumorphism (Soft UI)

Elements look extruded from, or pressed into, the same surface: same colour as the background, defined only by a light and a dark shadow.

## Core rules
- One background colour for page AND components. Light grey-blue is classic (`#e6ebf2`); dark variant `#23272f`.
- Two shadows per element: light highlight top-left, darker shadow bottom-right.
- Raised = default state, Inset = pressed/active/input fields.
- Use ONE accent colour (e.g. blue `#3b82f6`) only for active states, toggles, primary icons, so the UI stays readable.
- Generous radius (16–28px), generous spacing, simple line icons.

## Tokens
```css
:root {
  --bg: #e6ebf2; --text: #2d3748; --muted: #5b6678; --accent: #3b82f6;
  --light: #ffffff; --dark: #b8c1cf;
  --raised: 8px 8px 16px var(--dark), -8px -8px 16px var(--light);
  --raised-sm: 4px 4px 8px var(--dark), -4px -4px 8px var(--light);
  --inset: inset 6px 6px 12px var(--dark), inset -6px -6px 12px var(--light);
}
[data-theme="dark"] { --bg:#23272f; --text:#e5e7eb; --muted:#a3acb9; --light:#2d323c; --dark:#191c22; }
body { background: var(--bg); color: var(--text); }
```

## Recipes
```css
.card   { background: var(--bg); border-radius: 24px; box-shadow: var(--raised); padding: 24px; }
.btn    { background: var(--bg); border: 0; border-radius: 14px; box-shadow: var(--raised-sm); padding: 12px 20px; color: var(--text); }
.btn:active, .btn[aria-pressed="true"] { box-shadow: var(--inset); color: var(--accent); }
.input  { background: var(--bg); border: 0; border-radius: 12px; box-shadow: var(--inset); padding: 12px 16px; }
.toggle { width: 56px; height: 30px; border-radius: 99px; box-shadow: var(--inset); }
.toggle > span { width: 22px; height: 22px; border-radius: 50%; background: var(--accent); box-shadow: var(--raised-sm); }
```

## Avoid
- Low contrast: text must still be dark enough (≥ 4.5:1) and buttons need a visible label/icon, not just a shadow.
- Using it for everything: keep it to cards, controls, widgets. Long-form text sits on a flat area.
- Shadows on non-matching backgrounds (it only works when element colour = surface colour).
- Borders. The shadow IS the edge.

## Accessibility
Add a clear accent focus ring (`outline: 2px solid var(--accent)`); pressed states must also change colour or icon, not only shadow.
