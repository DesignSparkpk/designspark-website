---
name: bento-grid
description: Build website UI in the Bento Grid style - modular, rounded rectangular tiles of different sizes organising content in a clean, structured way, like a bento box. Use when the user asks for bento grid, bento layout, modular tiles, feature grids, dashboard overviews, or Apple/Linear-style feature showcases.
---

# Bento Grid

A tidy mosaic of rounded cards of varying sizes; each tile holds one idea, stat, chart or visual.

## Core rules
- CSS Grid with a fixed column count (4 or 6 desktop, 2 tablet, 1 mobile) and tiles spanning 1–3 columns/rows.
- One hero tile (largest) + medium tiles + small stat tiles. Hierarchy through size.
- Consistent gap (12–20px) and radius (16–28px) everywhere.
- Each tile: short title, one key message/number/visual. No long paragraphs.
- Light (`#f5f5f7` bg, white tiles) or dark (`#0a0a0a` bg, `#161616` tiles) theme; tiles may use soft tints (mint, lavender, peach) for categories.
- Subtle hover: lift 2px, border brightens.

## Tokens
```css
:root { --bg:#f5f5f7; --tile:#fff; --text:#111; --muted:#6b7280; --line:#e5e7eb;
        --mint:#d9f7e8; --lav:#e8e3ff; --peach:#ffe8d6; --sky:#dff1ff;
        --gap: 16px; --radius: 22px; }
```

## Recipes
```css
.bento {
  display: grid; gap: var(--gap);
  grid-template-columns: repeat(4, 1fr); grid-auto-rows: minmax(160px, auto);
  grid-auto-flow: dense;
}
.tile { background: var(--tile); border: 1px solid var(--line); border-radius: var(--radius);
        padding: 24px; display:flex; flex-direction:column; justify-content:space-between; overflow:hidden;
        transition: transform .2s, box-shadow .2s; }
.tile:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0,0,0,.06); }
.span-2 { grid-column: span 2; } .row-2 { grid-row: span 2; }
.hero   { grid-column: span 2; grid-row: span 2; }
.stat   { font-size: 2.5rem; font-weight: 700; letter-spacing: -.02em; }
@media (max-width: 900px) { .bento { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) { .bento { grid-template-columns: 1fr; } .span-2, .hero { grid-column: auto; } .row-2, .hero { grid-row: auto; } }
```

## Avoid
- Random tile sizes with no hierarchy, or uneven gaps.
- Overstuffed tiles; if it needs a paragraph, it's a section, not a tile.
- Holes in the grid — use `grid-auto-flow: dense` and check every breakpoint.

## Accessibility
Keep DOM order logical (reading order matches visual order on mobile). Tiles that are links: make the whole tile one `<a>` with a clear accessible name.
