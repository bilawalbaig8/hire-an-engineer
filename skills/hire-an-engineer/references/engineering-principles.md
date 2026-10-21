# Engineering Principles — selector

Contents: Delivery process · Definition of Ready and Done · Design and code principles · Code quality standards · Testing strategy · Security · Operations and reliability · Product learning after launch · Retrospectives

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
