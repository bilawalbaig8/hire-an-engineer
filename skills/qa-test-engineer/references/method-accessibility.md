# Method: Accessibility mode

## 1. When to read this
A built web page, app, other software or game must be checked so people with disabilities can use it. Building accessibility into the design is the Designer's job; this mode audits what was built.

## 2. Steps
1. **Pick the standard** and write it in the plan in `docs/qa/accessibility/`: WCAG 2.2 level AA for web and apps; W3C's WCAG2ICT guidance for other software; the Game Accessibility Guidelines and the Xbox Accessibility Guidelines (with AbleGamers' player-experience patterns) for games. Do not apply web rules alone to a game.
2. **Automated scan first**, and say that a scan finds only part of the problems. A clean scan is never a pass.
3. **Manual checks:** keyboard only (every control reachable, no keyboard trap, visible focus), screen reader, 200 percent zoom, contrast, colour as the only signal, target size, captions and subtitles (size, speaker, background), flashing, reduced motion, remappable controls, difficulty and timing options for games.
4. **List each problem** with the rule it breaks, the place, the severity (`bug-report.md`) and how it was found (scan or by hand). A person locked out is severity 4.
5. **Say what needs a person with that need to confirm**, and propose it as a later step.

## 3. Target size
A WCAG AA failure (SC 2.5.8) is reported only below 24 by 24 CSS pixels. The project's own 44-pixel target from `hire-an-engineer/references/ui-ux.md` is reported as a project target, not as a WCAG failure. Say which rule you used.

## 4. Words
Write what was checked and against which rule. Never "accessible", "fully accessible", "WCAG compliant" or a conformance statement, and no legal advice on accessibility law; offer a report of what was checked instead.

## 5. Done (Accessibility)
The standard is named, the automated and manual checks are listed separately, each problem has a rule and a place, and the answer says what was not checked.
