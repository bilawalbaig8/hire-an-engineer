# Review: Solution Architect, Project structure mode (B5) and move of the data design sources (B6)

Date: 2026-10-24
Reviewer: code-reviewer (opus)
Change: uncommitted work in the working tree against `HEAD` (10 modified files, 4 new reference files). Read with `git diff HEAD` and by reading the new files in full.
Requirement: `docs/superpowers/specs/2026-10-24-architect-project-structure.md` section 6 (build plan), the boss request `02-code-reviewer-request.json`, and the architect's response `01-architect-response.json`.

## Verdict

**Approved, with minor findings.** No Critical or Important findings. The build follows section 6 for everything in scope, System design and Data design are unchanged except the one allowed line, the 40 data design sources moved completely and unchanged in URL, year and status, and all checks pass. The label "built, not tested" is honest and safe to use: no evals exist or were run, and the mode is not installed.

Findings: Critical 0, Important 0, Minor 6.

## Checks run (all on the working tree, offline)

| Command | Result |
|---|---|
| `python scripts/validate_agents.py` | all 9 agents ok, exit 0 |
| `PYTHONUTF8=1 python scripts/validate_skills.py` | `software-architect: description 946 chars, SKILL.md 65 lines`; "All skills valid.", exit 0 |
| `python scripts/check_sources.py skills/software-architect` | "sources and citations ok", exit 0 |
| `python scripts/check_roster.py` | ok, exit 0 |
| `python -m pytest tests/test_install_office.py -q -p no:cacheprovider` | 16 passed |
| `python scripts/sync_team_start.py --check` | exit 0 (copies up to date) |
| Description lengths (front matter, counted by script) | `agents/architect.md` 904, `SKILL.md` 946; both under 1,024 |
| Script comparing the 40 rows of the data design table in `git show HEAD:docs/agents/roles/solution-architect.md` with the S-DB rows in `sources.md` | 40 and 40 rows; same order; every URL, year and status identical; no URL lost |

Not run: evals (none exist; out of scope), install, `check_evals.py`, `check_installed.py`. No network was used, so S-STR pages were not opened by this review (see "Spot-check of sources").

## Spec compliance (section 6)

| Item | State | Evidence |
|---|---|---|
| Four new references, loaded only in this mode | Met | `method-structure.md` (70 lines), `structure-trees.md` (109), `naming-rules.md` (56), `data-structures.md` (78); each says "Project structure mode" in its "When to read this" line. Shorter than the estimates; the spec calls sizes estimates |
| S-STR-1 to S-STR-30 in `sources.md` with status | Met | 30 rows, 26 verified, 4 unverified (S-STR-2, 23, 24, 25), each unverified row says why |
| Router: "Pick the mode" row and "Router" row | Met | `SKILL.md` lines 18 and 55 |
| Rules 14 and 15 | Met | `SKILL.md` lines 35-36, wording matches the spec |
| "What you produce" additions | Met | `SKILL.md` line 62 (`structure.md`, `tree.txt`, `naming.md`, `restructure-plan.md`) |
| Agent Never rule on moving, renaming, deleting outside `docs/architecture/`, `docs/decisions/`, `docs/data/`, including `git mv` | Met | `agents/architect.md` line 83, as the spec words it |
| Agent: mode in Role, When to use, Reads first, How it works | Met | `agents/architect.md` lines 14, 22-23, 40, 44 and 47 |
| Tools and model unchanged | Met | diff touches neither `model: opus` nor the `tools:` line |
| Descriptions as drafted (904 and 946) | Met | measured above |
| Roster and orchestrator routing (three modes, hand-offs) | Met | `docs/agents/roster.md`, `skills/team-start/runtime/roster.md` (identical copy), `skills/orchestrator/references/team-roster.md` lines 18-23 |
| `docs/lessons/architect.md` in the agent's reading list (decision X2, section 6 housekeeping) | Not met | see M1 |
| Boss defaults Q1-Q8 in the references | Met except Q4 | Q1 `method-structure.md` 5 and `naming-rules.md` 41; Q2 `method-structure.md` 29, 42; Q3 27; Q5 `structure-trees.md` 5, 15-22; Q6 `method-structure.md` 62, `naming-rules.md` 53; Q7 `method-structure.md` 7-11; Q8 50. Q4 (effort) has no home in a reference or the agent file (no effort field); the architect said so in its assumptions. Acceptable |
| Hand-offs to Software Engineer, Game & Technical Engineer, Project Manager say "not built yet" | Met | `method-structure.md` 5, 50; `data-structures.md` 3, 66; `naming-rules.md` 41, 53; `structure-trees.md` 13, 36, 100, 102; `agents/architect.md` 23, 47; `team-roster.md` 22 |
| Heuristics (4 levels, 20 files, 400 lines) not presented as sourced | Met | `structure-trees.md` line 5 and section 2 heading say "team heuristics, not sourced facts"; no source ID next to any of the numbers; `method-structure.md` line 61 repeats it |
| Agent never moves or edits project files | Met (by rule) | SKILL rule 14, agent Never line, `method-structure.md` line 5 and 57; `AGENTS.md` and `README.md` text only proposed (line 29). Enforcement is by rule and planned evals only (decision Q9: no guard hook) |
| Out of scope and not done: evals, install, CHANGELOG, THIRD_PARTY_NOTICES, B7 | Not reviewed | as the request says |

## System design and Data design unchanged

- `git diff HEAD --stat` shows no change to any other file in `skills/software-architect/references/` except `data-design.md` and `sources.md`.
- `data-design.md`: one line changed (line 41), from "the data design list in `docs/agents/roles/solution-architect.md`" to "the data design list is the S-DB group at its end". Nothing else in the file changed.
- `SKILL.md` rules 1-13: the diff only adds lines; no existing rule text changed. The two existing "Pick the mode" rows and all existing router rows are unchanged.
- `sources.md`: the diff only adds lines (a note near the top and two new groups at the end). No existing row changed.

## The S-DB move (B6)

- Complete: 40 of 40 rows moved, same order, every URL, year and status identical to `HEAD` (checked by script, see above). 38 verified, 2 unverified (S-DB-10, S-DB-40), as before.
- The pointer works: the role document (line 152) names `skills/software-architect/references/sources.md` and S-DB-1 to S-DB-40, and the group is there under "Data design (moved from the role document)". `data-design.md` line 41 points to the same group, so an installed copy can find it.
- No other file in `skills/`, `agents/`, `evals/`, `scripts/` or `tests/` referred to the old table (searched).

## Spot-check of sources (no network; checked against the spec's notes and well-known facts)

The S-STR rows match spec section 9 in title, author, year and URL. Rows checked against well-known content, all consistent: S-STR-9 (Rust: UpperCamelCase types and traits, snake_case functions and modules), S-STR-10 (Go: `internal/`, `cmd/`), S-STR-12 (SemVer MAJOR, MINOR, PATCH), S-STR-14 (Unity reserved names incl. `Gizmos`, `Editor Default Resources`), S-STR-15 (UPM `Runtime/`, `Editor/`, `Tests/`), S-STR-16 (Unreal `Source/`, `Content/`, `Config/`, generated `Binaries/`, `Intermediate/`, `Saved/`), S-STR-17 (Godot snake_case, C# PascalCase, `addons/`), S-STR-19 (Next.js `app`, `pages`, `public`, `src`, private `_folders`, route groups), S-STR-20 (VS Code `main`, `activate`, `deactivate`), S-STR-26 (Pike: cannot tell where time goes; fancy algorithms slow when n is small; data dominates), S-STR-23 and S-STR-25 DOIs and years. Reused IDs exist and fit their use: S-FND-5, S-GAME-3, S-GAME-37, S-REC-16, S-REC-18, S-REC-19.

Not checkable offline: S-STR-7's new note "its own file names are `snake_case`" (Google TypeScript guide). It is plausible and was changed by the architect after reading the page; `naming-rules.md` line 30 leans on it only as a side remark. Confidence: needs-check, not counted.

No invented number, URL or quote found. Example numbers ("212 of 220 files", "about 64 bytes each (estimate)", "500 now, 5,000 at 10 times") are labelled examples or estimates.

## Findings

### Critical
None.

### Important
None.

### Minor

**M1. `docs/lessons/architect.md` is not in the agent's reading list.** `agents/architect.md` "Reads first" (lines 36-40). Section 6 housekeeping says "`docs/lessons/architect.md` in the reading list (X2)"; other agents have it (`agents/writer.md` line 39, `agents/qa-test-engineer.md` line 41). Trigger: an owner lesson written to `docs/lessons/architect.md` is never read by the architect. Impact is low today (TASKS B3, lessons, is still open). Fix: add "`docs/lessons/architect.md` if it exists" to item 2 of "Reads first". Confidence: confirmed (grep found no `lessons` in `agents/architect.md`).

**M2. The spec contradicts itself after the status update.** `docs/superpowers/specs/2026-10-24-architect-project-structure.md` line 3 says 26 verified, 4 unverified and built; line 341 still says "27 verified, 3 unverified", line 346 still lists S-STR-2 as `verified`, and line 247 (decision 1) still says "planned, not built ... Nothing is built". Trigger: a reader of section 9 or 5 gets the old status. Fix: update line 341 and the S-STR-2 row, and mark decision 1 as "was: planned; now built, not tested". Confidence: confirmed. (The architect listed the "planned" leftovers in its assumptions; section 9 was not mentioned.)

**M3. The role document still says "two modes".** `docs/agents/roles/solution-architect.md` line 5: "one role, the Solution Architect, with two modes", while line 7 and the roster say three. Fix: "with three modes" and add Project structure to that sentence. Confidence: confirmed.

**M4. The S-DB group heading overstates "unchanged".** `sources.md` (Data design group intro) says "title, author, year, URL and status unchanged". URL, year and status are identical (script), but authors were expanded (for example "Codd" to "E. F. Codd", "PostgreSQL docs" to author "PostgreSQL Global Development Group"), titles got prefixes ("PostgreSQL docs: Constraints"), and the "Use" column is new text. None is wrong; the sentence is just not exact. Fix: "URL, year and status unchanged; author names written out and a Use note added". Confidence: confirmed.

**M5. Tie-break for an unclear sub-mode sends "a new part" to Audit.** `method-structure.md` line 13: "pick the one that matches what exists (code present: Audit)". The table on line 10 says New tree is also for "a new part of one". Trigger: "add a payments area to our app" with an unclear brief picks Audit and produces a restructure plan nobody asked for. Fix: "code present and the request is about the existing tree: Audit; a new part: New tree". Confidence: likely.

**M6. Roles that do not exist are not always marked.** DevOps Engineer and Data Engineer are not in `docs/agents/roster.md`; `structure-trees.md` section 7 marks them "not built yet", but `structure-trees.md` lines 48-49 and `method-structure.md` lines 62-63 name them without it. Trigger: the architect's answer names DevOps as the role that runs a check, and the boss treats it as callable. The orchestrator's Missing role rule limits the harm. Fix: add "(not built yet)" at those places. Confidence: likely.

## Question (needs-check, not counted)

- q1. `docs/agents/roles/software-engineer.md` line 14 says the Software Engineer creates the tree including "empty modules"; `structure-trees.md` line 21 says "No empty folders ... a folder is created when its first file is". Probably compatible (a module is a file), but worth aligning when the Software Engineer is built.

## What is done well

- The S-STR re-check was honest: S-STR-2 was downgraded from the spec's `verified` to `unverified` with the reason, and unverified sources (Parnas, Conway, Knuth, Brown) are cited only as "leads", with Pike cited instead of Knuth.
- The "design only, never move" rule is stated in four places that agree (SKILL rule 14, agent Never, `method-structure.md` top and "Rules that never bend"), and prompt text inside audited files is treated as data.
- Heuristic numbers are clearly labelled as team defaults, changeable per project.
- Reuse instead of copying: the audit points to `method-recover.md` steps 1, 3, 4 and 5; no new scripts.

## Recommended next steps

A short fix pass (Sonnet-level work) for M1-M6, then the 27 evals (B5 follow-up) before the label can move from "built, not tested" to "tested". Owner of the fixes: the architect's maintainer (whoever built B5), not the reviewer.
