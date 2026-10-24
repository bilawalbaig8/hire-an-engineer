# Review 2: Creative & Art Director agent (after fix round 1)

Range reviewed: working tree (the folder is not a git repository). Fix round 1 by the architect (`.team/runs/2026-10-24-creative-art-director-agent/03-architect-response.json`) against the first review `docs/reviews/2026-10-24-creative-art-director-agent.md`.
Requirement: the 2 Important and 4 Minor findings of the first review, plus the checks in `04-code-reviewer-request.json`.
Date: 2026-10-24
Read in full: `agents/creative-art-director.md` (103 lines), `skills/creative-art-director/SKILL.md` (54), `references/what-it-can-see.md` (32), `references/method-style.md` (39), `references/honest-ads-and-rights.md` (46), the first review, the architect response.
Read in part: role file `docs/agents/roles/creative-art-director.md` (lines 3, 16, 38-52, 57, 92, 124), spec `docs/superpowers/specs/2026-10-24-creative-art-director-design.md` (lines 3, 16, 18, 43, 47, 60, 107, 130, 143, 151, 154, 158, 165, 176, 179-181, 192), `skills/ua-growth-marketer/references/policy-flags.md` (section headings, section 4), `TASKS.md` (rows 9, 12, 13, 16, 19, 21, 27), the `agents/` folder listing.

## Verdict
**Approved** (0 Critical, 0 Important, 1 Minor new). All 6 earlier findings are fixed. Nothing broke: all five checks pass, and the shared sentences are still word for word the same.

## Earlier findings
| # | Finding | State | Evidence |
|---|---|---|---|
| I1 | Image size could be stated from just viewing a picture | **Fixed** | The new sentence "state an image size only when a tool or the file header really gave it ... opening or looking at an image is not measuring it; otherwise write `not measured`" is in exactly 3 places, identical: `agents/creative-art-director.md:31`, `SKILL.md:25`, `what-it-can-see.md:18` (`grep -rlF`). The old phrase "only from a file it opened" has 0 hits in `agents/`, `skills/`, `docs/` (outside reviews), `TASKS.md`. New `what-it-can-see.md:19` says a size script reads only the header, standard library, no network, reused. It now agrees with the Never line `agent:93`. |
| I2 | Role file and spec gave this role the variant table (Q3) | **Fixed** | Role file `:92` and spec `:47`: `docs/creative/ads/` holds "concept sets and hand-off notes only ... the variant table is the UA & Growth Marketer's, owner decision Q3". Spec `:158` template list has 7 items and says "no variant table"; spec `:3` and `:176` say 7 templates. `grep "ad variant table"`: 0 hits. Every other "variant table" mention (spec `:16`, `:43`, `:151`; role `:46`, `:124`; `method-ad-creative.md:9,15`; `SKILL.md:34`; `agent:22`; `team-roster.md:68`) gives the table to the UA & Growth Marketer or names it as a topic. No leftover conflict. |
| M1 | Q19 note hidden in a third table cell | **Fixed** | Role file `:49` now has 3 pipes (two cells), the same as the other rows (`:40` checked); it ends "(see the Q19 note below this table)". The note is a visible paragraph at `:51`, outside the table. |
| M2 | Contrast fallback had no known-answer check | **Fixed** | `method-style.md:19`: compare the script with the live W3C page, then white `#FFFFFF` on black `#000000` must give 21:1 and any colour on itself 1:1; command and output go in `evidence`; on a wrong answer fix and re-check or write `contrast not measured`. Both numbers are correct for the WCAG formula ((1.0 + 0.05) / (0.0 + 0.05) = 21; equal luminance gives 1). "No other expected number is written here; any threshold is read on the live page." Number scan of the agent and skill: the only ratios are these two (`method-style.md:19`, `agent:65`). Reuse of the existing script is at `:17`. |
| M3 | Stale current-state lines in the spec | **Fixed** | Spec `:18`, `:107` end with "(History, at spec time; superseded. Current state 2026-10-24: ...)"; `:192` is marked history with the status "Built, not tested (4 of 4 modes, no evals yet)". Neighbour statuses checked against reality: `agents/` holds `writer.md`, `ua-growth-marketer.md`, `qa-test-engineer.md`, `product-business-analyst.md` and no artist or project-manager file; `TASKS.md` rows 9, 16, 19, 21 say "Built, not tested", rows 13 and 27 "Not started". Correct. |
| M4 | Children's link led nowhere if the UA skill is not installed | **Fixed** | `honest-ads-and-rights.md:23`: "If the UA & Growth Marketer skill is installed, see ... section 4 ... If it is not installed, EU, UK and US children's rules are flagged as `unknown` and a lawyer decides." The target exists: `ua-growth-marketer/references/policy-flags.md` section 4 is at line 41. |

## Nothing else changed
There is no git history, so I checked by file times and content. Files changed after the first review (02:08): exactly the 7 the architect listed (agent, `SKILL.md`, `what-it-can-see.md`, `method-style.md`, `honest-ads-and-rights.md`, role file, spec). `critique.md`, `method-review.md`, `method-concept-brief.md`, `method-ad-creative.md`, `team-roster.md`, `docs/agents/roster.md` and `agents/orchestrator.md` are older than the first review. `TASKS.md` changed at 02:11 (not listed by the architect; row 12 still reads "Built, not tested", so I take it as the boss's tracker update). In the agent, the line count is still 103 and every line the first review cited (14, 22, 26, 34, 39, 46, 47, 55-71, 79-103) still holds the same text; the only changes are line 31 (the size sentence) and line 65 (the evidence example now names the 21:1 and 1:1 check), both asked for.

Shared sentences still identical (`grep -rlF` of the full sentence): children (agent, SKILL, honest-ads, team-roster, and the UA files), no image tool / Q19 (agent, SKILL, method-style, team-roster), Artist not built (agent, SKILL, team-roster), high-risk set (agent, SKILL, team-roster).

## Findings
### Critical
none

### Important
none

### Minor
1. **Owner-stated size is allowed by one rule but not named in the Never line**   [likely]
   - Where: `agents/creative-art-director.md:31` (and the same sentence in `SKILL.md:25`, `what-it-can-see.md:18`) allows a size from "an owner export that states the size"; `agents/creative-art-director.md:93` says never state a size "it did not measure with a tool it really ran".
   - Trigger: the owner writes "the icons were exported at the store size"; one rule lets the agent repeat the size, the other forbids it. The agent will likely choose the stricter one, so the harm is small.
   - Fix (architect, wording only): add to `agent:93` "or that the owner's export did not state (then say it is the owner's figure)", and label an owner-stated size as coming from the owner, not `verified`.

## Questions
none

## What I ran
All from the project folder, `PYTHONDONTWRITEBYTECODE=1`, no network, no writes besides this report.
- `python scripts/validate_agents.py`: exit 0, 11 agents with a check mark, including `creative-art-director`.
- `PYTHONUTF8=1 python scripts/validate_skills.py`: exit 0, "creative-art-director: description 944 chars, SKILL.md 54 lines", "All skills valid."
- `python scripts/check_roster.py`: exit 0, "ok: ...docs/agents/roster.md".
- `python -m pytest tests/test_install_office.py -q -p no:cacheprovider`: 16 passed in 3.44 s.
- `python scripts/sync_team_start.py --check`: exit 0, no output.
- `grep -rlF` of the size sentence and four other shared sentences; `grep` for "ad variant table", "8 templates", "only from a file it opened"; pipe count of role-file table rows; number scan for ratios, px, percent and NxN sizes; `stat` of file times.

## Not covered
- Agent behaviour (no evals; out of scope). Whether the Read tool shows PNG/JPG to this subagent (eval R1).
- Live W3C and policy pages (no network).
- sources.md, evals, scripts, templates, CHANGELOG, install, commit (out of scope by the request).
