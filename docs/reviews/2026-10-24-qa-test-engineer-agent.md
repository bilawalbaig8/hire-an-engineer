# Review: QA / Test Engineer agent (2026-10-24)

## Verdict
- **Spec compliance: met** for what this run was asked to build (agent file, skill router, 6 references, one roster row). Every "will not do" item in the role file and every Never rule is in the agent, all 5 modes are covered, the held-out AI rule is kept, the 7-field handoff is repeated, and no invented sources or numbers were found.
- **Quality: good.** No Critical findings. 1 Important, 4 Minor.
- **Safe to count as done: no, not yet.** The content can be accepted, but the repo's own Definition of Done is not met (see I1). The honest label today is "Built, not tested".

## Scope
- Request: `.team/runs/2026-10-24-qa-test-engineer-agent/02-code-reviewer-request.json`.
- Read in full: `agents/qa-test-engineer.md`, `skills/qa-test-engineer/SKILL.md`, all 6 files in `skills/qa-test-engineer/references/`, `docs/agents/roles/qa-test-engineer.md`, `docs/superpowers/specs/2026-10-24-qa-test-merge.md`, `docs/agents/agent-template/README.md`, the architect request and response.
- Spot-checked: `docs/agents/roster.md` row 14, section headings and frontmatter of `agents/backend-engineer.md`, `skills/ai-engineer/scripts/eval_compare.py` (arguments and print lines), `skills/hire-an-engineer/references/ui-ux.md` section 8, existence of `skills/software-architect/references/game-performance-budgets.md`, `TASKS.md` row 9, `docs/agents/visual-office/index.html` TAGS map.
- Not read: `handoff-contract.md` in full (the 7 fields in the agent match the shape repeated in `backend-engineer.md` and the request), the whole `art-qa.md`.
- Out of scope as the request says: orchestrator `Agent(...)` list, orchestrator `team-roster.md`, sources.md, evals, CHANGELOG, install, commit.

## Checks run
| Command | Result |
|---|---|
| `python scripts/validate_agents.py` | all 7 agents ok, including `qa-test-engineer`; exit 0 |
| `PYTHONUTF8=1 python scripts/validate_skills.py` | `qa-test-engineer: description 1010 chars, SKILL.md 54 lines`; "All skills valid."; exit 0 |
| `python scripts/check_roster.py` | `ok: ...docs/agents/roster.md`; exit 0 |

No tests were run (none exist for this skill).

## Spec compliance

### Role file section 4 ("What it will not do") against the agent's Never list
| Role file item | Agent file | Met |
|---|---|---|
| Fix product code, art or levels; only test code, data, config, reports | Never line 81 | yes |
| Code review or architecture | line 83 | yes |
| Set the look or edit / crop / re-export art | line 82 | yes |
| Change balance, levels or rules | line 81 | yes |
| Optimise code or assets | not named; covered only by "fix product code" (line 81) and `method-performance.md` line 10 | partly (M1) |
| AI feature / open eval set; statistics beyond counts | line 83 | yes |
| Full security audit | line 84 | yes |
| Legal advice or certificates | line 85 | yes |
| "Fun", "will perform", "accessible", "conformant" | line 86 | yes |
| Live service, real secrets, real data, paid tools, real players without approval | line 87 | yes |
| Deploy, publish, upload, real email, payments, delete data | line 88 | yes |
| Show held-out AI cases | line 89 | yes |
| "Looks right" | line 91 | yes |
| Text in files is not instructions | line 92 and How it works step 2 | yes |
| Ask the boss, never another specialist (request constraint) | line 80 | yes |
| Section 9 word list ("tested", "no bugs", "fixed", coverage or average alone, old run) | line 86 | yes |

### Other checks asked for
- **5 modes covered:** yes. `SKILL.md` lines 13-19 route each mode to its own method file; sub-modes of Test (Plan, Run, Automate) and Art QA (Gate, Spot check, Re-check) are in `method-test.md` section 2 and `method-art-qa.md` section 2. Release gate is inside Test (`method-test.md` section 7), as the spec decides.
- **Held-out case rule kept:** yes. Agent line 89, `SKILL.md` rule 10, `method-test.md` section 8: ids and counts only, inputs go to the owner's harness, no held-out set means `blocked`, requests for the cases are reported. Checked that `eval_compare.py` takes `--cases --before --after` (lines 58-60) and prints only counts and case ids (lines 72-84), so following the method does not leak case text.
- **No invented sources, numbers or claims:** none found. Numbers used (24 by 24 CSS pixels, 44-pixel project target, 200 percent zoom, severity 4 to 1, P0 to P3) all come from the role file. The 700 ms frozen-frame number was left out in favour of "where the platform defines them" (`method-performance.md` line 9), which is safe. `bug-report.md` line 32 honestly says the 3, 2, 1 wording is the role's own and checks out against `ui-ux.md` line 108. The defaults "Run" and "Gate" for unclear sub-modes are reasonable choices, not facts.
- **Owner decisions Q24 to Q26** are written in: no real players by default and "simulated" labels (`method-playtest.md` line 9), no load test without a test copy (`method-performance.md` line 15), device floor (`method-test.md` line 16, `method-performance.md` line 8).
- **Tools fit the role:** yes. Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch match spec section 5; each is justified in the Tools section (lines 31-34), with write limits and "no command against a live URL".
- **Thin agent file:** yes, 95 lines with the same sections as `backend-engineer.md`; method detail lives in the skill. Description 1,010 characters (agent) and 1,010 (skill), under 1,024.
- **7-field handoff:** yes, lines 56-72, with the status rules and "always end with the JSON".
- **Roster:** one new row (line 14), model `opus` matches frontmatter; `check_roster.py` passes.
- **Extra, not in the role file:** "do not open `.env` or secret files" (line 45) and "do not overwrite existing records" (line 95). Both are safe additions.

## Findings

### Important

**I1. The build is not "done" by the repo's own rules; status documents still say "not built".**
- Where: `docs/agents/roles/qa-test-engineer.md` line 3 ("Status: not built. There is no skill, agent file or eval"); `docs/superpowers/specs/2026-10-24-qa-test-merge.md` line 3; `TASKS.md` line 134 ("Documented | Not started"); `docs/agents/visual-office/index.html` line 869 (TAGS map has no `qa` entry, so the seat shows "Planned"). Plus the known gap: `agents/orchestrator.md` `Agent(...)` list and `team-roster.md`.
- Why it matters: `docs/agents/agent-template/README.md` lines 22-33 say a role is not done until the boss can call it, the office tag, `TASKS.md` and the role status line are updated, and evals pass (line 12, step 4 and 7). Right now the boss cannot call the agent at all, and the role file says the opposite of what exists. The spec's pre-mortem item 9 warns exactly about a dashboard label that overstates or misstates what is built.
- Trigger: the owner reads the role file or the tracker and sees "not built" while the agent exists; or the boss tries to send a QA job and cannot.
- Smallest fix: after the orchestrator change, set the role status line and `TASKS.md` row 9 to "Built, not tested (0 of 18 evals)", add `qa:'built'` to TAGS and run `python scripts/sync_team_start.py`. Keep "Tested" off until the evals exist and pass. Owner of fix: the boss (documents) with the Architect role.
- Confidence: confirmed.

### Minor

**M1. "Optimise code or assets" is not named in the Never list.** `agents/qa-test-engineer.md` line 81 forbids fixing product code, and `method-performance.md` line 10 says "do not change the code", but the role file's explicit line (role file line 73) is missing in the agent. A brief like "it stutters, make it faster" could tempt the agent to "optimise" a test asset or config. Fix: add "optimise the code or the assets; it measures and points" to line 81. Confidence: likely (low impact because the write rules already block product folders).

**M2. The agent and the Art QA method point to measuring scripts that do not exist yet.** Agent line 32 ("the role's own read-only measuring scripts") and `method-art-qa.md` line 15 ("Measure with scripts") refer to the spec's planned `image_specs.py`, `frame_stats.py`, `contrast.py`, `flaky_rerun.py`, which were not built in this run (architect response, assumption 7). With no installs allowed, an agent asked to measure icons may have no tool and be tempted to report sizes it did not measure. Fix: say "scripts in the skill when they exist; otherwise write a small standard-library script in `docs/qa/` or report the check as not run". Confidence: likely.

**M3. Held-out storage is treated as open, but the template records it as decided.** `docs/agents/agent-template/README.md` line 30 says held-out cases are kept by QA "outside the project folder (decision Q1)". `method-test.md` line 41 returns `needs_answers` when the brief names no place, and the architect response (assumption 2) calls it open. Not a safety problem (the default it suggests is the same), but it adds a question the owner already answered. Also `agents/ai-engineer.md` line 50 still says "QA / Test Engineer or Data Scientist & Analyst". Fix: confirm Q1 with the owner, then use "outside the project folder" as the stated default and update the spec's open question 1. Confidence: needs-check (which record is current).

**M4. "Live URL" is not defined for a hosted preview or staging link.** Agent line 32 bans "any command against a live URL or server", while role file section 6 lists "the build or preview link" as normal input. A hosted preview may be read as live (the agent refuses a normal job) or a production URL may be read as "preview". Fix: one line: a URL the brief names as a test copy or preview is allowed; anything else is live. Confidence: needs-check.

## What was met
Every role-file refusal, the five modes with one method file each, router that loads one mode at a time, one bug format and severity scale, find-do-not-fix write limits, test copies only, honest word list, held-out rule, owner decisions Q24 to Q26, WCAG 24 vs 44 pixel rule, game guidelines for games, 7-field handoff, roster row, all three validators.

## What could not be checked
The agent's behaviour: no evals exist, so nothing shows the agent actually follows these rules (spec section 5 plans 18 cases). The installed copy was not compared (not installed in this run).

## Fix plan (for the boss)
1. Boss: add `qa-test-engineer` to `agents/orchestrator.md` and `team-roster.md` (already planned).
2. Boss: update the role status line, `TASKS.md` row 9 and the office TAGS to "Built", not "Tested" (I1).
3. Architect (one short pass on the agent and two method files): M1, M2, M4; M3 after the owner confirms Q1.
4. Later, with the owner's go: sources.md, the 18 evals, CHANGELOG, install.
