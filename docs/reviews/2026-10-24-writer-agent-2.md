# Review 2: Writer agent after fix round 1

Range reviewed: uncommitted working tree, fix round 1 of run `.team/runs/2026-10-24-writer-agent/` (`03-architect-response.json`) plus the boss edit to `skills/orchestrator/references/team-roster.md:47`     Requirement: the 5 findings of `docs/reviews/2026-10-24-writer-agent.md`, the boss request `04-code-reviewer-request.json`
Date: 2026-10-24     Size: 4 files changed by the fix round (spec, agent, skill, role file) and 1 line changed by the boss (roster line 47)
Read in full: the earlier review, `03-architect-response.json`, the spec status lines and headings (lines 5, 17, 66-78, 124-128), `agents/writer.md` sections Model, Reads first and the section list, `skills/writer/SKILL.md` lines 1-22, the writer section of `team-roster.md` (lines 42-47), `git diff` of the role file and the spec.     Sampled: `TASKS.md` writer rows (141, 197).

## Verdict
Approved. Nothing important left.

All 2 Important and 3 Minor findings of the first review are fixed, with file evidence below. All requested checks pass. One new Minor note: the agent and the roster describe the high-risk review set in slightly different words. It is not blocking.

## Earlier findings: status
| # | Finding | Status | Evidence |
|---|---|---|---|
| I1 | Spec still says "not built" | Fixed | Spec line 5 now starts "Status: Built, not tested" and ends with build "Built, not tested"; line 17 and line 67 say "Built, not tested (4 of 4 modes, no evals yet)"; the section 5 heading (line 78) says "built 2026-10-24: steps 1 to 4 and part of 7; not done: `sources.md`, separate template files, evals, install, CHANGELOG". The 4 mode rows in the section 1 table now say "built, not tested". Line 126 (section 7, "calls made") keeps "Not built (0 of 4 modes)" as a record of the call at the time, as the first review allowed. |
| I2 | Agent does not read its lessons file | Fixed | `agents/writer.md:39`, Reads first item 2: "`docs/lessons/writer.md` if it exists". |
| M1 | Skill description had 4 characters of room | Fixed | `validate_skills.py`: "writer: description 864 chars" (was 1020); 160 characters of room. |
| M2 | Role file used "machine draft" | Fixed | `docs/agents/roles/writer.md:124` now reads "`draft` or `approved`"; no "machine draft" left in the file. |
| M3 | High-risk copy routed to the code-reviewer | Fixed | `agents/writer.md:26`: the review "checks wording only ... It is not a claims or legal check: the owner approves claims and anything legal-sensitive goes to a lawyer (owner decision Q33)". `team-roster.md:47`: "for wording only before the owner sees it (the owner approves claims, a lawyer the legal-sensitive ones; the reviewer never counts as that approval)". |

## Other checks asked for
- **Roster line 47 (boss edit):** says what was asked: the reviewer is for wording only and the owner approves claims, a lawyer the legal-sensitive ones; it adds that the reviewer never counts as that approval. It agrees with the agent and with Q33.
- **Skill description still triggers on the 4 modes:** yes. `skills/writer/SKILL.md:3` names all 4 modes with their key nouns (Content: store pages, ad copy, social and launch posts, email and landing-page text; Script and storyboard: video ad and trailer scripts, hooks, shot lists, voice-over, captions, playable-ad flows; Technical docs: README, user guides, setup and troubleshooting pages, release notes; Support: FAQ, canned replies, help articles, escalation list, ticket theme counts). The "Use for ..." example phrases were removed, so very short requests may match a little less often; this cannot be checked without evals (out of scope).
- **Nothing broke:** the role file diff is only the status line and the "draft" word; the spec diff is only status text (8 lines changed); the agent keeps all its sections (Role, When to use, Model, Tools, Reads first, How it works, Handoff, Language, Never) at 100 lines; the SKILL.md router table is unchanged at 53 lines.

## Findings
### Critical
none

### Important
none

### Minor
1. The high-risk set is described in two slightly different ways   [confidence: confirmed]
   - Where: `agents/writer.md:26` ("The boss **may** send a high-risk set (ad claims, store copy, a set of refund or data-request replies)") and `skills/orchestrator/references/team-roster.md:47` ("for a high-risk set (legal-sensitive claims, refund or data-request replies) **send** the result").
   - What goes wrong: the boss reads "send" for legal-sensitive claims only; the agent expects ordinary ad claims and store copy may go too. Both say the review is wording only, so no approval is lost; only which drafts get the extra read is unclear.
   - Smallest fix: use the same list in both lines (for example "ad claims, store copy, refund or data-request replies") and the same word ("send"). Who: whoever owns the roster and the agent; can wait for the next touch.

## Strengths
- The status fix went past the three lines named: the section 1 mode table and the dashboard label (line 17) were updated too, and the history line was kept on purpose.
- The wording-only rule is in both the agent and the boss roster, and both say the review is not the owner's or the lawyer's approval.
- The description cut (1020 to 864) kept every mode name and its main nouns.

## What I ran
All from the project root, on the working tree, with `PYTHONDONTWRITEBYTECODE=1`. Tests write only to pytest `tmp_path`; the sync script ran in `--check` mode only.
- `python scripts/validate_agents.py`: 8 agents ok (ai-engineer, architect, backend-engineer, code-reviewer, data-scientist, orchestrator, qa-test-engineer, writer); exit 0.
- `PYTHONUTF8=1 python scripts/validate_skills.py`: "writer: description 864 chars, SKILL.md 53 lines", "All skills valid."; exit 0.
- `python scripts/check_roster.py`: "ok: ...\docs\agents\roster.md"; exit 0.
- `python -m pytest tests/test_install_office.py -q -p no:cacheprovider`: "16 passed in 4.26s".
- `python scripts/sync_team_start.py --check`: exit 0, no output.
- `cmp` of `docs/agents/visual-office/index.html` and `skills/team-start/runtime/ui/index.html`: identical.
- `grep` of the spec for "Not started", "Not built (0", "Built, not tested"; `grep` of the role file for "machine draft" (none); `git diff` of the role file and spec.

## Not covered
- Known and out of scope by the brief: no `sources.md`, no evals, no checker script, no CHANGELOG, no install, no commit. The agent's behaviour is untested.
- The rest of `agents/writer.md` and the 6 reference files were not re-read line by line; they were read in full in the first review and the fix round did not name them as changed (the agent file is untracked, so there is no diff to confirm this; the section list and line count are the same).
- The other uncommitted files in the working tree (other roles, specs, TASKS.md lines for other work) are not part of this review.
- This file lands in the working tree and may be committed with the change.
