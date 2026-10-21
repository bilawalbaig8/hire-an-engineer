# Workflow — the phases

Scale every phase to the size tier; use the fast lane (SKILL.md) when they want speed. Start where the person is: vague idea → Phase 1; existing or half-built project → rescue steps in `getting-unstuck.md` §4, then join where it fits; automating a manual task → `process-automation.md` inside these phases.

## The project pack (sized to the project — see `documents.md`)

Brief · Tools & integrations register · UX & UI design · System design + data dictionary · Plan & roadmap + task board · Test plan & reports · Release checklist, changelog & notes · Cost register (record-only by default) · User guide · Handoff & maintenance guide — all in `docs/`, plus `AGENTS.md` and `PROJECT_STATE.md`.

## Phase 1 — Discovery
One line offering to just start ("bas shuru karo", in their language), then one open question about a real moment; ask in one message, grouping questions that block the same decision, **~5–7 in total**, then stated assumptions. If the person already asked for specific deliverables (plan, design, structure, tests), deliver them now on stated assumptions and ask only the 1–2 questions that block the next step, after the deliverable. Cover problem and current workaround, users, the one core action, inputs/outputs, constraints, success/failure, examples they can share, tool/tech preferences. Run the hidden-requirements checklist (`plain-language.md`) and the thinking tools (root cause, job to be done, do-nothing test). Classify size and type (`project-cases.md`). Summarise the sharpened problem back in their words.

## Phase 2 — Brief
v1 must-haves (few), later list, non-goals, constraints, done-when, main journeys. Riskiest assumption named — test it cheaply if possible. Approval.

## Phase 3 — Approach, tools, setup
Options (incl. one that removes something and one non-software), clear recommendation (`tools-and-stack.md`). Tools and integrations chosen and set up with permission (`tools-and-stack.md`, `integrations.md`); repo and scaffold with memory files (`github.md`, `project-memory.md`). Cost estimate, budget, and the one-time "dekhna chahenge ya record mein rakhun?" question (`cost-management.md`).

## Phase 4 — Design
UX/UI first: journeys → screens → wireframes → visual plan → clickable mockup they can open on their phone; all states and copy; self-critique; approval (`ui-ux.md`). Then system design, integrations, AI features with cost limits, database and data dictionary (`database.md`, `integrations.md`, `cost-management.md`, `technical-products.md` if relevant). Show screens and flows only; approval.

## Phase 5 — Plan & tests
Roadmap with versions, milestones (first = thinnest end-to-end core action), Gantt, risks, person-owned tasks; prioritised task board (`project-management.md`). Implementation plan in the technical layer; test plan per milestone (`engineering-discipline.md`, `engineering-principles.md`).

## Phase 6 — Build
Board order; branch per task; tests first for core logic; small commits; PR + review; CI green; migrations for DB changes; screens to the approved mockup; ~20-min checkpoints (`github.md`, `project-memory.md`). Keep moving; log rulings; stop only for approvals, risks, or changes to what they asked for.

## Phase 7 — Verify & report
Fresh checks with evidence ("12 mein se 12 pass"); a few checks for them on their device; test report, board, status (🟢/🟡/🔴, done, next, needed from you). Usability test with real users before others rely on it. Stuck or failing repeatedly → `getting-unstuck.md`.

## Phase 8 — Release
Per `versioning-release.md`: frozen scope, green evidence, backup, migration tested, version + changelog + notes + tag, approval, deploy, checks on live, monitoring. Update cost register and alerts; close milestone; update roadmap.

## Phase 9 — Handoff & support
User guide, handoff & maintenance guide, one-page "where everything lives". Later problems → incident, rollback if serious, root-cause fix, hotfix version. New ideas → backlog with priority → next version. Monthly AI-usage audit in the records.

## Watch for
Scope creep (to "later" unless it changes the core need) · not a software problem (say so) · their capacity to maintain it · honest estimates and costs up front · stale docs or `PROJECT_STATE.md`.
