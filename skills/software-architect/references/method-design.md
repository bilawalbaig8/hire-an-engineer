# Design mode: designing a new system

When to read this: the request is to design (or redesign) a system, an app, a game, a platform or an AI feature, and there is no existing architecture to recover.

You never talk to the owner directly. You answer the boss in the 7-field handoff shape (`status`, `summary`, `files`, `questions`, `approvals`, `assumptions`, `evidence`). Questions and approvals travel back to the boss.

## The five steps

### 1. Ask only what changes the design
First turn: look at what the boss gave you (goal, files, constraints). If something that would change the design is missing, return `status: needs_answers` with **at most 5 questions**, each with a `why` ("this decides whether we need offline support"). If nothing important is missing, state your assumptions and go on.

Question bank (pick only those whose answer would change the design):

| Topic | Questions that matter |
|---|---|
| Users | Who uses it and how many, now and in a year? Are they logged in? Children? |
| Where it runs | Browser, phone (which OS, how old), console, desktop, server? Offline? |
| Data | What is stored, how much, how sensitive? Can anything be lost? Does it belong to users or the business? |
| Money and law | Does real money move? Personal data, health or children's data? Which countries? Store rules? |
| What must never fail | Which single failure would hurt most (payment lost, saved game lost, wrong answer)? |
| Time and team | Deadline? Who builds and runs it, how many people, what skills? |
| Budget | A monthly running cost ceiling? Free tiers only? |
| Existing | What is already built, decided or required (hosting, accounts, tools)? |

Turn each answer into a scenario (see `core-principles`, section 2).

### 2. Write the scenarios
List 4 to 8 testable quality scenarios, ordered by importance. Mark the 2 or 3 that drive the design. Write them to `docs/architecture/scenarios.md`.

### 3. Generate and compare options
Produce 2 or 3 genuinely different candidate shapes (not three variations of one). For each: a one-paragraph description, how it meets each top scenario, and **what it gives up**. Compare in a table:

| | Option A | Option B | Option C |
|---|---|---|---|
| Meets scenario 1? | | | |
| Meets scenario 2? | | | |
| Build effort / running cost | | | |
| Hardest to change later | | | |
| What it gives up | | | |

Pick the simplest option that meets the top scenarios, and name the trigger that would make you step up (see `core-principles`, section 4). Field knowledge for the options lives in the field references you were pointed to (web and backend, mobile, game, AI, data).

### 4. Write the artifacts
Write files into the project (see "Artifacts" below). Keep them short and plain. Show one simple diagram of the main shape.

### 5. Hand back decisions
Sort decisions: two-way doors are decided and recorded as `accepted`. **One-way doors** are returned in `approvals` with `one_way_door: true`, your recommended option, the options and what each gives up, and their ADR is written as `proposed`. Return `needs_approval` when at least one is open; otherwise `done`.

## Artifacts

```
docs/architecture/overview.md    the system on one page
docs/architecture/scenarios.md   the testable scenarios
docs/architecture/risks.md       what could hurt, and what breaks at 10x
docs/architecture/diagrams/      diagram sources and rendered images
docs/decisions/NNNN-title.md     one record per decision (continue an existing series)
```

### overview.md (arc42-style skeleton; keep only what the project needs) [S-FND-12]
1. Goals: what the system must do, and for whom, in two sentences.
2. Constraints: money, time, team, platform, rules and laws.
3. Context: who and what the system talks to (people, other systems).
4. Solution strategy: the chosen shape in one paragraph and why.
5. Building blocks: the main parts, each with one sentence of responsibility and who owns it.
6. Runtime view: the 2 or 3 most important flows step by step.
7. Deployment: where each part runs.
8. Cross-cutting concepts: security, errors, logging, data handling, offline.
9. Decisions: a list linking each ADR.
10. Quality scenarios: link to docs/architecture/scenarios.md.
11. Risks and open questions: link to docs/architecture/risks.md.

### scenarios.md
A table: ID, scenario (the sentence format), measure, priority, how it will be checked.

### risks.md
- Top risks in order, each with likelihood, impact, and the first step to reduce it. [S-FND-15]
- **What breaks at 10x**: for each of data size, users, team size and cost, the first thing that breaks and how you would notice early.
- Assumptions you made that nobody confirmed.

### ADR (decision record) template
```
# NNNN. Title
Status: proposed | accepted | superseded by NNNN | inferred
Date: YYYY-MM-DD

## Context
The situation and the forces at play (2 to 5 sentences).

## Options considered
1. Option A: what it is, what it gives up.
2. Option B: what it is, what it gives up.

## Decision
What we chose and why, in two sentences.

## Consequences
Good, bad, and what we now have to watch.
```
If `docs/decisions/` already has records, copy *their* format and number instead. [S-FND-13] [S-FND-14]

## What goes in the response

- `status`: `needs_answers` (first turn, questions), `needs_approval` (a one-way door is open), `done` (everything written), or `blocked` (say why).
- `summary`: plain language for a non-engineer, 5 to 10 sentences: what you chose, why, what it gives up, what you need decided. No jargon without a one-line explanation. Include one simple picture (see `diagrams`).
- `files`: every path you created or changed.
- `assumptions`: everything you assumed instead of asking.
- `evidence` (required for `done`): things the boss can check without trusting you, for example "docs/architecture/scenarios.md has 6 scenarios, each with a measure", "diagram source renders with command X: output file exists", "ADR 0001 status proposed". "I checked it works" is not evidence.

## Quick self-check before you answer

- Is every top scenario covered by the chosen option, or its gap named in the risks?
- Is the shape the simplest that fits? Is the step-up trigger written?
- Does every decision say what it gives up?
- Are one-way doors returned as approvals, not decided?
- Could someone new build from these files without asking you anything important?

## Sources
[S-FND-12] [S-FND-13] [S-FND-14] [S-FND-15]
