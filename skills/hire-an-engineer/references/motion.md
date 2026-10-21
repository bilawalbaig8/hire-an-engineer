# Motion — animation that helps

Read when adding any animation or transition. Principles adapted from gsap-skills (MIT), designer-skills (MIT) and taste-skill (MIT), plus general practice; see THIRD_PARTY_NOTICES.

**Rule 0:** motion shows a change or gives feedback. If you can't say what it communicates, remove it.

## 1. Where it earns its place

Opening/closing panels, modals, menus and toasts · tab, step or page changes · toggles and icon swaps · one-off success/error feedback · skeleton → content. Not: every section fading in on load, decorative loops, motion that delays reading.

## 2. Timing

- Pick 2–3 base durations and reuse them everywhere: press/toggle 50–150 ms · fades, tooltips 150–250 ms · panels, modals 250–400 ms. Only rare choreography goes to ~700 ms; anything near 1 s feels broken.
- Close faster than open (~150 ms close vs 250–300 ms open).
- Stagger groups by 30–50 ms per item, whole sequence under ~700 ms, most important item first.
- Animations can be interrupted — a second click never waits for the first animation to end.

## 3. Easing and shape

- Entering: strong ease-out (e.g. `cubic-bezier(0.22, 1, 0.36, 1)`). Exiting: ease-in. Moving between positions: ease-in-out. Linear only for progress bars and endless loops.
- Entrances: fade plus a small move or scale from ~0.95. Dropdowns grow from the control that opened them.
- Every overlay has both an enter and an exit; hover transitions cover everything the hover changes.

## 4. Feedback timing

- Pressed state within 100 ms.
- Under ~400 ms: no spinner. Over ~400 ms: a loading state (skeleton matching the real layout, never a blank screen). Over ~3 s: real progress.
- Fade content in without layout jumps. After an error, give a beat (~0.5 s) before the next prompt.

## 5. Performance

- Animate only `transform` and `opacity` — never width, height, top, left or margin for movement.
- Name the properties (`transition: opacity 200ms`), never `transition: all`.
- `will-change` only on elements animating right now. In long lists animate only what's visible. Stop animations that are off-screen or no longer needed.
- Accepted exception — expand/collapse to natural height: animate `grid-template-rows` 0fr → 1fr with an inner wrapper (`min-height: 0; overflow: hidden`). It does cost layout work; keep it to small panels.

## 6. Scroll animation

Prefer a simple reveal-once as content enters, and keep content visible if scripts fail. Motion tied to scroll position: keep it light and recalculate positions only when layout really changes (after images/content load). Never block normal scrolling.

## 7. Reduced motion (required)

Honour `prefers-reduced-motion` in one central place: remove movement, keep fades instant or very short. CSS media queries follow setting changes automatically; JavaScript-driven motion must listen for the change. Information never depends on motion alone. A project that animates without this check has a defect.

## 8. Cleanup in components (React and similar)

Every animation, timer, scroll listener or observer created in a component is removed when it unmounts.

Libraries: plain CSS covers most UI motion. Use an animation library only for scroll-driven or timeline sequences the brief needs; choose by fit, licence and maintenance (`tools-and-stack.md`), not by default.
