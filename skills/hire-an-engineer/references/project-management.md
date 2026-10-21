# Project Management — planning, tasks, priorities, tracking

You are the project manager. Every project, however small, gets a real plan, a live task list, clear priorities and visible tracking. Scale the ceremony to the size tier (`project-cases.md`): a tiny tool gets a short checklist; a medium/large project gets everything below.

## Contents
1. Planning hierarchy
2. The task board (artifact)
3. Task anatomy
4. Setting priorities
5. Estimating and scheduling
6. Tracking and status updates
7. Risks, issues and change requests
8. Where the board lives

---

## 1. Planning hierarchy

```
Vision (one line: what this is for)
└── Roadmap: releases over time      v1.0 → v1.1 → v2.0
    └── Release: a version users get  v1.0 = "orders + daily report"
        └── Milestones: usable slices M1 order form, M2 report, M3 go live
            └── Tasks: one job each   "Build order form validation"
```

- **Vision & roadmap** come from the brief: v1 = must-haves, later versions = the "later" list, ordered by priority.
- **Each release** has a goal, a scope list, a target date and a version number (see `versioning-release.md`).
- **Milestones** end in something the person can open and use.
- **Tasks** are what you actually do — small enough to finish and verify in one sitting.

## 2. The task board (artifact)

Every project beyond tiny gets a **live task board** the person can open any time. Build it in this order of preference:
1. In the project tool they already use, via connector (GitHub Projects, Trello, Asana, Linear, Notion, monday, Jira).
2. An interactive task-board artifact (an HTML page with saved state, if the environment can publish artifacts) — columns, filters by priority/milestone, progress bar, and burndown/progress chart.
3. A Google Sheet / Excel tracker with status dropdowns, priority colours and a progress chart.
4. A Markdown checklist inside the Project Plan document (fallback, and for tiny projects).

Board columns: **Backlog → To do (this milestone) → In progress → In review/testing → Done**, plus a **Blocked** flag.

Views the person cares about: "What's done", "What's next", "What do you need from me". Keep technical tasks visible but labelled so they can ignore them.

Update the board as you work — every task you start or finish moves. A board that lags reality is worse than none.

## 3. Task anatomy

| Field | Example |
|---|---|
| ID | T-014 |
| Title (verb first) | Add "phone number" validation to order form |
| Why / user value | So wrong numbers don't break WhatsApp alerts |
| Milestone / release | M1 / v1.0 |
| Priority | P1 |
| Type | Feature / Bug / Design / Setup / Docs / Test / Chore |
| Estimate | S / M / L |
| Depends on | T-010 |
| Done when (acceptance) | Wrong number shows message; valid number saves; test passes |
| Owner | Agent / Person (e.g. "send product photos") |
| Status | To do / In progress / Review / Done / Blocked |
| Links | GitHub issue/PR, test report |

Tasks owned by the person (provide content, approve design, test on their phone, make payments) are real tasks with dates — they're often the biggest blocker.

## 4. Setting priorities

Use one simple, consistent scheme and show it on the board:

| Priority | Meaning | Rule |
|---|---|---|
| **P0 — Critical** | Broken/unsafe/blocking everything | Drop everything, fix now |
| **P1 — Must** | Needed for this release to be useful | In the current release |
| **P2 — Should** | Valuable, release works without it | Next release unless cheap |
| **P3 — Could** | Nice to have | Backlog; revisit later |
| **Won't (now)** | Explicitly out | Recorded so it isn't re-debated |

How to decide (internally, with `thinking-toolkit.md`):
- **Impact vs effort:** high impact + low effort first.
- **Risk first:** tasks that test the riskiest assumption or unknowns go early.
- **Dependencies:** what unblocks the most other work goes first.
- **Walking skeleton:** the thinnest end-to-end version of the core action before polishing any part.
- **Bugs:** P0 bugs beat all features; other bugs are prioritised alongside features by impact.

Show the person priorities in their terms: "Pehle yeh 4 cheezein (inke baghair app ka faida nahi), phir yeh 3 (achi hain, baad mein aa sakti hain)". They approve the P1 list for each release; you handle ordering within it.

## 5. Estimating and scheduling

- Size tasks S / M / L; give the person ranges in days/weeks, never false precision.
- Add buffer (~30%) for unknowns and for waiting on the person.
- Put person-owned tasks and approval points on the timeline explicitly.
- Show the schedule as a Gantt chart in the Project Plan; update when it moves and say why.

## 6. Tracking and status updates

At every milestone (and weekly on longer projects), give a status update and update the board, plan and charts:

```
Status: 🟢 On track / 🟡 At risk / 🔴 Blocked
Done: …
Next: …
Need from you: …   (with dates)
Risks: …
Progress: [chart] 9/14 tasks · v1.0 target [date]
```

Charts to keep current: progress (tasks done over time / burndown), release progress per milestone, test pass rate, open bugs by priority.

## 7. Risks, issues and change requests

- **Risk register** (in the Project Plan): risk, likelihood, impact, what we're doing about it. Seed it from the pre-mortem.
- **Issues/bugs:** go on the board as tasks with priority and steps to reproduce.
- **Change requests:** when the person asks for something new mid-release, add it to the backlog, assess impact (time, what moves), and let them choose: add to this release (and move a date or drop something) or schedule for the next. Record the decision in the decision log and the plan's change log.

## 8. Where the board lives

Record the board's link in the Tools & Setup Guide and at the top of the Project Plan. If tasks also live in GitHub Issues, keep one source of truth — the GitHub Project board — and link to it rather than duplicating.
