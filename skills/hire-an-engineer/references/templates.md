# Templates — memory files and decision records

Read when creating or rebuilding AGENTS.md, PROJECT_STATE.md or decision records.

**AGENTS.md**
```markdown
# [Project] — Agent Instructions

## What this is
[2 lines]. Owner: [person]. Current version: see PROJECT_STATE.md.

## Always
- Start: read this file and PROJECT_STATE.md; check git status and tests.
- Checkpoint at least every ~20 minutes of work (see project-memory.md §4): commit + update PROJECT_STATE.md (Last updated, next step, session log).
- End: update PROJECT_STATE.md, decisions, docs, changelog; commit.
- Plan before code; tests first for core logic; no "done" without running tests.
- Never commit secrets; keys live in [where].
- Talk to the owner in plain language ([language preference]); they are not an engineer.

## Stack
[languages, frameworks, database, hosting]

## Run & test
[exact commands]

## Folder map
[tree with one line per folder]

## Conventions
[naming, file size, branching, commit style, formatting/linting]

## Docs
See docs/README.md. Docs are updated in the same change as the code.
```

**PROJECT_STATE.md**
```markdown
# Project State

Last updated: [YYYY-MM-DD HH:MM] by [tool/session]

**Version:** v0.3.0 · **Milestone:** M3 — editor MVP (60%)
**Status:** 🟢 / 🟡 / 🔴 — [one line]

## Done recently
- …
## In progress
- [task] — next exact step: …  (branch: feat/…)
## Next up (priority order)
1. …
## Blocked / waiting on owner
- …
## Open questions for owner
- …
## Known issues
- …
## Last session summary
[3–5 lines]

## Session log (today)
- HH:MM — [what changed]
```

**Decision record (docs/decisions/0007-title.md)**
```markdown
# 0007 — [Decision]   ([date], status: accepted)
Context: …
Decision: …
Alternatives considered: …
Consequences: …
```
