# Review of role documents 1 to 4 (2026-10-24)

Scope: `docs/agents/roles/orchestrator.md`, `solution-architect.md`, `code-reviewer.md`, `ai-engineer.md`, and the specs `docs/superpowers/specs/2026-10-24-ai-engineer-ai-ops-merge.md` and `2026-10-24-ai-engineer-design.md`.

Method: every checkable claim was compared with the real file (map against territory). Counts of sources and evals were computed by script from `sources.md` and `evals.json`, not read from summaries. Then pre-mortem, inversion, red team, steel-man and Bayesian checks were applied to the status labels and plans. Only docs were edited; no skill, agent, eval or script was changed. Each edited doc has a "Review pass 2026-10-24" line at the bottom.

Result values: **ok** (matches the real file), **fixed** (the doc was wrong and was corrected), **open** (the owner must decide; see the list below).

## 1. Orchestrator (`docs/agents/roles/orchestrator.md`)

| # | Claim | Real file checked | Result |
|---|---|---|---|
| 1 | Agent file is `agents/orchestrator.md` | `agents/orchestrator.md` | ok |
| 2 | Skill is `skills/orchestrator/` | folder listing | ok |
| 3 | Version 0.1.0, unreleased | `CHANGELOG.md` orchestrator section | ok |
| 4 | 12 local eval cases | `evals/orchestrator/evals.json` (12 cases) | ok |
| 5 | All 12 pass after three fixes | only `CHANGELOG.md`; no results file in `evals/orchestrator/` | open (O5) |
| 6 | Start with `claude --agent orchestrator`; not a subagent | agent description, `SKILL.md` | ok |
| 7 | Answer has 7 fields | `SKILL.md`, `scripts/agent_contract.py` | ok |
| 8 | Tools: `Agent(architect, code-reviewer, ai-engineer, data-scientist)`, Read, Grep, Glob, Bash, Write, 2 office tools | agent frontmatter `tools:` | ok |
| 9 | Bash changes nothing in the project | `team_event.py` appends to `.agents/events.jsonl` | fixed |
| 10 | Write only in `.team/runs/` | agent file line 31 | ok |
| 11 | Office answer tools switched off for now | agent file line 58 | ok |
| 12 | Callable today: architect, code-reviewer, ai-engineer, data-scientist | agent frontmatter | ok |
| 13 | backend-engineer is in the roster but not in the boss's list | `docs/agents/roster.md`, agent frontmatter | ok (see O1) |
| 14 | "The roster says" to add the name to `Agent(...)` when installed | `roster.md` only says "add a row in the same commit that adds the agent file" | fixed |
| 15 | Caps: 8 calls, 2 fix rounds, 1 retry | `SKILL.md` rule 8, `failure-handling.md` | ok |
| 16 | At most 5 own questions at intake | `references/run-method.md` line 8 | ok |
| 17 | Run folder files (`plan.md`, request/response JSON, `decisions.md`, `summary.md`) | agent file, `run-method.md` | ok |
| 18 | 9 boss event names | `EVENT_TABLE` in `skills/orchestrator/scripts/team_event.py` | ok |
| 19 | Hook writes `agent_start`, `agent_stop`, `file_written` | `scripts/log_event.py` | ok |
| 20 | `team_event.py check-run` exists | `team_event.py` sub-command `check-run` | ok |
| 21 | Office address from `.agents/office.json` | agent file line 55 | ok |
| 22 | 7 method files named in section 10 | `skills/orchestrator/references/` | ok |
| 23 | Roster is mirrored in `references/team-roster.md` | `team-roster.md` table has no backend-engineer row | fixed |
| 24 | 59 sources, 58 verified, 1 unverified (S-ORC-16) | `skills/orchestrator/references/sources.md` (script count) | ok |
| 25 | ID ranges and counts per area (9 areas) | same file, per-ID statuses | ok |
| 26 | `agent_contract.py` exists | `scripts/agent_contract.py` | ok |
| 27 | The 10 sections exist | headings `## 1.` to `## 10.` | ok |
| 28 | Status "built and tested" | `TASKS.md` row 1 "Tested" | ok |
| 29 | Source count agrees with CHANGELOG | `CHANGELOG.md` says 58 sources (57 verified) | open (O2) |

## 2. Solution Architect (`docs/agents/roles/solution-architect.md`)

| # | Claim | Real file checked | Result |
|---|---|---|---|
| 1 | Agent file is `agents/architect.md` | file exists | ok |
| 2 | Skill `skills/software-architect/` with `references/data-design.md` | folder listing | ok |
| 3 | Two modes, System design and Data design | agent description | ok |
| 4 | Owns `docs/architecture/`, `docs/decisions/`, `docs/data/` | `roster.md` row architect | ok |
| 5 | Backend data dictionary lives in `docs/backend/` | `roster.md` row backend-engineer | ok |
| 6 | Neighbour role is the "Backend & Integration Engineer" | split spec `2026-10-24-backend-integration-split.md`, `TASKS.md` rows 6 and 6b, agent `backend-engineer` | fixed (now "Backend Engineer") |
| 7 | Own-skill files `database.md`, `engineering-discipline.md`, `engineering-principles.md`, `integrations.md`, `cost-management.md`, `tools-and-stack.md` | `skills/hire-an-engineer/references/` | ok |
| 8 | `database.md` section 2 suggests soft delete | `database.md` line 32 under "## 2." | ok |
| 9 | The role asks "undo or only history" before soft delete | `data-design.md` step 4 | ok |
| 10 | Base rules come from `hire-an-engineer` | `data-design.md` holds them inline; the base file is optional | ok |
| 11 | 201 sources, 200 verified, S-FND-23 unverified | `skills/software-architect/references/sources.md` (script count) | ok |
| 12 | ID ranges per area (10 areas) | same file | ok |
| 13 | Data design sources: 38, 36 verified, 2 unverified | the table in the doc itself has 40 rows, 38 verified, 2 unverified | fixed |
| 14 | The 2 unverified data sources are Sussman and GDPR | doc table | ok |
| 15 | Data design method is in `references/data-design.md` | file, steps 1 to 9 | ok |
| 16 | The skill can find the data design source list | `data-design.md` line 41 points to this role doc, which is not installed with the skill | open (O13) |
| 17 | Status line says built; no test claim | `TASKS.md` row 2 says "Tested"; data eval results show round 3 at 0 of 4 before the evals were relaxed | open (O3) |
| 18 | Statuses done, needs_answers, needs_approval, blocked | `agents/architect.md`, handoff contract | ok |
| 19 | The 10 sections exist | headings | ok |
| 20 | Source count agrees with CHANGELOG | `CHANGELOG.md` software-architect 0.1.0 says 123 sources (86 verified) | open (O2) |

## 3. Code Reviewer (`docs/agents/roles/code-reviewer.md`)

| # | Claim | Real file checked | Result |
|---|---|---|---|
| 1 | Agent `agents/code-reviewer.md`, model opus | frontmatter | ok |
| 2 | Skill `skills/code-reviewer/` | folder listing | ok |
| 3 | Version 0.1.0, not released | `CHANGELOG.md` | ok |
| 4 | Tools: Read, Grep, Glob, Bash, Write; no Edit, no web | frontmatter `tools:` | ok |
| 5 | Tests only through `run_tests_safe.py` (scratch copy, stripped environment, timeout, not a sandbox) | agent file line 30, `skills/code-reviewer/scripts/run_tests_safe.py` | ok |
| 6 | Never `git checkout`, `stash`, `reset` | agent file line 30 | ok |
| 7 | Report path `docs/reviews/YYYY-MM-DD-<topic>.md`, suffix `-2`, `-3` | `references/report-templates.md` line 7 | ok |
| 8 | Reviews AI-Ops release changes | `SKILL.md` router, `ai-written-code.md` section | ok |
| 9 | Reviews the architect's `docs/data/` plans | agent file line 37 | ok |
| 10 | "SKILL.md and 10 reference files" | 11 files in `references/` (10 method and lens files plus `sources.md`) and one script | fixed |
| 11 | Roster: model opus, owns `docs/reviews/` | `roster.md` | ok |
| 12 | 14 eval cases in 5 groups as listed | `evals/code-reviewer/evals.json` (14 ids) | ok |
| 13 | Ground-truth file and a check script | `shop-GROUND-TRUTH.md`, `verify-ground-truth.py` | ok |
| 14 | CHANGELOG says `review-tests` not run; no pass rate claimed | `CHANGELOG.md`; but `TASKS.md` 4.8 says 14 of 14 pass; no results file | fixed (note added), open (O4) |
| 15 | 87 sources, 81 verified, 6 unverified with the 6 IDs named | `skills/code-reviewer/references/sources.md` (script count) | ok |
| 16 | Count and status per area (12 areas) | same file | ok |
| 17 | `qa-test-engineer.md` and `security-reviewer.md` exist | `docs/agents/roles/` | ok |
| 18 | The 10 sections exist | headings | ok |
| 19 | Status "built and tested" | `TASKS.md` row 3 "Tested"; no saved results | open (O4) |

## 4. AI Engineer (`docs/agents/roles/ai-engineer.md`)

| # | Claim | Real file checked | Result |
|---|---|---|---|
| 1 | 5 modes exist | `skills/ai-engineer/SKILL.md` router, agent description | ok |
| 2 | Design/Build and Train/Evaluate: 13 of 14 pass, one run each | `evals/ai-engineer/results-rerun-after-aiops.md` | ok |
| 3 | AI-Ops: 9 of 9 pass, one run each, 2026-10-23 | only `CHANGELOG.md`; no AI-Ops results file | open (O6) |
| 4 | "It has no keys and no network" | agent `tools:` includes WebFetch and WebSearch (official docs only) | fixed |
| 5 | Owns `docs/ai/` and `docs/ai/ops/` | agent file, `roster.md` | ok |
| 6 | Held-out set kept by QA / Test Engineer or Data Scientist & Analyst | `method-release-check.md`, `qa-test-engineer.md`, `data-scientist.md` agree; QA is not installed | open (O7) |
| 7 | Offline runner compares open and held-out sets | `skills/ai-engineer/scripts/eval_compare.py` | ok |
| 8 | Monitor never wakes itself | agent file step 7, `SKILL.md` rule 11 | ok |
| 9 | Validation rules "kept in one shared reference when the skills are built" | both skills built; no shared reference exists | fixed (open O11 for the build) |
| 10 | Neighbour "Backend & Integration Engineer" | split spec, `TASKS.md` | fixed |
| 11 | 9 own-skill files named as base | `sources.md` cites 7 (S-OWN-1 to 7); `versioning-release.md` and `engineering-discipline.md` are not cited | fixed (note added) |
| 12 | 100 outside sources, 98 verified, 2 unverified (OpenAI agents guide, GDPR) | `sources.md` (S-LLM-16, S-GOV-7 unverified) | ok |
| 13 | 40 AI-Ops sources, all verified | `sources.md` S-AIO-1 to 40 | ok |
| 14 | 17 of 20 passed is about 62 to 97 percent | exact binomial interval for 17/20 is about 0.62 to 0.97 | ok |
| 15 | "Limit of this backing" text | a sentence was repeated | fixed |
| 16 | Release results may get a second look from the Code Reviewer | `code-reviewer.md` section 2, `ai-written-code.md` | ok |
| 17 | The 10 sections exist | headings | ok |
| 18 | Status: all 5 modes built | `TASKS.md` row 4 "Tested", AI-1 to AI-4 done | ok |
| 19 | No secret or risky instruction in the doc | pattern scan for keys and passwords; read of section 4 | ok |
| 20 | One-off failing case is named | results file: `hiring-screening-legal` partial, not rerun | open (O12) |

## 5. Spec `2026-10-24-ai-engineer-ai-ops-merge.md`

| # | Claim | Real file checked | Result |
|---|---|---|---|
| 1 | Built 2026-10-23, AI-Ops evals 9 of 9 | `CHANGELOG.md` ai-engineer | ok (evidence O6) |
| 2 | Table: AI-Ops modes "planned" | modes are built | fixed |
| 3 | Agent tools list | agent frontmatter | ok |
| 4 | Decision 1 "Tested (2 of 5 modes)" | `TASKS.md` row 4 "Tested"; role doc says all 5 built | fixed (marked superseded) |
| 5 | Decision 3 "no network" | agent tools include WebFetch, WebSearch | fixed |
| 6 | New references `method-release-check.md`, `method-monitor.md`, `method-investigate.md` | `skills/ai-engineer/references/` | ok |
| 7 | A prompt-register template | register table in `method-release-check.md` | ok |
| 8 | Router loads AI-Ops references only in AI-Ops modes | `SKILL.md` lines 39 to 41 | ok |
| 9 | Stdlib eval runner | `scripts/eval_compare.py` | ok |
| 10 | Shared validation reference not done | no such file | ok |
| 11 | 9 AI-Ops eval cases as named | `evals/ai-engineer/evals.json` ids 15 to 23 | ok |
| 12 | Check step `check_merge` | no `check_merge` script in `scripts/` (also named in 3 other specs) | fixed (note), open (O8) |
| 13 | Open questions have defaults | section 6, all three have defaults; Q1 default (QA) is not installed | open (O7) |
| 14 | Date 2026-10-24, build 2026-10-23 | machine clock and results files say 2026-10-23 | open (O9) |

## 6. Spec `2026-10-24-ai-engineer-design.md`

| # | Claim | Real file checked | Result |
|---|---|---|---|
| 1 | Status "DRAFT, nothing installed or committed" | `TASKS.md` AI-1 to AI-4 done | fixed |
| 2 | Role file is in Roman Urdu | role doc is in English | fixed |
| 3 | Branch `feat/specialized-agents` | `git rev-parse` | ok |
| 4 | Reference list in section 8 | `skills/ai-engineer/references/` | ok |
| 5 | 100 sources plus 7 own files (S-OWN) | `sources.md` | ok |
| 6 | 14 evals, `setup-fixtures.py`, `GROUND-TRUTH.md` | `evals/ai-engineer/` | ok |
| 7 | Model opus, tools list | agent frontmatter | ok |
| 8 | "Two modes only" | superseded by the merge spec; the status line now points there | ok (with new status) |
| 9 | Section 9 written in Roman Urdu | owner rule: documents in simple English | open (O10) |
| 10 | No secret or risky instruction | pattern scan, read | ok |

## Counts

- Claims checked: 112 (Orchestrator 29, Solution Architect 20, Code Reviewer 19, AI Engineer 20, AI-Ops merge spec 14, AI Engineer design spec 10).
- Fixed in the docs: 18 (Orchestrator 3, Solution Architect 2, Code Reviewer 2, AI Engineer 5, merge spec 4, design spec 2).
- Open (owner decides): 13 findings, O1 to O13 below.
- Nothing in these docs was found to contain a secret or an instruction that is risky to follow. The red-team pass found no finding with a concrete attack path.

## Open findings for the owner

Each has a suggested default. Nothing here was changed.

- **O1. Boss cannot call the backend-engineer.** `roster.md` calls itself "the single list of specialists the Orchestrator may call" and has a backend-engineer row, but `agents/orchestrator.md` `Agent(...)` and `references/team-roster.md` do not include it. Default: add it to both after the Backend Engineer has its first evals (it is "Built, not tested" today).
- **O2. CHANGELOG counts are old.** Orchestrator: 58 sources (57 verified), real 59 (58). software-architect 0.1.0: 123 sources (86 verified), real 201 (200). There are also two `## software-architect` headings. Default: update the CHANGELOG lines in the next commit.
- **O3. Solution Architect "Tested" is weakly backed for Data design.** Saved results: round 1 1 of 10, round 2 5 of 10, round 3 0 of 4 reruns. After that, cases 01, 02 and 07 were relaxed to accept the output they already gave, and case 08 got an instruction fix, with no saved rerun. The 15 system design cases have no saved results file at all. Bayesian view: changing the test to fit the output is weak evidence that the role meets the original bar. Default: rerun data-01, 02, 07 and 08 once, save `results-data-round4-*.md`, and until then show "Tested (system design), Data design partly tested".
- **O4. Code Reviewer pass rate disagrees.** `TASKS.md` 4.8 says 14 of 14 pass; the CHANGELOG says `review-tests` was not run; no results file exists. Default: rerun the 14 cases once and save a results file.
- **O5. Orchestrator 12 of 12 has no results file.** Only the CHANGELOG records it. Default: keep the label, save results on the next run.
- **O6. AI-Ops 9 of 9 has no results file.** Only the CHANGELOG records it. Default: same as O5.
- **O7. Nobody installed can keep the held-out set today.** The default keeper is the QA / Test Engineer (not built). The Data Scientist may keep it "if you choose it". Without a keeper every Release check is `blocked`. Default: the Data Scientist keeps the held-out cases until QA is built.
- **O8. `check_merge` does not exist.** It is a build step in the AI-Ops merge spec and in the DevOps, UA & Growth and Writer merge specs. Default: drop it from those plans, or write it as a separate task (scripts were out of scope here).
- **O9. Dates.** The specs and several docs say 2026-10-24, while the machine clock and the results files say 2026-10-23. Default: leave as is; use the `date` command for new files.
- **O10. Roman Urdu in a spec.** Section 9 of the AI Engineer design spec is in Roman Urdu; the owner rule says documents are in simple English. Default: translate it in a later pass (not a rewrite now).
- **O11. Shared validation reference not built.** AI Engineer and Data Scientist each hold their own copy of "baseline first, time-aware split, leakage". Pre-mortem: the copies drift and give different answers on the same model. Default: build the shared reference the next time either skill changes.
- **O12. `hiring-screening-legal` is still partial.** Health and children are not named among the details that must not drive a hiring decision; not rerun. Default: rerun once now that the agent must read the skill first.
- **O13. The architect's data sources live in a doc, not in the skill.** `data-design.md` tells the agent to cite "the data design list in `docs/agents/roles/solution-architect.md`". A user install copies the skill, not that doc, so in another project the agent cannot find the 40 data sources. Default: copy the 40 data design sources into `skills/software-architect/references/sources.md` with IDs.

## Verdicts

| Role | Verdict | Why |
|---|---|---|
| 1 Orchestrator | sound with fixes | All tools, caps, events, files and source counts match; three wording errors fixed; the backend-engineer gap (O1) and the missing results file (O5) are open. |
| 2 Solution Architect | sound with fixes | Files, ownership and system design sources match; a wrong source count and a stale role name fixed. The "Tested" label for Data design rests on relaxed evals with no saved rerun (O3), and the data sources are outside the skill (O13). |
| 3 Code Reviewer | sound with fixes | Tools, safety rules, eval cases and sources match; a file count fixed. The pass rate is not backed by a saved result and two files disagree (O4). |
| 4 AI Engineer | sound with fixes | Modes, evals for Design/Build and Train/Evaluate, owned folders and 147 sources match; the "no network" claim, stale role name, shared-reference wording and both stale spec statuses fixed. The held-out keeper (O7) and the AI-Ops results file (O6) are open. |
