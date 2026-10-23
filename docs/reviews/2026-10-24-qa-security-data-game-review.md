# Review: QA / Test Engineer, Security Reviewer, Data Engineer, Game & Technical Engineer

Date: 2026-10-24 (checks run 2026-10-23). Reviewer: Claude (review pass, documents only).
Scope: `docs/agents/roles/qa-test-engineer.md`, `docs/superpowers/specs/2026-10-24-qa-test-merge.md`, `docs/agents/roles/security-reviewer.md`, `docs/agents/roles/data-engineer.md`, `docs/agents/roles/game-technical-engineer.md`. No skill, agent, eval or script was built or changed.

## How it was checked
- **Map and territory (main test).** Every checkable claim was compared with the real file: `agents/*.md` front matter, `skills/ai-engineer/scripts/eval_compare.py`, `skills/hire-an-engineer/references/*.md` section headings and lines, `skills/software-architect/references/`, `docs/agents/roster.md`, `TASKS.md`, `scripts/`, `evals/`, git history (deleted part documents), and the neighbour role documents.
- **Source counts** were recounted with a script over each sources table (rows and status column).
- **Outside sources:** 56 URLs opened on 2026-10-23 (13 QA, 15 Security, 14 Data, 14 Game and Technical); the page title was compared with the claimed title, and a few quoted numbers were checked in the page text.
- **Thinking skills:** pre-mortem and inversion (how would each role fail after six months), red team (concrete leak and misuse paths only), steel-manning (strongest case against each boundary), Bayesian (how much to trust "verified" labels: every opened page matched its title, so the labels are reliable; the only failures were pages already marked unverified).

Result labels: **ok** (the claim matches the file or page), **fixed** (wrong, corrected in the document with a "Review pass" line at the bottom), **open** (the owner must decide, or it is outside these documents).

## 1. QA / Test Engineer: role document

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | Not built: no skill, agent file or eval | `skills/`, `agents/`, `evals/` listings | ok |
| 2 | Spec is `docs/superpowers/specs/2026-10-24-qa-test-merge.md` | file exists | ok |
| 3 | `art-qa.md` stays in place as background | `docs/agents/roles/art-qa.md` exists | ok |
| 4 | Sections 1 to 10 exist | the document | ok |
| 5 | Code Reviewer never runs the product as a user and never edits | `agents/code-reviewer.md` (tools Read, Grep, Glob, Bash, Write; writes only `docs/reviews/`; tests only through `run_tests_safe.py` after approval) | ok |
| 6 | Builders named "Backend & Integration Engineer" | `TASKS.md` rows 6 (Backend Engineer) and 6b (Integration Engineer, split) | fixed |
| 7 | Held-out AI cases "kept and run here" (stated as settled in section 2) | spec open question 1; `agents/ai-engineer.md` line 50 (QA or Data Scientist & Analyst) | fixed ("by default") |
| 8 | AI release check reports `k of n` before and after and the flipped cases, never the case text | `eval_compare.py`: prints `k of n` per set and case ids only (regressions, fixed, missing) | ok |
| 9 | `ux-ui-designer.md` says "Accessibility Specialist" | `ux-ui-designer.md` lines 34, 44, 58, 64 | ok |
| 10 | 7-field answer; statuses done, needs_answers, needs_approval, blocked | `scripts/agent_contract.py` lines 17, 101-124 | ok |
| 11 | `engineering-principles.md` section 5: testing table, "all critical flows", "whole suite rerun", flaky "fixed or removed", "WCAG AA checklist + automated scan" | lines 63-84 | ok |
| 12 | `engineering-discipline.md` sections 3 and 5 | headings "Test first", "Evidence before done" | ok |
| 13 | `integrations.md` sections 4 and 6: test keys first, one approved live check | lines 71, 93 | ok |
| 14 | `technical-products.md` sections 4 and 5; typical frame rate in the budget table | lines 63-93; line 69 "60 fps" | ok |
| 15 | `ui-ux.md` section 7 lists 44 by 44 px under "WCAG 2.2 AA basics"; section 8 has the 4 to 1 scale | lines 89, 91, 108 | ok |
| 16 | `visual-quality.md` 6 and 7, `motion.md` 7, `project-management.md` 4 (P0 to P3), `cost-management.md` | headings and line 54 | ok |
| 17 | `software-architect/references/game-performance-budgets.md` exists | file listing | ok |
| 18 | Test-mode table: 38 sources, 37 verified, 1 unverified; same as the old document | recount; `git show HEAD:` old file line 134 | ok |
| 19 | Art QA: 40 sources, 39 verified, 1 unverified (EBU R 128) | `art-qa.md` line 139; recount | ok |
| 20 | Merged-modes table: 35 sources, 35 verified | recount | ok |
| 21 | WCAG 2.2 appears in all three lists | `art-qa.md` line 98 | ok |
| 22 | W3C WCAG-EM 2.0, Group Note, 2026 | https://www.w3.org/TR/WCAG-EM/ (Group Note 23 July 2026) | ok |
| 23 | WCAG2ICT, Group Note, 2025 | https://www.w3.org/TR/wcag2ict-22/ (11 December 2025) | ok |
| 24 | axe-core claims about 57 percent | https://github.com/dequelabs/axe-core ("on average 57% of WCAG issues") | ok |
| 25 | GOV.UK: 42 of 143 barriers (29 percent) missed by all 10 tools | accessibility.blog.gov.uk 2017 post | ok |
| 26 | Xbox Accessibility Guidelines v3.2, 2023 | learn.microsoft.com (V3.2, 8 June 2023) | ok |
| 27 | Android: frames over 700 ms are frozen | developer.android.com slow rendering (700 ms to 5 s) | ok |
| 28 | Web Vitals at the 75th percentile | web.dev/articles/vitals | ok |
| 29 | k6 example: 95 percent of requests under 200 ms | grafana.com k6 thresholds (`p(95)<200`) | ok |
| 30 | Stewart, "Test Sizes", 2010 | testing.googleblog.com (13 December 2010) | ok |
| 31 | Politowski et al., "A Survey of Video Game Testing", 2021 | arxiv.org/abs/2103.06431 | ok |
| 32 | Playwright "Visual comparisons" | playwright.dev/docs/test-snapshots | ok |
| 33 | SC 2.5.8 Target Size (Minimum), level AA | w3.org/WAI Understanding page | ok |
| 34 | Bach, "Session-Based Test Management" | satisfice.com download page | ok |

## 2. QA / Test Engineer: merge spec

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | Nothing built: no `skills/qa-test-engineer/`, `agents/qa-test-engineer.md`, `evals/qa-test-engineer/` | listings | ok |
| 2 | "merged into 22 bigger roles" | `TASKS.md` heading "Roles (23)" (6b added) | fixed |
| 3 | QA is role 9 in `TASKS.md` | `TASKS.md` line 135 | ok |
| 4 | Only QA and Art QA had documents; Playtest, Performance, Accessibility had none | git history of `docs/agents/roles/` (no such files ever) | ok |
| 5 | `game-technical-engineer.md` points to QA Performance and Playtest modes | lines 47, 56 | ok |
| 6 | `TASKS.md` untouched | working copy: row 9 now "Documented / Not started" | fixed |
| 7 | "see section 8 for the follow-ups" | the spec has sections 1 to 7; follow-ups are in section 5 | fixed |
| 8 | Orchestrator may call only `architect, code-reviewer, ai-engineer, data-scientist` | `agents/orchestrator.md` lines 5 and 28 | ok |
| 9 | Code Reviewer tools and write rules | `agents/code-reviewer.md` lines 5, 30, 31 | ok |
| 10 | AI Engineer has `references/method-release-check.md` and `scripts/eval_compare.py` | `skills/ai-engineer/` listing | ok |
| 11 | `eval_compare.py` reads one cases file, each case `"set": "open"` or `"held_out"`, compares recorded outputs offline | script lines 7, 22, 39-41, 64 | ok |
| 12 | `agents/ai-engineer.md`: no held-out set means `blocked`; never read the held-out set | lines 50 and 83 | ok |
| 13 | The hiding rests on a prompt rule | AI Engineer has Read and Bash; nothing blocks a path | ok |
| 14 | No playtest method anywhere in the repo | no "playtest" in `skills/` | ok |
| 15 | 44 px project target vs 24 CSS px for SC 2.5.8 | `ui-ux.md` line 91; W3C Understanding page | ok |
| 16 | The Data Scientist merge spec defaults the held-out cases to itself (conflict) | `2026-10-24-data-scientist-analyst-merge.md` line 111; AI-Ops merge spec line 67 defaults to QA | ok |
| 17 | `docs/art-qa/` named in `art-qa.md`, never written | `art-qa.md` lines 27, 66, 84; no such folder | ok |
| 18 | Check scripts exist (`validate_skills`, `validate_agents`, `check_sources`, `check_evals`, `check_roster`, `install_agents --only`) | `scripts/` listing; `install_agents.py` line 6 | ok |
| 19 | `GROUND-TRUTH.md` "as for the other roles" | only `evals/ai-engineer/` and `evals/data-scientist/` have one | fixed |
| 20 | Eval plan: 18 cases, at least 3 per mode, each plants a trap | table: Test 5, Playtest 4, Art QA 3, Performance 3, Accessibility 3; every row has a trap and a "must do" | ok |
| 21 | Every open question has a default | section 6, 6 of 6 | ok |
| 22 | Sources 38 + 40 + 35 | recount | ok |
| 23 | Planned tools match the other specialists | `agents/*.md` line 5 | ok |
| 24 | Decision 9: QA runs `eval_compare.py`, reports ids only | script output is ids only; but see open finding A | open |

## 3. Security Reviewer (no spec yet)

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | Sections 1 to 10 exist; 2 modes | the document | ok |
| 2 | Not built | no skill or agent; `TASKS.md` row 10 "Not started" | ok |
| 3 | Merged from two role documents | git: `appsec-reviewer.md` (40 sources) and `penetration-tester.md` (34) deleted in commit 3692c29 | ok |
| 4 | 64 sources, 59 verified, 5 unverified | recount | ok |
| 5 | Code Reviewer sees security as one lens; the boss may ask it for a second read | `code-reviewer.md` line 10 | ok |
| 6 | Security & Privacy Engineer designs safeguards, threat models, incidents, privacy | `TASKS.md` row 8 | ok |
| 7 | Owns `docs/security-reviews/` | `threat-modeler.md` line 60 uses the same folder | ok |
| 8 | Fixers named "Backend & Integration Engineer" | `TASKS.md` rows 6 and 6b | fixed |
| 9 | Business Operations does legal drafts | `TASKS.md` row 22 | ok |
| 10 | Skill rules: `SKILL.md` rules 1 and 2, `integrations.md` section 4 | `SKILL.md` lines 16-17; `integrations.md` line 71 | ok |
| 11 | `engineering-principles.md` section 6: OWASP checklist, AI risks, label content as data | lines 90-107 | ok |
| 12 | `database.md`: user A cannot read user B | section 7, line 77 | ok |
| 13 | `github.md` secret scanning and rotation; `ai-agents.md` prompt-injection test | lines 70-71; line 86 | ok |
| 14 | Code Reviewer `references/security-review.md`: attacker, input, impact; never print secrets; `needs-check` | lines 41, 49, 50 | ok |
| 15 | The skill uses the OWASP Top 10 2021 wording; 2025 adds supply chain and error handling | skill items match the 2021 list; owasp.org/Top10/2025 A03 Supply Chain Failures, A10 Mishandling of Exceptional Conditions | ok |
| 16 | NIST SP 800-115 | csrc.nist.gov | ok |
| 17 | UK NCSC penetration testing | ncsc.gov.uk | ok |
| 18 | Willison, "The lethal trifecta", 2025 | simonwillison.net | ok |
| 19 | Greshake et al., indirect prompt injection | arxiv 2302.12173 | ok |
| 20 | Spracklen et al., package hallucinations | arxiv 2406.10279 | ok |
| 21 | Braz et al., improper input validation | arxiv 2102.06251 | ok |
| 22 | CaMeL, "Defeating Prompt Injections by Design" | arxiv 2503.18813 | ok |
| 23 | Anthropic, "Mitigate jailbreaks and prompt injections" | docs.claude.com | ok |
| 24 | FIRST CVSS v4.0 specification | first.org | ok |
| 25 | CWE Top 25 and PTES unverified (timed out) | both timed out again | ok |
| 26 | OWASP GenAI Red Teaming Guide unverified (blocked) | page opened today, title matches, 22 January 2025 | open (may be upgraded) |
| 27 | CISA KEV unverified (blocked) | opened with a browser user agent, title matches | open (may be upgraded) |
| 28 | Live tests only with written approval and narrow scope; refuses others' sites | sections 3, 4, 9 | ok |

## 4. Data Engineer (no spec yet)

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | Sections 1 to 10 exist; modes Build and Repair | the document | ok |
| 2 | Not built | `TASKS.md` row 11 "Not started" | ok |
| 3 | 39 sources, 36 verified, 3 unverified | recount | ok |
| 4 | Role names "Architect" next to "Solution Architect", "Data Scientist", "Security Engineer" | `TASKS.md` rows 2, 5, 8 | fixed |
| 5 | Owns `docs/data/` | `docs/agents/roster.md`: `docs/data/` belongs to the architect; "one owner per artifact" | fixed (now `docs/data-pipelines/`) |
| 6 | Integration Engineer hands over the adapter and a "collect once" command | `integration-engineer.md` lines 38, 80 | ok |
| 7 | Backend Engineer does not build pipelines | `backend-engineer.md` line 41 | ok |
| 8 | Data Scientist & Analyst does not build pipelines | `data-scientist.md` line 43 | ok |
| 9 | Solution Architect sends pipelines to the Data Engineer | `solution-architect.md` lines 49, 90 | ok |
| 10 | `platform-targets.md` section 3: raw data never edited | line 59 | ok |
| 11 | `database.md` sections 4 to 8: import checks with row counts, backups, restore | lines 59, 60, 68, 79 | ok |
| 12 | `engineering-principles.md` section 10: size first, design for 10 times | line 138 | ok |
| 13 | `process-automation.md` section 6: copies, safe twice, run log, failure alerts | lines 72-77 | ok |
| 14 | `integrations.md` sections 5 and 11; `cost-management.md` sections 3 and 4 | lines 80-81, 125; headings 55, 69 | ok |
| 15 | AWS article adds jitter and a cap | aws.amazon.com builders library | ok |
| 16 | Slice-rebuild note rests on "the batch-processing article" | Beauchemin is unverified (403 again) | fixed (now says unverified) |
| 17 | Kleppmann, DDIA | dataintensive.net | ok |
| 18 | Kimball and Ross, 3rd ed. | kimballgroup.com | ok |
| 19 | Dehghani, Data Mesh principles | martinfowler.com | ok |
| 20 | Armbrust et al., Lakehouse, CIDR 2021 | PDF text: title and authors match | ok |
| 21 | Sambasivan et al., Data Cascades | research.google | ok |
| 22 | Sculley et al., Hidden Technical Debt | papers.nips.cc | ok |
| 23 | Gebru et al., Datasheets for Datasets | arxiv 1803.09010 | ok |
| 24 | OpenLineage docs; GDPR Article 5 | openlineage.io; gdpr-info.eu | ok |
| 25 | Sussman and Beauchemin unverified (403) | both 403 again | ok |
| 26 | Breck et al. unverified (text not matched) | PDF metadata title "Data Validation for Machine Learning", first author Breck | open (may be upgraded) |
| 27 | Schelter et al. verified | PDF text could not be read by my script | open (not re-confirmed) |

## 5. Game & Technical Engineer (no spec yet)

| # | Claim | Real file or URL checked | Result |
|---|---|---|---|
| 1 | Sections 1 to 10 exist; 4 modes | the document | ok |
| 2 | Not built | `TASKS.md` row 15 "Not started" | ok |
| 3 | Merged from two role documents | git: `game-unity-engineer.md` (40 sources) and `technical-artist.md` (40) deleted in commit a4c655e | ok |
| 4 | 44 sources, 43 verified, 1 unverified | recount (the merged count after removing duplicates was not re-derived) | ok |
| 5 | Server work named "Backend & Integration Engineer" | `TASKS.md` rows 6 and 6b | fixed |
| 6 | QA owns whole-game profiling, playtests and final art checks | `qa-test-engineer.md` sections 3, 4 | ok |
| 7 | Build settings owned by this role, not DevOps | `devops-engineer.md` lines 18, 66 | ok |
| 8 | Artist = 2D, 3D, animation, effects | `TASKS.md` row 13 | ok |
| 9 | `technical-products.md`: engine does not make a job Large; playable ad is one self-contained file | lines 11, 117 | ok |
| 10 | Skill budget is 60 fps; game references suggest 30 fps on mobile | `technical-products.md` line 69; `game-performance-budgets.md` line 9 | ok |
| 11 | Five `software-architect/references/game-*.md` files | listing | ok |
| 12 | "Unity pages are for the Unity 2022 era" | the `/Manual/` links open Unity 6.6 (6000.6) today | fixed |
| 13 | "Limit of this backing" paragraph | two sentences were repeated, one started in lower case | fixed |
| 14 | Unity "Reduce rendering work on the CPU or GPU" | docs.unity3d.com | ok |
| 15 | Unity "Optimization" | docs.unity3d.com | ok |
| 16 | Unity "Frame Debugger window reference" | docs.unity3d.com | ok |
| 17 | Unity "Choose a GPU texture format by platform" | docs.unity3d.com | ok |
| 18 | Unity "Sprite atlases" | docs.unity3d.com (redirects, title matches) | ok |
| 19 | Unity "Introduction to static batching" | docs.unity3d.com | ok |
| 20 | Shader Graph 14.0 | docs.unity3d.com packages | ok |
| 21 | AppLovin: 5 MB single HTML | support.axon.ai: "5 MB or smaller", "single HTML file" | ok |
| 22 | Unity Playworks AppLovin page | docs.lunalabs.io: single html, up to 5MB | ok |
| 23 | Segwise 2026 comparison, third party | segwise.ai | ok |
| 24 | Google Ads uploaded display ads specs | support.google.com | ok |
| 25 | IAB MRAID | iab.com | ok |
| 26 | Khronos KTX 2.0 | registry.khronos.org | ok |
| 27 | Arm GPU guide unverified | page gives only "Documentation – Arm Developer" | ok |

## Counts
- Claims checked: 140 (QA role 34, QA spec 24, Security Reviewer 28, Data Engineer 27, Game & Technical 27).
- Fixed in the documents: 13 claims (QA role 2, QA spec 4, Security Reviewer 1, Data Engineer 3, Game & Technical 3). A fixed name was often changed in several places in the same file.
- Open: 5 rows in the tables, plus the findings A to G below.
- Outside URLs opened: 56 (QA 13, Security Reviewer 15, Data Engineer 14, Game & Technical 14). Titles matched on every page that opened; the pages that failed were already marked unverified.

## Open findings for the owner
**A. Held-out AI cases: who keeps them, and who runs the compare (decide before building QA).**
- Two specs disagree: the AI-Ops merge spec defaults to QA; the Data Scientist merge spec defaults to the Data Scientist & Analyst once the AI-Ops modes exist (they now do).
- The real script `eval_compare.py` reads one cases file that holds both sets, with the `contains` texts. `agents/ai-engineer.md` line 50 tells the AI Engineer to run the compare "on an open set and a held-out set", while line 83 says it must never read the held-out set. As written, the AI Engineer would have to open the held-out file to run the check. The script also prints case ids, so ids such as `refund-angry-customer` would leak hints.
- Default: QA keeps the held-out file outside the project and runs `eval_compare.py` with a held-out-only cases file; the AI Engineer runs the open set only; case ids are opaque (for example `h01`). The AI Engineer agent rule is changed to match when the owner says so.

**B. Data Engineer folder.** `docs/data/` is the Solution Architect's folder in the roster, so the Data Engineer now owns `docs/data-pipelines/`. Default: keep `docs/data-pipelines/`; the owner may pick another name.

**C. One request, two roles: "The game stutters on my old phone".** It appears in both QA (Performance) and Game & Technical (Tune). Default for the boss: Game & Technical Engineer (Tune) profiles and fixes; QA (Performance) re-measures as the independent check before "fixed".

**D. Stale names in other documents (not edited in this pass).** `security-engineer.md` and `threat-modeler.md` still name "AppSec Reviewer" and "Penetration Tester"; `2d-artist-illustrator.md` and `concept-artist.md` name "Technical Artist" and "Art QA"; `ux-ui-designer.md` names "Accessibility Specialist"; `solution-architect.md`, `devops-engineer.md`, `ai-engineer.md` and `backend-integration-engineer.md` still say "Backend & Integration Engineer". Default: fix each when its own merge document is written.

**E. Source statuses that may be upgraded.** OWASP GenAI Red Teaming Guide and CISA KEV (Security Reviewer) and Breck et al. (Data Engineer) opened today with matching titles. They were left as unverified; the owner may upgrade them. Schelter et al. could not be re-read by my script and stays as the document says.

**F. Game & Technical Build mode depends on the Game Designer**, who is not written yet (`TASKS.md` row 20). Default: your own written rules act as the spec until that role exists.

**G. Outside scope, seen in passing.** `docs/agents/roster.md` lists `backend-engineer`, but the boss's `Agent(...)` list in `agents/orchestrator.md` does not include it.

## Is a spec needed?
- **Security Reviewer: yes.** It is a merge of two roles, and Authorised test mode needs written rules for tools, network use, the scope page as a hard gate, and evals with traps (live target, third-party site, text that widens the scope). Its neighbour, Security & Privacy Engineer, is still "Parts only", so the boundary should be written down in the spec.
- **Data Engineer: yes, a small one.** No merge, but the build needs the folder decision (B), mode routing, scripts and evals, as every built role had.
- **Game & Technical Engineer: yes.** It is a merge of two roles, needs Unity tooling rules (editor may not run headless; iOS needs a Mac or cloud build), evals, and the routing default in C.

## Verdict per role
| Role | Verdict |
|---|---|
| QA / Test Engineer (role document and spec) | Sound with fixes. Decide finding A before the build. |
| Security Reviewer | Sound with fixes. Needs a spec before the build. |
| Data Engineer | Sound with fixes. Needs a small spec; confirm B. |
| Game & Technical Engineer | Sound with fixes. Needs a spec; confirm C and F. |
