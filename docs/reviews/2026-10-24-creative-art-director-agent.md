# Review: Creative & Art Director agent

Range reviewed: working tree (the folder is not a git repository), files written by the architect run `.team/runs/2026-10-24-creative-art-director-agent/01-architect-response.json`
Requirement: `docs/agents/roles/creative-art-director.md`, `docs/superpowers/specs/2026-10-24-creative-art-director-design.md`, the boss request `02-code-reviewer-request.json`
Date: 2026-10-24
Read in full: `agents/creative-art-director.md` (103 lines), `skills/creative-art-director/SKILL.md` (54 lines) and all 7 references (250 lines), the role file (157 lines), the spec (241 lines), the architect request, response and plan.
Read in part: `agents/orchestrator.md` (lines 3, 5, 28), `skills/orchestrator/references/team-roster.md` (line 15, lines 63-71), `docs/agents/roster.md` (line 17), `TASKS.md` (rows 12, 13), `tests/test_install_office.py` (line 165), `skills/team-start/runtime/ui/index.html` and `docs/agents/visual-office/index.html` (TAGS line), `skills/ua-growth-marketer/references/policy-flags.md` (sections 3-4), `docs/reviews/2026-10-24-ua-growth-agent-2.md` (headings and earlier findings).

## Verdict
**Needs fixes** (2 Important, 4 Minor, 0 Critical).

The label "built, not tested" is honest: the agent, the skill, the roster row and the boss lists exist and every check passes, and no file claims evals, scripts, templates or a connected image tool. Two things should be fixed in one short fix round first: the rules let the agent state an image size from just looking at a picture (an unmeasured number), and the role file and spec still give this role the ad variant table that the owner gave to the UA & Growth Marketer (Q3).

## Spec compliance
- **Met:**
  - All 16 "will not do" items of the role file (section 4) are in the agent's Never list (`agents/creative-art-director.md:79-103`), plus the section 9 last-paragraph rules (never "works", never "legally safe", never "safe to use" without licence, never "looks fine on phones", never "saw" what it did not open: lines 81, 87, 90-93).
  - Four modes: router `SKILL.md:12-20`, one method file each, mode list in the agent `:14`, `:18-21`.
  - Never makes or publishes art (`agent:80`, `SKILL.md:23`); never judges a file it did not open (`agent:46`, `:81`, `what-it-can-see.md`); never gives legal advice (`agent:90`, `honest-ads-and-rights.md:18`).
  - Owner decisions: Q19 (no tool connected, said "not built", credits budget per job later: `agent:34`, `SKILL.md:23`, `method-style.md:20`, `team-roster.md:65`); Q20 as the boss briefed it (Artist not built, boss routes hand-offs: `agent:22`, `SKILL.md:23`, `team-roster.md:65`); Q21 (guide read first, draft if none, kept up to date, change to an approved line is an approval: `SKILL.md:27`, `method-style.md:7-8,13`); Q22 (both lessons files in Reads first `agent:39`, `SKILL.md:33`); Q23 (UK/US/EU as background, age unknown, children flagged every time: `agent:47`, `SKILL.md:29`, `honest-ads-and-rights.md:21`).
  - Missing scripts, templates, sources and evals are said to be not built (`SKILL.md:25,51`, `agent:31`, `what-it-can-see.md:18-19`, `method-style.md:17`); the Artist is said to be not built.
  - No invented sources or numbers: all 15 URLs in the skill appear exactly in spec section 14 and each one is a `verified` row (checked by script, see "What I ran"). No platform size, safe-zone number, ratio threshold or legal claim is written; sizes and safe zones must be read live (`method-ad-creative.md:10`, `agent:100`).
  - Tools fit the role (Read, Grep, Glob, Bash limited to its own stdlib scripts, Write/Edit limited to `docs/creative/`, WebFetch/WebSearch for live pages); thin agent file (103 lines, UA 98, Writer 100); 7-field handoff repeated (`agent:55-71`).
  - Boss list names the agent in all places: `agents/orchestrator.md` lines 3, 5, 28; `team-roster.md:15` and section at `:63`; `docs/agents/roster.md:17`; runtime `roster.md` and `ui/index.html`; office TAGS `creative:'built'` in both HTML copies; test list `tests/test_install_office.py:165`.
  - Current-status lines say built, not tested: role file `:3`, `:9-14`; spec `:3`, `:154`; `TASKS.md:137`; agent `:14`; `SKILL.md:8`.
  - Shared sentences word for word the same (grep -F of the full sentence): children (agent 47, SKILL 29, honest-ads 21, team-roster 70; also the same as UA `policy-flags.md:42`), no image tool (agent 34, SKILL 23, method-style 20, team-roster 65), Artist not built (agent 22, SKILL 23, team-roster 65), high-risk set (agent 26, SKILL 35, team-roster 71), scripts not built (agent 31, SKILL 25).
- **Missing:** none in the agent; the variant-table line in the role file and spec is a conflict (Important 2).
- **Extra (not requested):** none. `docs/creative/scripts/` is used for the agent's own contrast script; the spec allows that folder (spec `:47`, `:152`).
- **Cannot verify from the change:** whether the Read tool really shows PNG/JPG files to this subagent (spec eval R1); how the agent behaves on the 18 eval traps (no evals, out of scope).

## Findings
### Critical
none

### Important
1. **Image size may be stated from just viewing a picture**   [confidence: likely]
   - Where: `agents/creative-art-director.md:31`, `skills/creative-art-director/SKILL.md:25`, `skills/creative-art-director/references/what-it-can-see.md:18`; in conflict with `agents/creative-art-director.md:93`.
   - What goes wrong: lines 31 / 25 / 18 say "give an image size only from a file it opened". Opening a PNG with the Read tool shows the picture to the model; it does not measure its width and height. Trigger: "Review these store icons, are they 1024 px?" The agent opens `icon-01.png`, and the rule allows it to write a size, labelled `verified` because the file was opened, that it only estimated by eye. Line 93 says the opposite ("State an image size ... it did not measure with a tool it really ran; write `not measured`"), so the two rules disagree.
   - Why it matters: an unmeasured number presented as checked is exactly what the role file forbids (section 9) and what this build was told to avoid ("no invented numbers"). Image sizes are also Art QA's to check.
   - Smallest fix (architect, wording only): in the shared sentence and in `what-it-can-see.md:18`, replace "from a file it opened" with "from a tool it really ran on the file (for example a small standard-library script that reads the PNG or JPG header, written and run like the contrast script) or from the owner's stated export settings; opening an image is not a measurement". Keep the sentence word for word the same in agent, SKILL and the reference.

2. **Role file and spec still give this role the ad variant table (conflicts with owner decision Q3)**   [confidence: confirmed]
   - Where: `docs/agents/roles/creative-art-director.md:90` ("`docs/creative/ads/` (ad concept sets, variant tables, hand-off notes) ... It is the only role that writes in these folders"); spec `docs/superpowers/specs/2026-10-24-creative-art-director-design.md:47` (same list) and `:158` (template "ad variant table"). Against: spec `:43` and `:151`, role file `:46` and `:122`, `method-ad-creative.md:15`, `agent:14,22`, `team-roster.md:68`, and the UA skill `method-paid-ua.md:11` (the UA builds the variant table).
   - What goes wrong: the role file says this role owns and alone writes variant tables, while the same file, the spec and the agent say the UA & Growth Marketer builds them. Trigger: whoever builds the 8 templates later follows spec `:158` and adds a variant-table template to this skill, or the boss reads role file `:90` and routes the table here; two roles then write the same document (pre-mortem item 8 in the spec).
   - Answer to the boss's question: yes, it is a real conflict that needs a fix. The agent itself is already correct, so the fix is in the two documents only.
   - Smallest fix (architect, wording only): role file `:90` and spec `:47`: "`docs/creative/ads/` (ad concept sets, hand-off notes; the variant table is the UA & Growth Marketer's, owner decision Q3)"; spec `:158`: drop "ad variant table" from the template list (7 templates) or rename it "what stays fixed and what may change" note; update the count "8 templates" at spec `:3`, `:176` and role file mentions if the count changes.

### Minor
1. **Q19 note sits in a hidden third table cell**   [confirmed]
   - Where: `docs/agents/roles/creative-art-director.md:49`. The row has three cells in a two-column table, so a Markdown viewer drops the "Changed by owner decision (Q19)" text. Fix: move the note inside the second cell. (Same row and `:57` say "never spends"; true today because no tool is connected, but they must change together with the four Q19 sentences when tools are connected.)
2. **Contrast fallback has no known-answer self-check**   [likely]
   - Where: `skills/creative-art-director/references/method-style.md:17`. The fallback is safe (standard library only, own folder, no network, command and output in `evidence`, otherwise "not measured") and honest in shape. But a freshly written script can carry a formula slip (for example the sRGB linearisation step) and still produce a "measured" ratio. Fix: before using it, run it on two pairs whose answer is fixed by the formula (white on black gives the maximum ratio, a colour on itself gives 1) and put that line in `evidence`; reuse the script already in `docs/creative/scripts/` instead of writing a new one each job.
3. **Stale current-state lines in the spec**   [confirmed]
   - Where: spec `:18` ("None of these is built") and `:107` ("None of the neighbour roles ... is built") although Writer, UA & Growth Marketer and QA / Test Engineer are now built; `:192` item 6 "Not built (0 of 4 modes)" is history but not marked. Fix: mark them "(history, at spec time; superseded)" with the current state, as was done for the UA spec.
4. **Children pages are a pointer into another skill**   [likely]
   - Where: `skills/creative-art-director/references/honest-ads-and-rights.md:23` points to `ua-growth-marketer/references/policy-flags.md` section 4. The spec install step is `--only creative-art-director` (spec `:165`); if the UA skill is not installed, the pointer leads nowhere. Fix: add "if that skill is not installed, mark the US and UK children's pages `unknown`", or copy the two checked URLs when `sources.md` is built.

## Questions
none

## Strengths
- The "not built" honesty is consistent everywhere: scripts, templates, sources, evals, image tool and the Artist are all named as missing, with a safe way to work without them.
- Shared rules are one sentence copied word for word across agent, skill and boss roster, including the children rule shared with the UA agent.
- Every URL in the skill is a verified row of spec section 14; no remembered platform sizes or legal claims.

## What I ran
All from the project folder, with `PYTHONDONTWRITEBYTECODE=1`, no network, no writes besides this report.
- `python scripts/validate_agents.py`: exit 0, 11 agents with a check mark, including `creative-art-director`.
- `PYTHONUTF8=1 python scripts/validate_skills.py`: exit 0, "creative-art-director: description 944 chars, SKILL.md 54 lines", "All skills valid."
- `python scripts/check_roster.py`: exit 0, "ok: ...docs/agents/roster.md". The expected product-business-analyst error did not appear: its roster row already exists (`docs/agents/roster.md:18`).
- `python -m pytest tests/test_install_office.py -q -p no:cacheprovider`: 16 passed in 3.51 s, exit 0.
- `python scripts/sync_team_start.py --check`: exit 0, no output.
- URL check (shell loop): every URL in `skills/creative-art-director/` and the agent file (15) found exactly in the spec; all 15 belong to `verified` rows (S14, S15, S16, S18, S19, S20, S27, S28, S29, S30, S31, S32, S33, S34, S35). No URL was opened (no network).
- Shared-sentence check: `grep -F` of five full sentences across agent, SKILL, references and `team-roster.md` (lines listed above).
- Number scan: no pixel sizes, ratios, percentages or second counts in the skill or agent.

## Not covered
- Agent behaviour (no evals exist; out of scope by the request).
- Whether the Read tool shows PNG/JPG to this subagent (eval R1).
- The live pages behind the URLs (no network); their content was not re-checked.
- CHANGELOG, THIRD_PARTY_NOTICES, install and commit (out of scope).
