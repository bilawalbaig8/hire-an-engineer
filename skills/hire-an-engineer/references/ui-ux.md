# UI / UX Design

Contents: The UX process · Users and journeys · Screens and wireframes · Visual design · Every state of every screen · Words on the screen (UX copy) · Accessibility and devices · Design review (self-critique) · Quick usability test with real users · Design tokens and handoff spec · Tools for design work

The UX Designer role, end to end. Drawn and simplified from the frontend-design, ux-copy, accessibility-review, design-critique, user-research, design-system and design-handoff skills for this use case.

The person can't judge design from words or specs. They judge by **seeing** and **trying**. So: show early, show options, let them click, then refine.

---

## 1. The UX process

| Workflow phase | UX work | Person sees |
|---|---|---|
| 1 Discovery | Who uses it, where, on what device, what they do today | Questions about real moments |
| 2 Brief | Core user journeys | "Customer link kholega → order dega → aap ko message aayega" |
| 4 Design | Screen list, wireframes, visual direction, states, copy | Clickable mockup or 2 visual options |
| 6 Build | Build to the design system; all states | Working screens |
| 7 Verify | Design review, accessibility check, quick usability test | "3 logon ne try kiya, sab ne order de diya" |
| 9 Handoff | Screenshots for User Guide; handoff spec for future developers | User Guide with pictures |

Skip or shrink steps for tiny tools — a single calculator still deserves good states, copy and mobile layout, but not a usability study.

## 2. Users and journeys

- **Who:** each type of user (owner, staff, customer), their device, their comfort with tech, language, where they'll be (shop counter, on the move, at a desk).
- **Journeys:** for each user type, the 1–3 most important tasks, step by step, from their trigger to done. Draw the main one as a flowchart.
- **Count the steps.** Every extra tap or field loses people. Remove anything not needed for the task.

## 3. Screens and wireframes

1. **Screen inventory:** list every screen and what it's for, mapped to journeys. Fewer screens is better.
2. **Wireframes first:** quick ASCII or simple boxes showing layout and content order — no colours yet. Get the structure right before the looks.
3. **Then a clickable mockup:** an HTML preview (or design tool) the person can open and tap through. This catches more misunderstandings than any document.
4. Ask with concrete choices: "Order list upar ho ya calendar view?" — and show both when it matters.

Layout principles:
- The most important action on each screen is the most visible thing.
- One clear primary button per screen.
- Group related things; keep a clear top-to-bottom reading order.
- Mobile first if users are on phones: big tap targets, one column, key action reachable by thumb.

## 4. Visual design

Ground the look in the subject — a kids' learning app, a bakery, and a finance dashboard should look nothing alike. Before building UI, write a compact visual plan:

- **Colour:** 4–6 named colours (background, text, primary action, accent, success/error). Use brand colours if the person has them (ask for a logo).
- **Type:** one or two typefaces with clear roles; readable sizes (body ≥ 16px on mobile); line length under ~80 characters.
- **Layout concept:** a sentence plus an ASCII sketch; alignment rules.
- **One memorable thing:** spend boldness in one place, keep the rest calm. Remove one unnecessary decoration before shipping.

Avoid generic AI-template looks that ignore the subject (identical rounded cards everywhere with soft grey shadows, decorative gradients, all-caps labels above every heading, arrow "→" on every button, a single accent word in the headline). Use them only if the brief calls for it.

Motion only when it shows what changed (item added, panel opened). No decorative animations on every section.

For anything branded or public (website, customer-facing app), offer the person 2 visual directions to choose from. For internal tools, one clean, consistent direction is enough.

## 5. Every state of every screen

Design and build all of these — missing states are where non-technical owners get stuck:

| State | Needs |
|---|---|
| Default | Normal content |
| Empty | What this is + why it's empty + how to start ("Abhi koi order nahi. Pehla order aate hi yahan dikhega.") |
| Loading | Something is happening; set expectations if slow |
| Success | Confirm what happened, in the action's own word ("Order saved") |
| Error | What happened + why + how to fix; keep what the user typed |
| Disabled | Why it can't be used right now |
| Too much / too little | Very long names, 1000 rows, missing photo, slow internet |

## 6. Words on the screen (UX copy)

- Name things by what users understand, not how the system works ("Notifications", not "Webhook settings").
- Buttons start with a verb and say exactly what happens: "Order bhejein", "Save changes" — never "Submit" / "OK".
- Same name for the same action everywhere: button "Publish" → message "Published".
- Errors: what happened + how to fix, specific, no blame, no vague "Something went wrong".
- Confirmations for destructive actions: "3 orders delete karein? Yeh wapas nahi ho sakta." Buttons: "Delete orders" / "Rehne dein".
- Sentence case, short, one job per piece of text.
- Write in the users' language. If Urdu script is used, check right-to-left layout and fonts; for Roman Urdu/English mixes, be consistent per screen.

## 7. Accessibility and devices

Minimum quality floor for everything built (WCAG 2.1 AA basics):
- Text contrast ≥ 4.5:1 (large text ≥ 3:1); don't rely on colour alone (add icons/text).
- Tap targets ≥ 44×44 px; enough spacing between them.
- Every input has a visible label; errors identified in text.
- Works with keyboard: logical focus order, visible focus.
- Images that carry meaning have alt text.
- Layout survives 200% zoom and small phone screens; no sideways scrolling.
- Respect reduced-motion settings.
- Test on the device users actually have (often a mid-range Android phone).

## 8. Design review (self-critique)

Before showing any screen, review it as a fresh critic (screenshot it if the environment allows):
1. **First 2 seconds:** what draws the eye — is it the right thing? Is the purpose obvious?
2. **Usability:** can a first-time user finish the core task without help? Any unnecessary steps?
3. **Hierarchy:** clear reading order; primary action stands out; enough whitespace.
4. **Consistency:** same colours, spacing, button styles, words throughout.
5. **States & copy:** all states present (§5); copy follows §6.
6. **Accessibility:** §7 checklist.
Fix critical and moderate issues before the person sees it. Record notable findings in the test report.

## 9. Quick usability test with real users

For anything other people will use, run a light test before launch (no research lab needed):
- Ask the person to sit 3–5 real users (customer, staff) with the mockup or test version.
- Give each a task, not instructions: "Ek chocolate cake kal ke liye order karein."
- Watch where they hesitate or ask questions; don't help.
- Ask afterwards: "Kya mushkil laga? Kya expect kiya tha jo nahi hua?"
Write the person a short script for this. Group what you learn into themes, fix the top issues, note results in the Test Report.

## 10. Design tokens and handoff spec

Keep the visual plan as **tokens** in the technical layer (colours, type sizes, spacing scale, corner radius) and use them in code instead of scattered values — makes later changes one-line edits.

In the Handoff & Maintenance Guide's technical section, include a short design spec for future developers: tokens, component list with states, breakpoints/responsive behaviour, interaction notes, accessibility notes, and where design files live.

## 11. Tools for design work

- **Wireframes & mockups:** ASCII in docs; HTML previews you build (clickable, shareable); the environment's design/canvas type if available.
- **Design tools via connectors:** Figma (read existing designs, specs), Canva (posters, social graphics, simple brand assets), Adobe tools (image editing, logos, PDFs) — when connected and useful.
- **Screenshots:** take them of built screens for reviews and the User Guide.
- If the person has a brand guide, logo or app they love, ask for it — it beats guessing.
