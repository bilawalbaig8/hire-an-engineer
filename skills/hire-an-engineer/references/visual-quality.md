# Visual Quality — beyond the generic AI look

Read when building or reviewing anything customers will look at: landing pages, customer-facing apps, branded screens. For internal tools, use only §6 (critique) and §7 (polish); familiar patterns beat novelty there. Ideas adapted from taste-skill (MIT) and impeccable (Apache-2.0); see THIRD_PARTY_NOTICES.

**The brief wins.** Every value and ban in this file is a default. The person's named style, font, colour or era, their brand guide, an existing design system or the component library already in use always win. Refining keeps the existing look; a redesign replaces it — never half-way.

## 1. How bold to be — pick the mode by the surface

| Mode | Surface | Approach |
|---|---|---|
| Persuade | Landing page, launch page | Commit to one memorable idea |
| Operate | App, dashboard, admin | Familiar patterns, scanability, calm |
| Read | Docs, guides, help | Structure and typography first |
| Show | Portfolio, gallery | The work leads; the frame stays quiet |

## 2. Idea and claims before layout (Persuade / Show)

- **One sentence:** "Here, [something true about this subject] becomes [the layout idea]." A furniture maker's page might be built around close-ups of the wood and the build stages.
- **Competitor swap:** put a competitor's name on the page. If it still works, the page has no idea yet.
- **Five answers before any layout:** who reads it · what it is in plain words · the one thing to believe after one screen · the proof · the next action.
- **Page = claims:** each section makes one claim and shows one proof. A section with no claim is cut. This also breaks the stock order (hero → logos → features → testimonial → pricing).
- **Never invent proof:** no made-up logos, quotes, ratings or "10,000+ customers". Real proof or none.

## 3. Generic tells — avoid unless the brief asks

- Violet/indigo gradients, gradient headline text, glow buttons, glass/blur panels, floating pill navigation
- Soft grey shadow under every card; a row of three identical icon cards; emoji used as icons
- Small uppercase label or "New" pill above every headline; one coloured accent word in the headline; arrow on every button
- Fake dashboards drawn from grey bars; pulsing "live" dots; cream background with terracotta accent
- 01/02/03 section numbers, monospace "technical" captions, hairline rules everywhere
- Headline shapes like "X, reimagined", "Not just X — it's Y", "Fast. Simple. Secure."; buttons saying "Get started" / "Learn more"; words like seamless, unlock, supercharge

Removing tells isn't enough — a page with only the tells removed is empty. Fill the space with the idea, real content and real pictures. A richer page with a few familiar devices beats a thin, "clean" one.

## 4. Concrete values

- **Type:** at most 5 sizes, clearly apart; on desktop landing pages display ≥ 4× body, scaled down on phones; body ≥ 16px; line length 45–75 characters. One typeface, two at most. Big type needn't be bold. Latin display type: tracking −0.02 to −0.04em, line height ~1.0–1.1; body ~1.5. **Urdu/Arabic script:** no letter-spacing (it breaks joined letters) and generous line height (~1.6+ body, ~1.3 display).
- **Headlines:** ≤ 2 lines on phone and desktop; balanced wrapping; cut words rather than shrinking the font.
- **Colour tokens:** the role list in `ui-ux.md` §4, used through tokens, never raw values in components. Background 70–90% of the screen; the action colour under ~5%, kept for the main action. Text on a coloured surface is tinted from that hue, not grey.
- **Depth:** panels one tone step from the background instead of heavy shadows; never a panel inside a panel; declare depth once (border or shadow, not both); real shadows have offset and blur.
- **Space:** more space above a heading than below; gaps between sections larger than gaps inside them; equal side margins; no accidental empty band taller than half a screen.
- **Details:** card radius ~12–16px, pills only for small controls; one icon set, one stroke weight; style the focus ring; placeholder text also meets 4.5:1 contrast.

## 5. Design record

Keep the visual plan where every session and AI tool will find it — Small: the design section of `docs/project.md`; Medium+: `docs/design/ux-ui.md`; Tiny: a few lines in README. Record: mode and idea, colour tokens, typography, layout, depth, shapes, key components, do/don't. Fill it from the code's tokens first; ask the person only for the feel ("warm and homely", "sharp and serious").

## 6. Self-critique on screenshots

Judge screenshots, not your code. Capture at ~1440, 768 and 390 px wide, with scroll-reveal animations turned off (emulate reduced motion) so every section is visible. No browser available: careful code read, and say so.
- **1 s, then 5 s glance as a stranger:** what is it, who is it for, what do I do next?
- **Squint:** the screen reduces to 2–3 big masses.
- **Repeats and holes:** name each section's layout in one word — flag repeats; flag empty bands and anything sitting on text or running off the phone screen.
- **Phone view** is its own composition, not a squeezed desktop.
- **Cognitive load on task screens:** one focus; few visible choices (~4) for the main decision; one decision at a time; nothing to remember from the previous screen. Admin screens and tables may show more — group them.
- **Severity** (same scale as `ui-ux.md` §8): 4 blocks the task · 3 major (a user would ask for help) · 2 minor · 1 polish. Fix 4 and 3 before showing; then the weakest area first, and stop when changes stop helping.

## 7. Polish pass before showing

1. Order: broken paths → missing states → hierarchy and consistency drift → visuals and motion → cleanup.
2. Classify each inconsistency: missing token · one-off that should reuse a shared component · flow mismatch · local bug. Fix at the narrowest correct level.
3. Final walk with mouse, keyboard and touch; check for console errors and layout jumps.
4. Polish never smuggles in a redesign. If the idea is wrong, say so and propose one.
