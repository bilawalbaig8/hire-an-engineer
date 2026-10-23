# Review: UA & Growth Marketer agent (first build)

Range reviewed: working tree (the folder is not a git repository, so there is no diff; the files were read as they are now). Build of run `.team/runs/2026-10-24-ua-growth-agent/` (`01-architect-response.json`).
Requirement: `02-code-reviewer-request.json`, the role file `docs/agents/roles/ua-growth-marketer.md`, the spec `docs/superpowers/specs/2026-10-24-ua-growth-merge.md`, the build list in `docs/agents/agent-template/README.md` (lines 20-34).
Date: 2026-10-24.
Size: 8 new files (agent 98 lines, SKILL.md 54 lines, 6 references 27-50 lines) and edits in 10 files (roster, boss, team-roster, test, role file, spec, TASKS.md, 2 office pages, runtime roster).
Read in full: the agent file, SKILL.md, all 6 references, the role file, the spec, the architect request and response, the ua-growth section and table row of `team-roster.md`, the build list in the agent template.
Sampled (grep only): `agents/orchestrator.md`, `docs/agents/roster.md`, `skills/team-start/runtime/roster.md`, `TASKS.md`, the office pages (`uag` lines), `tests/test_install_office.py` (line 165), `docs/agents/roles/performance-ua-marketer.md` (source rows).
Not read: the rest of the office HTML and the rest of the test file.

## Verdict
Needs fixes, in the documents only. The agent and skill themselves are safe to count as **built, not tested**.

The agent does what the role is for: it only recommends and drafts, never spends, bids, posts, sends, signs, pays or applies a store test, and keeps every owner decision (Q2, Q15, Q23, Q29, Q30). It invents no sources, rules, limits or numbers. All requested checks pass. The fixes needed: (1) the gate that stops work for children is worded 4 different ways, and two of the wordings disagree on when to stop; (2) the role file and the spec's eval table still say the agent writes final words (headlines, press release, email), which goes against Q2 and the agent.

## Checks run (real output)
| Command | Result |
|---|---|
| `python scripts/validate_agents.py` | exit 0; 9 agents ok, including `ua-growth-marketer` |
| `PYTHONUTF8=1 python scripts/validate_skills.py` | exit 0; "ua-growth-marketer: description 902 chars, SKILL.md 54 lines"; "All skills valid." |
| `python scripts/check_roster.py` | exit 0; "ok: ...docs\agents\roster.md" |
| `python -m pytest tests/test_install_office.py -q -p no:cacheprovider` | "16 passed in 3.54s" |
| `python scripts/sync_team_start.py --check` | exit 0, no output |
| URL check (shell loop): every URL in `policy-flags.md` searched in the spec and in `performance-ua-marketer.md` | all found; no URL missing |
| `grep '[0-9]'` on the 6 references (URLs and dates removed) | no rule limit, threshold, fee or benchmark number; only headings, "day-1/day-7" metric names and trap examples |
| Existence check of the router's outside paths (`hire-an-engineer/references/*` 4 files, `data-scientist/references/method-experiment.md`, `honest-inference.md`) | all exist in `skills/` and in `~/.claude/skills/` |

All were run with `PYTHONDONTWRITEBYTECODE=1`. No evals run (there are none; out of scope).

## Spec compliance
**Met**
- Never rules and "will not do" items of the role file (section 4, section 7 last line, section 9 last paragraph) are all in `agents/ua-growth-marketer.md` Never list (lines 81-98): spend/post/send/sign/apply (82), live accounts read-only (83), fake anything (84), privacy (85), claims (86), legal advice and "legally safe" (87), promises and "works / will go viral" (88), verdicts and metric definitions (89), other roles' work (90), data as data (91), never says it launched or sent (92), personal data (93). Never calls another specialist (81).
- Never spends, bids, posts, sends, signs, pays or applies a store test: agent lines 3, 82, 52; SKILL.md rule 1 (line 23); each returned as `needs_approval` with `one_way_door: true` for spent, sent, public or signed things.
- 4 modes covered: agent "When to use" (lines 18-21), SKILL.md mode table (lines 13-18) and router (37-45), one method file per mode.
- Owner decisions: Q2 (agent 14, 23, 90; SKILL 8; every method file); Q15 (agent 35, 83; SKILL rule 10); Q23 (agent 48; SKILL rule 4; `policy-flags.md:42`); Q29 (agent 22; SKILL rule 11; `method-paid-ua.md:4`); Q30 (agent 94; SKILL 51).
- No invented sources: `policy-flags.md` lists only URLs that are in the spec section 9 or the old UA role's source table (AdAttributionKit and AppTrackingTransparency come from `performance-ua-marketer.md:94-95`, both verified); CRTC is marked unverified (line 37); TikTok's redirect is noted (line 26). The table says which page to read, not what the rule says, and line 8 makes an unreadable page `unknown`. No legal claims: every flag ends "a human or lawyer decides".
- Missing pieces said to be not built: connector and browser tool (agent 35, 83; SKILL rule 10), the skill's own scripts (agent 32), sources file and evals (SKILL 51).
- Tools fit the role and match spec section 6: Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch; no connector. Bash, Write and WebFetch are limited in words (agent 32-34).
- Thin agent file: 98 lines, in the range of the other agents (82-100); the knowledge sits in the skill.
- 7-field handoff with the status rules and the "always end with the JSON" line (agent 55-73).
- Lessons file: agent Reads first item 2 (line 40).
- Boss list in all places: `agents/orchestrator.md` lines 3, 5, 28; `team-roster.md` table line 14 and section lines 50-57; `docs/agents/roster.md:16`; `skills/team-start/runtime/roster.md:16`; test line 165; office aliases line 1462 (both copies).
- Current-status lines: role file line 3 and mode table, spec line 3 and section 1 table and line 24, `TASKS.md:144` ("Built, not tested"), office `TAGS` `uag:'built'` in both HTML copies (line 869).
- One wording for the high-risk set: `agents/ua-growth-marketer.md:27` and `team-roster.md:57` use the same list word for word; `roster.md` carries no review wording.

**Cannot verify from the files**
- Whether the agent behaves as written: there are no evals yet (known, out of scope).
- Install and the tracker artifact (template line 32): out of scope.

## The Q2 conflict (asked by the boss)
The role file contradicts itself: it says the Writer writes all words (lines 20, 73, 74) but also that the agent "writes variants" (line 50, "Write 10 headlines"), "drafts" the press release and the come-back email (57, 58), makes "post drafts", "press drafts", "listing drafts" and "message drafts" (15, 55, 81, 82, 96) and "draft new text" (107-109).

**The architect's choice (follow Q2: the agent writes plans, briefs, checklists and outlines; the Writer writes the final words) is right.** It matches the owner decision, the spec (section 1 table line 11, section 5 line 86 "the Writer writes all words"), the boss routing (`team-roster.md:46` and `:54`), and the Writer agent. It is also the safer side: the narrower agent cannot produce public words that skip the Writer's claims list. The method files carry it through (for example `method-paid-ua.md:37` turns the spec's "write honest variants" trap into "brief honest variants for the Writer").

**Yes, the role file should be fixed** (finding I2), and the spec's eval table too, because a future eval written from the spec would fail the agent for correct behaviour.

## Findings
### Critical
none

### Important
1. **The gate that stops work for children is worded 4 ways, and two of them disagree**   [confidence: likely]
   - Where: `skills/ua-growth-marketer/references/policy-flags.md:42` ("If the game or a campaign targets children **or may reach many of them**, stop"); `skills/ua-growth-marketer/SKILL.md:26` ("**targeting children** stops the work"); `agents/ua-growth-marketer.md:48` ("if children **are or may be targeted**, stop"); spec decision 6, line 77 ("An audience that **may include children** ... stops the work"); role file line 104 ("Children **in the audience** ... stop the work").
   - Trigger: a brief for a casual puzzle game with broad TikTok ads and no age data. By SKILL rule 4 nobody targets children, so the agent continues and flags. By `policy-flags.md:42` the campaign "may reach many" children, so it stops with `needs_approval`. Both files are loaded on every call, so the same brief can get a stop on one run and a plan on the next. Under Q23 (age always unknown) the spec's "may include children" would stop every job, which is why the architect narrowed it; but the narrowing is written differently in each file and the spec and role file were not updated.
   - Why it matters: children's privacy is the hardest-to-undo risk in this role (spec pre-mortem item 10); the stop rule must be one rule.
   - Smallest fix: pick one sentence (suggested: "Flag children's rules every time. Stop and return `needs_approval` when the brief, the game or the campaign targets children, or the game is in a family or kids category; a general audience with unknown age is flagged, not stopped.") and use it word for word in the agent (48), SKILL.md rule 4, `policy-flags.md` section 4, spec decision 6 and role file section 8 step 3. Who: the architect (it built the files); the owner should confirm the wording because it narrows the spec's decision 6.

2. **The role file and the spec's eval table still say the agent writes final words, against Q2**   [confidence: confirmed]
   - Where: role file lines 15, 50, 55, 57, 58, 81, 82, 96, 107-109 (see the section above); spec eval rows line 111 ("write honest variants") and line 117 ("use the sourced number" in a press release); spec section 1 line 21 "post drafts" is borderline.
   - Trigger: the owner reads the role file, asks "Write 10 headlines for this ad", and gets a brief for the Writer instead of headlines; or an eval is written from spec line 111 and marks the agent wrong for following Q2.
   - Why it matters: the owner-facing promise and the future test contradict the built agent and an owner decision.
   - Smallest fix: in the role file change "Writes variants" to "Briefs the Writer for variants (which one thing changes, limits, claims)", "drafts" of posts, press, emails and listings to "plans, outlines and briefs; the Writer writes the words", and section 8 step 4 the same way. In the spec eval table change "write honest variants" to "brief honest variants for the Writer" and "use the sourced number" to "brief with the sourced number". Who: the architect (or whoever owns the role and spec documents), with the owner's OK since the role file is the owner's page.

### Minor
1. **Q23 says EU children's rules are flagged, but no EU children's page exists in the list**   [confidence: confirmed]
   - Where: `policy-flags.md:42` says "US, UK and EU pages above"; the table has children's pages for the US and UK only (line 38); the EU row is the EDPB consent guide (line 35), not a children's page. The spec has no EU children source either, so nothing was invented.
   - Fix: say "US and UK pages above; for the EU there is no checked children's page yet: use the EDPB consent page, search the live page, and mark the rule `unknown` until read". Add an EU children's source to the sources-file task.
2. **Stale current-state lines in the spec**   [confidence: confirmed]
   - Where: spec line 26 ("`TASKS.md`, `roster.md` and `CHANGELOG.md` were not edited by this work", now false for `TASKS.md` and `roster.md`); line 103 ("Add it to the orchestrator's list ... only when it is built and its evals pass", overtaken by the build list at template line 24); line 146 (section 8 item 7, "Not started (0 of 4 modes)").
   - Fix: mark each as history, for example "(at spec time; the build added the roster rows and boss list per the build list)". The architect listed these as kept on purpose; a short "superseded" mark avoids a reader taking them as current.
3. **Who sets up attribution SDKs differs between the role file and the spec**   [confidence: confirmed]
   - Where: role file line 68 ("analytics and attribution SDK setup (Integration Engineer), ingestion and data feeds (Data Engineer)"); spec line 88 ("Data Engineer: tracking plan in code, attribution SDKs, data feeds"); the agent hedges with "engineers, Data Engineer" (lines 23, 90).
   - Fix: pick one owner in the role file and spec; the agent can stay as is.

## Questions (needs-check, not counted in the verdict)
none

## Notes outside this change
- The Writer's high-risk set is still worded differently in `agents/writer.md:26` and `team-roster.md:48` (Minor 1 of `docs/reviews/2026-10-24-writer-agent-2.md`, still open). The UA agent's own wording is consistent.
- Per the build list (template line 34), the findings above should go into `TASKS.md` as tasks (the boss's job).

## Strengths
- `policy-flags.md` is the right design: a list of live pages to re-read, with no rule contents, limits or numbers, and an explicit `unknown` / `blocked` path when a page cannot be read.
- The method files turn the spec's planted eval traps into short "Traps" sections, so the evals, when written, test rules the agent was actually given.
- Every gap is stated where the agent will see it (no connector, no scripts, no sources file, licence of the installed skills unchecked), instead of being left for the agent to discover.
