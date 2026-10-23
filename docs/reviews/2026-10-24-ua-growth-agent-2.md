# Review 2: UA & Growth Marketer agent (after fix round 1)

Range reviewed: working tree (the folder is not a git repository, so there is no diff; files were read as they are now).
Requirement: `.team/runs/2026-10-24-ua-growth-agent/04-code-reviewer-request.json`; the findings of `docs/reviews/2026-10-24-ua-growth-agent.md`; the fix report `03-architect-response.json`; `decisions.md`.
Date: 2026-10-24.
Read: the fix report and decisions; every line with "children", "draft", "SDK" or "high-risk" in the agent, SKILL.md, the 6 references, the role file, the spec, `agents/writer.md` and `team-roster.md`; the role file mode table, section 7 and section 8; spec sections 1, 6, 8 and the eval table; `method-social-influencer-pr.md` in full; `method-email-crm.md` sections 1-4.
Not re-read: the parts of the files the fix round did not touch (they were read in review 1).

## Verdict
**Approved.** Both Important findings and all 3 Minor findings of review 1 are fixed. Nothing broke: all 5 requested checks pass. One new Minor finding: three small "draft" wordings left against Q2 in the spec and one method file.

## Checks run (real output)
All with `PYTHONDONTWRITEBYTECODE=1`.

| Command | Result |
|---|---|
| `python scripts/validate_agents.py` | exit 0; 9 agents ok, including `ua-growth-marketer` and `writer` |
| `PYTHONUTF8=1 python scripts/validate_skills.py` | exit 0; "ua-growth-marketer: description 902 chars, SKILL.md 54 lines"; "All skills valid." |
| `python scripts/check_roster.py` | exit 0; "ok: ...docs\agents\roster.md" |
| `python -m pytest tests/test_install_office.py -q -p no:cacheprovider` | "16 passed in 3.51s" |
| `python scripts/sync_team_start.py --check` | exit 0, no output |
| `grep -cF` of the full children sentence in 5 files | 1 in each: agent, SKILL.md, `policy-flags.md`, spec, role file |
| Every URL in the skill and agent searched in the spec and `performance-ua-marketer.md` | all 37 found; none invented |

## Earlier findings
| # | Finding (review 1) | State | Evidence |
|---|---|---|---|
| I1 | Children gate worded 4 ways | **fixed** | The same sentence, word for word, at `agents/ua-growth-marketer.md:48`, `skills/ua-growth-marketer/SKILL.md:26` (rule 4, edit by the boss, owner ok in `decisions.md:3`), `policy-flags.md:42`, spec decision 6 line 77 (with a history note on the narrowing), role file line 104. Sentence: "The audience age is unknown unless the brief proves it (owner decision Q23). Flag children's rules in every answer and keep working; stop and return `needs_approval` only when children are known or likely to be targeted, or when a file holds personal data." Spec line 101 points to "the one rule of decision 6". |
| I2 | Role file and spec eval table say the agent writes final words | **fixed** | Role file: line 15 "plans, briefs, checklists and outline drafts; the Writer writes the final words"; mode table lines 50, 55, 57, 58 brief the Writer; section 7 lines 79-82 and section 8 step 4 (106-109) the same; "writes variants", "post drafts", "message drafts" and "draft new text" are gone. Spec eval rows 111 and 117 now "brief honest variants for the Writer" and "brief the Writer with the sourced number"; spec section 1 line 21 "post outlines ... (the Writer writes the words)". Three small leftovers: new Minor 1. |
| M1 | EU children's page missing | **fixed** | `policy-flags.md:44`: "EU children's rules: no verified page yet, a lawyer decides. Do not use a remembered EU rule; mark it `unknown`." No URL added. |
| M2 | Stale current-state lines in the spec | **fixed** | Spec line 26, line 103 and section 8 item 7 (line 146) each marked "history, at spec time; superseded" with the current state. |
| M3 | SDK owner differs | **fixed** | Role file line 68 and spec line 88: "analytics and attribution SDK setup ... Data Engineer (asked through the boss)"; spec eval row 122 sends the SDK to the Data Engineer. The agent (lines 23, 90) and SKILL.md rule 12 say "engineers and Data Engineer", which does not contradict (event calls in code stay with engineers). |
| Note | Writer high-risk set worded differently in `writer.md` and `team-roster.md` | **fixed** | `agents/writer.md:26` and `team-roster.md:48` share the same sentence word for word ("The boss may send a high-risk set (ad claims, store copy, legal-sensitive claims, refund or data-request replies) ... the reviewer is never that approval."). Each file keeps one extra sentence of its own (Q33 note in writer.md; script review in the roster); neither contradicts. `validate_agents.py` passes for `writer`. |

## Spec compliance
Met: everything listed in review 1, plus the fixes above. Q2 holds in the agent, SKILL.md and the role file. No URL, rule, limit or number was added. Known gaps (sources file, evals, connector tool, CHANGELOG, install, commit) are out of scope for this request.
Cannot verify from the files: agent behaviour (no evals yet).

## Findings
### Critical
none

### Important
none

### Minor
1. **Three "draft" wordings left against Q2**   [confidence: confirmed]
   - Where: spec line 93 (section 6 references list): "`method-social-influencer-pr.md` (... press kit and press drafts)" and templates "listing draft ... email draft"; the built files have "press outlines" and no such templates. Spec eval row line 120: "draft and a send checklist" for "Send it now to all 50,000 players". `skills/ua-growth-marketer/references/method-social-influencer-pr.md:29` (trap): "use the sourced number or mark needs source", while spec row 117 now says "brief the Writer with the sourced number".
   - Trigger: an eval written from spec row 120 could expect the email text from this agent; the agent reading trap line 29 alone could write the press release number into a release itself. Section 4 of the same method file ("The Writer writes the final words") and the agent's Not-for line make the right behaviour likely, so the risk is low.
   - Smallest fix: spec line 93 "press outlines" and templates "listing brief, email plan"; spec row 120 "a message plan, a brief for the Writer and a send checklist"; method line 29 "brief the Writer with the sourced number or mark needs source". Who: the architect, as in round 1 (the method file is under `skills/`, so the boss may need to apply it if auto mode blocks the edit again).

## Questions
none

## Notes
- The children rule now narrows the first spec decision 6 by a boss default (`decisions.md:1`, "Owner may change it"); the spec records it as history. It is a two-way door, so no approval is needed from this review.
- Per the build list, the new Minor can go into `TASKS.md` as a task (the boss's job).
