# Review 2: QA / Test Engineer agent after fix round 1 (2026-10-24)

## Verdict
- **Approved.** The 1 Important (I1) and 4 Minor (M1 to M4) findings of `docs/reviews/2026-10-24-qa-test-engineer-agent.md` are fixed. The fixes broke nothing: all three validators and the office tests pass.
- **Spec compliance: met.** The boss can now call `qa-test-engineer`. Status lines say "built, not tested", not "tested".
- **Quality: good.** No Critical or Important findings. 2 new Minor findings, both leftovers of I1 (N1, N2). They are documentation and display only.

## Scope
- Request: `.team/runs/2026-10-24-qa-test-engineer-agent/04-code-reviewer-request.json`.
- Read: the first review, `decisions.md`, `03-architect-response.json`, `agents/qa-test-engineer.md` in full. Also the changed lines of `skills/qa-test-engineer/SKILL.md` (rules 1, 2, 10), `references/method-art-qa.md` line 15, `references/method-test.md` lines 40-45 and `references/method-performance.md` lines 10 and 15. Plus `agents/orchestrator.md` lines 1-30, `skills/orchestrator/references/team-roster.md` (the qa lines), the status lines of the role file, the spec and `TASKS.md`, the office `TAGS` map, and `scripts/sync_team_start.py` (the copy list).
- Not reread: the parts of the skill references that this round did not change.
- Out of scope, as the request says: sources.md, evals, CHANGELOG, install, commit, and `agents/ai-engineer.md` line 50.

## Checks run
| Command | Result |
|---|---|
| `python scripts/validate_agents.py` | 7 agents ok, including `qa-test-engineer`; exit 0 |
| `PYTHONUTF8=1 python scripts/validate_skills.py` | `qa-test-engineer: description 1010 chars, SKILL.md 54 lines`; "All skills valid."; exit 0 |
| `python scripts/check_roster.py` | `ok: ...docs/agents/roster.md`; exit 0 |
| `python -m pytest tests/test_install_office.py -q` | `16 passed in 3.53s`; exit 0 |
| `diff docs/agents/roster.md skills/team-start/runtime/roster.md` | no difference |
| `diff` of the two office `index.html` files, line 869 removed | no other difference (only line 869 differs) |

## Earlier findings
| Id | State | Evidence |
|---|---|---|
| I1 boss list and status lines | **Fixed** (one step left, see N1) | `agents/orchestrator.md` line 3 (description), line 5 (`tools: Agent(..., qa-test-engineer)`) and line 28 all name `qa-test-engineer`. `team-roster.md` line 12 has the row and lines 34-39 add a "five modes" section. `skills/team-start/runtime/roster.md` line 14 is the same as `docs/agents/roster.md` line 14. The role file line 3 says "Status: built, not tested ... There are no evals yet". The spec line 3 says "Status: Built, not tested". `TASKS.md` line 134 says "Documented, Built, not tested". `docs/agents/visual-office/index.html` line 869 has `qa:'built'`. Nothing says "tested". |
| M1 "optimise" missing from Never | **Fixed** | Agent line 83: "or optimise the code or the assets (it measures and points; the builder optimises)". `SKILL.md` rule 1: "Never optimise". `method-performance.md` line 10: "Do not change or optimise the code or the assets". |
| M2 measuring scripts that do not exist | **Fixed** | Agent line 33 and `method-art-qa.md` line 15 now say that the scripts are not built yet. They say to use an installed tool or a small standard-library script in `docs/qa/` (`docs/qa/art/`), to give every number with its command, and to list a check with no working tool as "not run", never estimated. A grep shows the skill and the agent no longer name `image_specs.py`, `frame_stats.py`, `contrast.py` or `flaky_rerun.py`. |
| M3 held-out storage treated as open | **Fixed** | `decisions.md` line 2 records the default: QA keeps the cases outside the project folder (decision Q1). Agent line 14, `SKILL.md` rule 10 and `method-test.md` line 41 say the same and add "This is decided: do not ask the owner again." This matches `docs/agents/agent-template/README.md` line 30. Agent line 35 allows writes to that folder. `ai-engineer.md` line 50 was left as is (out of scope). |
| M4 "live URL" not defined | **Fixed** | Agent line 34, `SKILL.md` rule 2 and `method-performance.md` line 15 all give the same rule. A URL is a test copy only when the brief names it as a test copy, preview or staging build the owner set up for testing. Local builds count as test copies. Any other URL is live and goes to the boss first. The three wordings agree. |

## New findings

### Minor

**N1. The office copy inside the team-start runtime was not synced, so the installed office still shows QA as "Planned".**
- Where: `skills/team-start/runtime/ui/index.html` line 869 has `var TAGS={...,be:'built'}` with no `qa` entry. The source `docs/agents/visual-office/index.html` line 869 has `qa:'built'`. No other line differs.
- Trigger: install or run team-start from this repo. `scripts/sync_team_start.py` line 25 copies the source file to `ui/index.html`, but that copy was not refreshed after the edit. `tagOf` (line 871) then falls back to `'planned'` for the `qa` seat.
- Why it matters: this is the display-label problem that I1 was about. It now shows only in the copy that gets installed.
- Smallest fix: run `python scripts/sync_team_start.py`, then rerun `tests/test_install_office.py`. Owner: the boss (a mechanical step).
- Confidence: confirmed.

**N2. The spec's own state table and dashboard label still say "planned" and "Not started".**
- Where: `docs/superpowers/specs/2026-10-24-qa-test-merge.md` lines 10-14 (the "State" column is `planned` for all 5 modes) and line 16 ("Honest status label for the dashboard: 'Not started (0 of 5 modes)'"). Line 3 of the same file says "Built, not tested".
- Trigger: a reader of the spec sees two different statuses on the same page.
- Smallest fix: set the State column to "built, not tested" and the line 16 label to "Built, not tested (0 of 18 evals)". Owner: the boss (documents).
- Confidence: confirmed.

## What was met
The boss list (3 places) and the orchestrator roster name the agent. Every status line is honest ("built, not tested"). The Q1 default is in `decisions.md` and is used the same way in the agent, the skill and the method file. The "optimise" refusal, the not-built-scripts fallback and the live-versus-test-copy rule are each stated the same way in every file that mentions them. The agent and skill descriptions are still at or under 1,024 characters (validators pass).

## What could not be checked
How the agent behaves: there are still no evals (this is known and out of scope). The installed copy was not compared, because nothing was installed in this run.

## Fix plan (for the boss)
1. Run `python scripts/sync_team_start.py` and rerun the office tests (N1).
2. Update the spec's state table and line 16 label (N2).
3. Later, with the owner's go: sources.md, the 18 evals, CHANGELOG, install, commit.
