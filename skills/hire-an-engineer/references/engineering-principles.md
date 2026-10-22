# Engineering Principles — selector

Contents: Delivery process · Definition of Ready and Done · Design and code principles · Code quality standards · Testing strategy · Security · Operations and reliability · Product learning after launch · Retrospectives · Data and performance choices · Runtime performance: browser, devices, OS

You already know these methodologies. This file says **which to apply, on which size of project, in which phase, and how much**. Apply them as a professional engineer would — silently, as standard practice — and never name them to the person unless asked.

Size tiers (Tiny / Small / Medium / Large) are defined in `project-cases.md`. "✓" = apply; "lite" = a lightweight version; "—" = skip.

---

## 1. Delivery process

| Size | Process | Rhythm |
|---|---|---|
| Tiny | Just do it: plan → build → verify | One sitting |
| Small | Kanban: board, WIP of 1–2 tasks, milestone demos | Release per milestone |
| Medium | Kanban + short iterations (≈1–2 week releases), milestone reviews with the person | Status each milestone/week |
| Large | Scrum-style iterations: iteration goal, backlog refinement, review/demo with the person, retrospective; release train of versions | Fixed iteration length |

- **Waterfall-style fixed scope** only when requirements are genuinely fixed and well understood (e.g. a regulatory form, a migration with a clear spec). Even then, deliver in verified slices.
- **Lean / MVP** always: the smallest thing that tests the core value first.
- **Shift-left**: requirements, design, security and tests are thought about early, not bolted on at the end.

## 2. Definition of Ready and Done

**Ready** (a task can start when): clear goal, done-when written, priority set, dependencies available, design approved (if UI), data/content from the person received.

**Done** (a task/milestone is done only when):
- [ ] Meets its acceptance criteria — verified with fresh evidence
- [ ] Automated tests written and passing; nothing else broke
- [ ] (Small+) Code reviewed; no debug leftovers or hardcoded secrets
- [ ] UI: all states, mobile checked; accessibility checklist (Small+)
- [ ] Docs updated; data dictionary and changelog (Small+); `PROJECT_STATE.md` reflects the change
- [ ] (Small+) Merged to `main`, CI green; board updated
- [ ] (Milestone) person has seen it working

## 3. Design and code principles

| Principle | How it shows up | Tiny | Small | Med | Large |
|---|---|---|---|---|---|
| **KISS** | Simplest design that works; no clever tricks | ✓ | ✓ | ✓ | ✓ |
| **YAGNI** | Build only what the brief requires | ✓ | ✓ | ✓ | ✓ |
| **DRY** | One source of truth for each rule/value — but don't abstract after only one repeat | lite | ✓ | ✓ | ✓ |
| **Separation of concerns** | Screens, logic, data access in separate places | — | ✓ | ✓ | ✓ |
| **SOLID** (single responsibility above all) | One job per module/function; depend on interfaces at boundaries (DB, AI, payments) so they can be swapped/tested | — | lite | ✓ | ✓ |
| **Clean / layered architecture (lite)** | UI → application logic → data/services; core logic doesn't depend on frameworks | — | — | lite | ✓ |
| **12-Factor App** | Config in env vars, stateless app, logs to stdout, same build for test & live, dependencies declared | — | lite | ✓ | ✓ |
| **Domain-driven naming** | Code uses the person's business words (order, batch, delivery), matching the data dictionary | ✓ | ✓ | ✓ | ✓ |
| **Fail fast, fail safe** | Validate inputs at the edges; clear errors; never silently lose data | ✓ | ✓ | ✓ | ✓ |
| **Least privilege** | Each part/user gets only the access it needs | — | ✓ | ✓ | ✓ |
| **Decision records (ADRs)** | Significant choices in the decision log with context and trade-off | — | lite | ✓ | ✓ |

## 4. Code quality standards

Always:
- Consistent formatter and linter for the language; run in CI (Small+).
- Clear names; small functions; comments explain *why*, not *what*.
- Handle errors deliberately: user-friendly message outside, detailed log inside.
- No secrets in code; config via environment.
- Pin dependency versions; prefer few, popular, maintained libraries.
- README that lets a new developer run the project in under 15 minutes.

## 5. Testing strategy

**Testing pyramid** — many fast low-level tests, fewer slow high-level ones:

| Type | What it checks | Tiny | Small | Med | Large |
|---|---|---|---|---|---|
| **Unit** | Core logic, test-first | ✓ | ✓ | ✓ | ✓ |
| **Integration** | Parts working together: app ↔ DB, app ↔ AI/APIs | — | lite | ✓ | ✓ |
| **End-to-end (E2E)** | Full user journeys in a real browser/device | — | 1 main flow | key flows | all critical flows |
| **Acceptance / UAT** | Person's Given/When/Then checks; person signs off | ✓ | ✓ | ✓ | ✓ |
| **Regression** | Whole suite rerun after every change | ✓ | ✓ | ✓ | ✓ |
| **Smoke** | Quick "is it alive and core action works" after each deploy | — | ✓ | ✓ | ✓ |
| **Exploratory** | You try to break it like a curious user (odd inputs, back button, double click) | lite | ✓ | ✓ | ✓ |
| **Usability** | Real users try tasks (`ui-ux.md` §9) | — | lite | ✓ | ✓ |
| **Accessibility** | WCAG AA checklist + automated scan | lite | ✓ | ✓ | ✓ |
| **Security** | OWASP checks, permission tests (§6) | — | lite | ✓ | ✓ |
| **Performance / load** | Speed with realistic data; behaviour at expected peak users | — | — | lite | ✓ |
| **Data/migration** | Row counts, integrity after imports/migrations | if data | if data | ✓ | ✓ |
| **Contract** | External API responses still match what code expects | — | — | if APIs | ✓ |
| **Cost** | Tokens/cost per AI call within limits | if AI | if AI | if AI | if AI |

Principles: test behaviour, not implementation; every bug fixed gets a regression test; flaky tests are fixed or removed, never ignored; test data is realistic but never real personal data.

## 6. Security

Apply **security by design** and **privacy by design** from Phase 4, scaled to size.

**OWASP Top 10 checklist** (Small+ when anything is online):
- Access control enforced on the server/database, not only the UI (test: user A cannot read user B's data)
- No secrets in code; HTTPS everywhere; passwords never stored by you — use a proven auth provider
- Injection safe: parameterised queries, no raw input in queries/commands
- Insecure design: threats considered in Phase 4 (below)
- Secure config: no debug mode or default credentials in live; minimal open endpoints
- Vulnerable components: Dependabot/updates on
- Authentication: proven provider, rate-limited logins, session expiry
- Data integrity: validate uploads, verify webhooks
- Logging & monitoring: security-relevant events logged (without sensitive content)
- SSRF and external requests: only call known, allowed services

**Threat modelling (STRIDE lite)** — Medium/Large, in Phase 4: for each data flow ask: can someone pretend to be someone else, tamper with data, deny an action, see data they shouldn't, take the service down, or gain more access? Write the top risks and safeguards in the design doc.

**Privacy by design:** collect the minimum, explain it to users, set retention, allow export/delete, keep personal data out of logs and AI prompts unless needed.

**Risks specific to AI-built projects** (every size):
- **Prompt injection in AI features.** Anything the AI reads that a user or outsider wrote (messages, emails, uploaded files, web pages, reviews) can contain instructions meant to hijack it. Keep your instructions and that content separate and label the content as data; give the AI feature only the access it needs (read-only where possible, no secrets in the prompt); never let model output run as code, a query or a command without validation; and an action that sends, pays, deletes or changes other people's data needs a code check or a human OK, never the model's say-so alone. Test it: put "ignore previous instructions and …" in a test input and confirm nothing happens.
- **Check every new package before installing.** AI tools sometimes suggest package names that don't exist, and attackers publish malware under exactly those names (or near-copies of popular ones). Before adding a dependency: it exists on the official registry under that exact name, is widely used and recently maintained, and is really the one the docs mean. Prefer the standard library or a package already in the project; commit the lockfile; never run install scripts or `curl … | sh` from an unverified source.
- **Stop secrets before they leave the machine.** Besides GitHub secret scanning (`github.md`), add a local pre-commit secret check (e.g. gitleaks) on Small+ projects and keep `.env` in `.gitignore` from the first commit. If a key was ever committed or pasted anywhere public, treat it as leaked: the person revokes and replaces it with the provider (their account, their action), then remove it from the code — deleting it from history alone is not enough.

## 7. Operations and reliability

| Practice | Tiny | Small | Med | Large |
|---|---|---|---|---|
| Uptime check + alert to the person | — | if online | ✓ | ✓ |
| Error tracking (errors captured with context) | — | lite | ✓ | ✓ |
| Structured logs | — | lite | ✓ | ✓ |
| Metrics (usage, speed, errors, cost) dashboard | — | — | lite | ✓ |
| **SLO** — agreed target in plain words ("99% time chalega; order 2 sec mein save") | — | — | lite | ✓ |
| Backups + tested restore | if data | ✓ | ✓ | ✓ |
| Rollback ready | keep old copy | ✓ | ✓ | ✓ |
| **Blameless postmortem** after an incident: what happened, impact, root cause, fix, prevention | — | lite | ✓ | ✓ |

## 8. Product learning after launch

- **Build → measure → learn:** decide 1–3 numbers that show the software is working for the person (orders per day captured, time saved, active users). Track them simply (privacy-respecting analytics or database counts).
- Review with the person at each release (if they want it); feed findings into the backlog with priorities.
- Kill or simplify features nobody uses.

## 9. Retrospectives

After each milestone (Small+), spend a few lines in the technical layer on: what went well, what went wrong, what we'll change. Apply the change in the next milestone (Kaizen — continuous improvement). Share with the person only items that affect them (e.g. "next time content pehle bhej dein to 2 din bachenge").

## 10. Data and performance choices

You know data structures and algorithms; these rules cover the defaults AI-written code most often gets wrong. Apply whenever code handles lists, searches, sorting, nested data or anything that grows — every size; Small+ for the performance test.

1. **Ask the real size first.** How many rows, items, users or files now, and in a year? Design for ~10× that. A list of 50 and a list of 500,000 need different code.
2. **Lookups by key → a map/dictionary/set**, not a search through a list each time. Checking "is this ID already seen?" inside a loop is the classic case.
3. **No loop inside a loop over large data.** Comparing every item to every other item is fine for 100, unusable for 100,000. Group or index first (one pass into a map, then look up).
4. **Use built-in sort, search and collection types.** Never hand-write a sort, binary search, hashing or date maths when the language or a well-known library has it.
5. **Let the database do the work.** Filter, sort, count, group and paginate in the query, with indexes on those fields (`database.md`), instead of loading everything into the app. Never run a query inside a loop (fetch once, or join).
6. **Paginate or stream anything that can grow** — lists on screen, API results, exports, file reads. Never load "all records" into memory or one page.
7. **Pick the structure that fits the shape of the data:** ordered items → list/array; unique items → set; key → value → map; first in, first out → queue; hierarchy (folders, categories, org chart, comment threads) → tree with parent IDs; connections (friends, routes, dependencies) → graph as a list of links. Store trees and graphs in the database as rows with parent or link IDs, not as one big blob.
8. **Deep trees and graphs: loop, not deep recursion.** Recursion can crash on deep or cyclic data; use an explicit stack/queue, and track visited items in a graph so cycles can't loop forever.
9. **Cache only what is slow and read often**, with a clear rule for when it expires. A cache without expiry is a stale-data bug.
10. **Don't optimise blind.** Simple and correct first; when something is slow, measure where the time goes and fix that step only (`thinking-toolkit.md` §6, Find the bottleneck).
11. **Test with realistic size.** At least one test or check with data at the expected 10× size (generated, never real personal data), and note the timing. Required at Medium/Large; for Small, do it whenever the data can grow.
12. **Review question:** "What happens when this data is 10× bigger?" Part of every code review (`engineering-discipline.md` §6).

Tell the person only the outcome in their terms ("1 lakh orders par bhi list 1 second mein khulti hai"), never the structure names.

## 11. Runtime performance: browser, devices, OS

How the software behaves on the real machine: speed, memory, CPU, battery. Games, engines, WebGL and playable ads use the stricter budgets in `technical-products.md` §4; this section covers everything else (websites, web apps, desktop apps, scripts, automations).

**Budgets** — set in Phase 4, measured on the weakest device that real users have (usually a mid-range Android phone on 4G, or an old office laptop), not only on your machine:

| Budget | Typical target (adjust to project) | Applies |
|---|---|---|
| Page shows main content (LCP) | ≤ 2.5 s on 4G | websites, web apps |
| Responds to a tap/click (INP) | ≤ 200 ms | websites, web apps |
| Layout doesn't jump while loading (CLS) | ≤ 0.1 | websites, web apps |
| JS sent on first load | as small as the job needs; check with a bundle analyzer | web apps |
| App/script start-up | a few seconds at most; show progress if longer | desktop apps, scripts |
| Memory | flat over a long session — no steady growth | all |
| CPU when idle | near zero; nothing spinning in the background | desktop apps, background jobs |

Apply: Tiny — rules only; Small — rules + one check on a weak device; Medium/Large — budgets written in the design doc and checked before every release (automated, e.g. Lighthouse CI, where possible).

**Browser rules:**
1. **Images:** right size for where they show (no 4000 px photo in a 300 px box), modern format (WebP/AVIF), lazy-load below the fold, width/height set so the layout doesn't jump.
2. **Less JavaScript:** no heavy library for a small job; split code so each page loads only what it uses; remove unused packages.
3. **Fonts:** one or two families, few weights, `font-display: swap`; system fonts are fine.
4. **Don't block the screen:** long work (parsing big files, heavy calculations) goes to a web worker or is split into chunks; show progress. Animate only `transform` and `opacity` (`motion.md`).
5. **Network:** fewer, smaller requests; compression and caching headers on (most hosts do this — check); show content as it arrives; handle a slow or dropped connection.
6. **Long lists** (hundreds of rows on screen): paginate or virtualise (render only what's visible).
7. **Memory leaks:** remove event listeners, timers and subscriptions when a screen closes. Test: leave the app open and in use for ~30 minutes — memory should stay flat.
8. **Real devices and browsers:** Chrome, Safari (iOS), Firefox, a cheap Android phone; check with throttled CPU and network in DevTools.

**OS, desktop and script rules:**
9. **Big files and data in pieces:** read and process in chunks or streams, never the whole file into memory at once.
10. **Don't freeze the app:** slow work (network, disk, heavy processing) runs async or in the background, with progress and a cancel option; the window keeps responding.
11. **Idle means idle:** no busy loops or polling every second; use events, schedules or sensible intervals. Background jobs pause or slow down on battery where the platform allows.
12. **Clean up:** close files, connections and child processes; delete temp files; no zombie processes after exit.
13. **Cross-platform:** build paths with the language's path tools (never hard-coded `\` or `/`), don't assume admin rights or a fixed install folder, handle file names with spaces and non-English characters; test on every OS the person's users have.
14. **Concurrency with care:** parallel work only where measured to help; limit how many run at once; protect shared data. Concurrency bugs are hard to undo — design and review it as risky code.

**Always:** measure before and after any optimisation (DevTools Performance and Memory panels, Lighthouse, Task Manager / Activity Monitor, a timer around the slow step) and fix the biggest cost first (`thinking-toolkit.md` §6, Find the bottleneck). Report to the person in their terms: "sasta phone par page 2 second mein khulta hai; 1 ghanta chalne ke baad bhi slow nahi hota."
