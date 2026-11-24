# Beacon website: professional audit and competitor comparison

Audited 24 Nov 2026. Tools: Google Lighthouse 12 (mobile + desktop), axe-core (WCAG 2.1 AA + best practices, English and Urdu), html-validate, Playwright functional tests on desktop (1366px) and mobile (390px).

## Scores
| | Beacon (ours) | PPSC (ppsc.edu.pk) | PEACE (thepeace.edu.pk) | Superior Haripur |
|---|---|---|---|---|
| Lighthouse Performance (mobile) | **99** | n/a* | 58 | 31 |
| Lighthouse Accessibility | **100** | n/a* | 87 | 93 |
| Lighthouse Best Practices | **100** | n/a* | 89 | 79 |
| Lighthouse SEO | **100** | n/a* | 82 | 100 |
| Largest content shown (mobile) | **1.4 s** | ~2.5 s load (manual) | 12.0 s | 11.3 s |
| Page weight | **138 KB** (mobile) | ~92 KB + images | 4,432 KB | 3,434 KB |
| Desktop Lighthouse | **100 / 100 / 100 / 100** | n/a* | | |
| axe accessibility violations | **0** (EN and Urdu, desktop and mobile) | | | |
| HTML validation errors | **0** | | | |

\* PPSC's server blocks automated audit tools (HTTP 403), so it could not be scored the same way.

## Feature comparison
| Feature | Beacon | PPSC | PEACE | Superior |
|---|---|---|---|---|
| English + Urdu (RTL, Nastaliq font) | ✅ | ❌ | ❌ | ❌ |
| WhatsApp admission form (pre-filled message) | ✅ | ❌ | ❌ | ❌ |
| Fee section | ✅ (sample until confirmed) | ❌ | ❌ | ❌ |
| Transport routes | ✅ (sample until confirmed) | ❌ | ❌ | ❌ |
| Admission process + documents | ✅ | partly (FAQ) | ❌ | ❌ |
| Campus finder with maps | ✅ 3 campuses | ✅ | ✅ | ❌ |
| Notice board with readable text | ✅ | ✅ notices page | ❌ poster image only | ❌ |
| Results / achievers | ✅ (sample until confirmed) | ✅ | ✅ in poster | ❌ |
| FAQ | ✅ | ✅ | ❌ | ❌ |
| Google structured data (School schema) | ✅ | ? | ? | ? |
| Floating WhatsApp button | ✅ | top bar link | ✅ | ❌ |
| Parent portal / LMS | ❌ (future add-on) | ✅ | ❌ | ❌ |
| Real photo gallery | ❌ (needs photos) | ✅ | ✅ | ✅ |
| Principal message / About | ❌ (needs content) | ✅ | ✅ | ✅ |

## Checks passed
- No horizontal scrolling on desktop or mobile, English or Urdu
- All internal links point to existing sections; no broken images; every image has alt text
- Admission form: blocks empty submit with a message; sends a complete WhatsApp message to +92 300 5148824
- Mobile menu opens and closes; language choice is remembered
- Colour contrast passes WCAG AA everywhere
- Respects "reduce motion" setting; visible keyboard focus; skip-to-content link

## Fixed during this audit
- Logo rebuilt from Adobe vector trace: sharp at every size, transparent background
- Contrast: WhatsApp buttons and section labels darkened to pass WCAG AA
- Accessible names of language button and logo link matched to visible text
- Responsive images (smaller files on phones) and high priority for the hero logo
- Title shortened for Google (under 60 characters); input types; phone numbers no longer break across lines
- All inline styles moved into the stylesheet
- Added School structured data for Google, Admission process section, landmark regions

## Still needed from the school (before going live)
1. Fees per class, transport routes, results and toppers (currently marked "Sample")
2. Session year (site says 2027-28, assumed)
3. Real campus photos for a gallery; principal's message / short history
4. Confirm documents list and admission test details
5. Instagram link, office timings, separate campus phone numbers if any
6. Domain name and hosting (Netlify / Cloudflare give free compression and caching, which the remaining Lighthouse hints refer to)
7. Remove the "Concept design by DesignSpark" ribbon once approved
