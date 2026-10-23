# Review: Writer agent (built, not tested)

Range reviewed: uncommitted working tree of the Writer build (run `.team/runs/2026-10-24-writer-agent/`)     Requirement: `docs/agents/roles/writer.md`, `docs/superpowers/specs/2026-10-24-writer-merge.md`, the boss request `02-code-reviewer-request.json` and the build brief `01-architect-request.json`, `docs/agents/agent-template/README.md`
Date: 2026-10-24     Size: 8 new files (`agents/writer.md` 100 lines, `skills/writer/SKILL.md` 53 lines, 6 reference files 212 lines) and 10 modified files (`git diff --stat`: +83 / -15; 50 of the TASKS.md lines are earlier uncommitted work, not this build; the Writer change there is row 16 only)
Read in full: `agents/writer.md`, `skills/writer/SKILL.md`, all 6 files in `skills/writer/references/`, `docs/agents/roles/writer.md`, the spec, both run files, the template README section "Also part of every build", the diffs of `agents/orchestrator.md`, `TASKS.md`, the spec and the role file, the writer section of `skills/orchestrator/references/team-roster.md`.     Sampled: the writer rows in both rosters, the `TAGS` line and writer aliases in the office HTML, line 165 of `tests/test_install_office.py`.

## Verdict
Needs fixes (small, documents only).

The agent and skill are good: every "will not do" item of the role file is a Never rule in the agent, the 4 modes each have a method file, the five owner decisions are kept, no source, number or store rule is invented, and the missing tools are said to be not built. All checks pass. Two things keep it from "approved": the spec still says "not built" in two places next to the new "built" line, and the agent does not read its lessons file, which the template makes part of every build. Both are one-line fixes. Counting the Writer as "built, not tested" is fair once they are fixed.

## Spec compliance
- Met:
  - Thin agent file (100 lines; others are 73 to 99), model `sonnet`, tools Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch as in spec section 5; Bash limited to read-only commands; Write and Edit limited to `docs/writing/`, `README.md`, `docs/guides/`, release notes, `CHANGELOG.md` only when named (`agents/writer.md:28-34`).
  - Every item of role section 4 "What it will not do" (lines 63-75) and the "never says" line 129 is in the agent Never list (`agents/writer.md:80-93`); the spec section 5 Never list is covered too.
  - 4 modes: router in `skills/writer/SKILL.md:12-20` and one method file each (content, script-storyboard, technical-docs, support), plus two shared files.
  - Owner decisions: Q31 English only (`agents/writer.md:14,75,94`, SKILL rule 6); Q32 no written policy, point to the store route (`agents/writer.md:81`, SKILL rule 2, `method-support.md:17-19`); Q33 owner approves claims, legal-sensitive to a lawyer (SKILL rule 3, `claims-and-sources.md:16`, agent `:22,84`); Q15 live accounts read-only on request, tool not built (`agents/writer.md:34,87`, SKILL rule 12, `method-support.md:33`); Q2 the Writer writes words, UA chooses keywords, tests, spend (`agents/writer.md:90`, `method-content.md:20`).
  - No invented sources, numbers, store rules or legal claims: the only outside facts (Apple and Google Play refund routes, the UK one-month limit for data requests) match spec rows 29-31 (verified), are dated "last check 2026-10-23" and say to re-read the live page (`method-support.md:18,22`). No source IDs are cited; SKILL.md line 50 says there is no sources list and no evals.
  - Not-built items are named: checker script (`agents/writer.md:31`, `method-technical-docs.md:33`), live helpdesk tool (`agents/writer.md:34`), evals and sources.md (SKILL.md:50, role file line 3).
  - 7-field handoff repeated in the agent with the status rules (`agents/writer.md:53-71`).
  - Boss list: `writer` in all three places of `agents/orchestrator.md` (lines 3, 5, 28), in `skills/orchestrator/references/team-roster.md:13` with a writer section (42-47), in `docs/agents/roster.md:15` and the runtime copy `skills/team-start/runtime/roster.md:15`, in the test list (`tests/test_install_office.py:165`).
  - Status lines: role file line 3, spec line 5 and the state table (lines 12-17), `TASKS.md` row 16 ("Documented | Built, not tested"), office `TAGS` `writer:'built'` (`docs/agents/visual-office/index.html:869`, runtime copy identical).
- Missing: the lessons file in the reading list (Important 2); stale "not built" text left in the spec (Important 1).
- Extra (not requested): none. `TASKS.md` carries 50 other uncommitted lines (row 9, rows 27-28, phases, fix list) from earlier work; not part of this build, but they will go into the same commit unless split.
- Cannot verify from the change: whether the agent behaves as written (no evals; out of scope by the brief); the installed copy (no install, by the brief).

## Findings
### Critical
none

### Important
1. The spec still says "not built" next to the new "built" status   [confidence: confirmed]
   - Where: `docs/superpowers/specs/2026-10-24-writer-merge.md:5` (the same status line ends "is now 'Documented', build 'Not started'"), `:67` (section 4 "Decisions (what the role document now says)", item 1: `Honest status. "Not built (0 of 4 modes)"`), `:78` (heading "Build plan (later; not started, needs the owner's go)").
   - What goes wrong: a reader of the spec gets two statuses in the same file, one of them in the status line itself. The brief asked that the spec status, including its labels, say built, not tested. This is the spec's own pre-mortem point 10 (a status misread).
   - Why it matters: status honesty is the main thing this review was asked to check; the dashboard and later briefs read these lines.
   - Smallest fix: in line 5 change "build 'Not started'" to "build 'Built, not tested'"; in line 67 change the label to "Built, not tested (4 of 4 modes, no evals yet)"; in line 78 change the heading to say steps 1 to 4 and part of 7 are done, evals, sources.md, install and CHANGELOG are not. Line 126 (section 7, calls made) can stay, as a record of the call at the time. Who: the Architect or whoever owns the spec.
2. The agent does not read its lessons file   [confidence: confirmed]
   - Where: `agents/writer.md:36-40` (Reads first); rule in `docs/agents/agent-template/README.md:29` ("Add `docs/lessons/<role>.md` to the role's reading list"); the QA agent does it (`agents/qa-test-engineer.md:41`).
   - What goes wrong: the owner reports a problem with a Writer draft, the boss writes `docs/lessons/writer.md` (decision X2), and the Writer never reads it, so the same mistake comes back.
   - Why it matters: the template says a role is not done until each "part of every build" line is done.
   - Smallest fix: in Reads first item 2 add "`docs/lessons/writer.md` if it exists". Who: the engineer who built the agent.

### Minor
1. Skill description has 4 characters of room   [confidence: confirmed]
   - Where: `skills/writer/SKILL.md:3` (1,020 of 1,024 characters, from `validate_skills.py`).
   - What goes wrong: adding the parked Localise mode, or any word, breaks the validator. The template asks for "room for the modes the spec plans". The same issue is already open for the Backend agent (TASKS.md F1).
   - Smallest fix: cut the example phrases ("Use for ...") to bring it near 900. Add it to the fix list if not done now.
2. Role file still uses the old mark "machine draft"   [confidence: confirmed]
   - Where: `docs/agents/roles/writer.md:124` ("`machine draft` or `approved`"), left over from the removed Localise mode; the agent uses `draft` or `approved` (`agents/writer.md:69`).
   - Smallest fix: change to "`draft` or `approved`". Not changed by this build; the brief allowed only the status line.
3. High-risk copy is routed to the code-reviewer   [confidence: confirmed]
   - Where: `skills/orchestrator/references/team-roster.md:47` (an assumption of the builder, listed in `01-architect-response.json`).
   - What goes wrong: legal-sensitive claims and refund reply sets are copy, not code; the code-reviewer's skill has no lens for advertising claims or refund wording, so its check may look stronger than it is.
   - Smallest fix: keep it, but say in that line that the code-reviewer checks the claims list against the sources and the Never rules only, and that the lawyer check (Q33) is still separate. Owner may decide later; easy to change.

## Other checks asked for
- Spec line endings: Git stores the spec with LF in the index and the working copy is LF (`git ls-files --eol`: `i/lf w/lf`), `core.autocrlf=true`. `git diff --stat` shows 12 changed lines (+6 / -6) for the spec, so the line-ending change does not make the diff larger and does not matter. Git warns it will turn LF into CRLF in the working copy next time it touches the file; that is normal on this machine.
- Thin agent: yes; the knowledge sits in the skill, the agent holds role, tools, how it works, handoff and Never.
- Tools fit the role: yes; same list as other specialists; Bash and network use are limited in words (no technical guard, same as the other sonnet specialists).
- Instructions in data: covered in the agent (`:46,88`), SKILL rule 5, `claims-and-sources.md` section 6, `method-support.md:8`.
- No text in the change is aimed at the reviewer.

## Strengths
- The Never list is a near line-for-line copy of the role file, so nothing was lost in the move.
- Facts that change (refund routes, data deadline) are dated and come with "re-read the live page", and "not built" is said wherever a tool is missing.
- Method files load per mode, as the spec asked, so a support call does not carry the storyboard rules.

## What I ran
All from the project root, on the working tree, with `PYTHONDONTWRITEBYTECODE=1`. The tests write only to pytest `tmp_path`; the sync script was run in `--check` mode only.
- `python scripts/validate_agents.py`: 8 agents ok, including `writer`; exit 0.
- `PYTHONUTF8=1 python scripts/validate_skills.py`: `writer: description 1020 chars, SKILL.md 53 lines`, "All skills valid."; exit 0.
- `python scripts/check_roster.py`: `ok: ...docs\agents\roster.md`; exit 0.
- `python -m pytest tests/test_install_office.py -q -p no:cacheprovider`: `16 passed in 3.51s`.
- `python scripts/sync_team_start.py --check`: exit 0, no output.
- `cmp` of the two office `index.html` copies: identical. `git diff --stat` and `git ls-files --eol` as above.

## Not covered
- No evals, no `sources.md`, no checker script, no CHANGELOG, no install and no commit (out of scope by the brief); the agent's behaviour is untested.
- The 50 unrelated uncommitted lines in `TASKS.md` and the untracked `agents/qa-test-engineer.md` were not reviewed here.
- `docs/agents/roles/storyboard-scriptwriter.md` was not compared in full with `method-script-storyboard.md`; only the steps, traps and the folder change were checked.
- This file lands in the working tree and may be committed with the change.
