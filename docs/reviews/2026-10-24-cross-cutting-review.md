# Cross-cutting review of all role documents and specs

Date: 2026-10-24. Reviewer: cross-cutting test (read-only; no role document, spec, skill, agent, eval or script was changed).
Inputs read: `docs/agents/roles/*.md` (26 files), `docs/superpowers/specs/*.md` (17 files), `docs/agents/roster.md`,
`TASKS.md` (roles table), `agents/orchestrator.md`, `CHANGELOG.md`, plus the live "Agent Team Tracker" artifact rows,
`skills/orchestrator/references/team-roster.md` and `docs/agents/visual-office/index.html` where a finding needed the real file.
Thinking skills applied: map vs territory, systems, second-order, theory of constraints, pre-mortem, inversion.

Snapshot note: other reviewers were editing role documents at the same time (the working tree shows many modified files).
Every finding below is what the files said when they were read. Re-check a finding before acting on it if the document was edited after this review.

## Summary

- Script checks: all pass (details in section 1).
- Findings: **5 blockers, 14 important, 12 minor** (section 10).
- The biggest risks are not inside single documents. They sit **between** documents: (1) the boss cannot call the Backend Engineer, which it is told to use; (2) seven work items have two owners or a disputed owner (ad copy, store text, ad test question, held-out AI cases, secrets register, security audits, release notes); (3) "tracking code" has no owner that accepts it; (4) status words say more than the evidence ("Documented" for roles without a spec, "Tested" for partly tested roles).
- **The constraint is the owner's attention, not writing.** There are 38 open questions across the specs (section 9). Building more roles before the 6 boundary questions are answered would put the same conflicts into skills, evals and agent files, where they cost more to undo.

## 1. Script results (run 2026-10-24, from the repo root)

| Check | Result | Exact output (short) |
|---|---|---|
| `python scripts/validate_agents.py` | PASS (exit 0) | ✓ ai-engineer, architect, backend-engineer, code-reviewer, data-scientist, orchestrator |
| `python scripts/validate_skills.py` | PASS (exit 0) | 8 skills ✓; "All skills valid." Descriptions: ai-engineer 1012, backend-engineer 1008, code-reviewer 691, data-scientist 925, hire-an-engineer 736, orchestrator 723, software-architect 714, team-start 561 chars |
| `python scripts/check_roster.py` | PASS (exit 0) | `ok: ...\docs\agents\roster.md` |
| `python scripts/check_sources.py skills/<name>` (each skill) | PASS | ✓ ai-engineer, code-reviewer, data-scientist, orchestrator, software-architect; skipped (no `references/sources.md`): backend-engineer, hire-an-engineer, team-start |
| `python scripts/check_evals.py evals/<name>/evals.json` (each) | PASS | ✓ ai-engineer, code-reviewer, data-scientist, hire-an-engineer, orchestrator, software-architect. There is no `evals/backend-engineer/`. |
| `python -m pytest -q` (`pytest.ini`: `testpaths = tests`) | PASS | **390 passed, 2 skipped** in 56.51 s. No failure from the live `.agents/events.jsonl`. |

What the green checks do **not** prove: `check_roster.py` passes although the roster lists `backend-engineer` and the boss's `Agent(...)` list does not (finding B1). The checks look at built files only; no check reads role documents or specs.

## 2. Structure

### 2.1 Ten sections

All 26 files in `docs/agents/roles/` have exactly the 10 numbered sections (1. What this role is ... 10. Where it learned this). No file is missing a section.

### 2.2 The 23 roles in `TASKS.md` against the files that exist

| # | Role (TASKS.md) | Documentation (TASKS) | Role document file(s) | Spec file | Note |
|---|---|---|---|---|---|
| 1 | Orchestrator | Documented | `orchestrator.md` | `2026-10-23-orchestrator-design.md` | ok |
| 2 | Solution Architect | Documented | `solution-architect.md` | `2026-10-22-architect-agent-design.md` (system design only) | no spec for the Data design merge; only the master plan mentions it |
| 3 | Code Reviewer | Documented | `code-reviewer.md` | `2026-10-23-code-reviewer-design.md` | ok |
| 4 | AI Engineer | Documented | `ai-engineer.md` | `ai-engineer-design`, `ai-engineer-ai-ops-merge` | ok |
| 5 | Data Scientist & Analyst | Documented | `data-scientist.md` | `data-scientist-design`, `data-scientist-analyst-merge`, `-sources` | file name is the old single-role name |
| 6 | Backend Engineer | Documented | `backend-engineer.md` | `backend-integration-split.md` | ok |
| 6b | Integration Engineer | Documented | `integration-engineer.md` | `backend-integration-split.md` | ok |
| (old) | Backend & Integration Engineer | — | `backend-integration-engineer.md` | `backend-integration-merge.md` | **superseded** by the split, still in place, still says "Built (2 of 4 modes)" and writes `docs/backend/integrations/` |
| 7 | DevOps Engineer | Documented | `devops-engineer.md` | `devops-merge.md` | ok |
| 8 | Security & Privacy Engineer | Parts only | `security-engineer.md`, `threat-modeler.md` | none | see 2.3 |
| 9 | QA / Test Engineer | Documented | `qa-test-engineer.md` (+ old part `art-qa.md`) | `qa-test-merge.md` | `art-qa.md` superseded, still names `docs/art-qa/` |
| 10 | Security Reviewer | Documented | `security-reviewer.md` | **none** | "Documented" means "role document and spec done" (TASKS.md line 122); the spec is missing |
| 11 | Data Engineer | Documented | `data-engineer.md` | **none** | same |
| 12 | Creative & Art Director | Documented | `creative-art-director.md` | `creative-art-director-design.md` | ok |
| 13 | Artist | Parts only | `concept-artist.md`, `2d-artist-illustrator.md` | none | see 2.3 |
| 14 | Video & Sound Editor | Parts only | `video-editor.md` | none | see 2.3 |
| 15 | Game & Technical Engineer | Documented | `game-technical-engineer.md` | **none** | same as 10 and 11 |
| 16 | Writer | Documented | `writer.md` (+ old part `storyboard-scriptwriter.md`) | `writer-merge.md` | `storyboard-scriptwriter.md` superseded, still names `docs/storyboards/` |
| 17 | Designer | Parts only | `ux-ui-designer.md` | none | see 2.3 |
| 18 | Frontend & Mobile Engineer | Not written | none | none | other documents already hand work to it |
| 19 | UA & Growth Marketer | Documented | `ua-growth-marketer.md` (+ old part `performance-ua-marketer.md`) | `ua-growth-merge.md` | old part superseded, still names `docs/ua-marketing/` |
| 20 | Game Designer | Not written | none | none | other documents already hand work to it |
| 21 | Product & Business Analyst | Documented | `product-business-analyst.md` | `product-business-analyst-design.md` | ok |
| 22 | Business Operations | Not written | none | none | other documents send legal drafts to it |

Counts: 23 roles; 16 marked Documented; 4 Parts only; 3 Not written. **By the TASKS.md definition only 12 are fully documented** (2, 10, 11, 15 lack a spec for the role as merged). 26 role files exist: 16 role documents for whole roles, 6 part documents (security-engineer, threat-modeler, concept-artist, 2d-artist-illustrator, video-editor, ux-ui-designer) and 4 superseded documents (backend-integration-engineer, art-qa, storyboard-scriptwriter, performance-ua-marketer). `database-architect.md` was deleted in the working tree (merged into the Solution Architect).

### 2.3 The 4 parts-only roles: what exists and what a merge needs

| Role | Part documents that exist | Missing parts | Also needed for a merge |
|---|---|---|---|
| 8 Security & Privacy Engineer | `security-engineer.md` (folder `docs/security/`), `threat-modeler.md` (`docs/threats/`) | Incident Responder, Privacy / Compliance | one merged document; a spec; mode names; one folder root (`docs/security/` with `threats/` inside, or keep both); remove the "list of keys" claim (DevOps owns the secrets register); settle security audits vs Security Reviewer (I5); settle the security-incident line with DevOps (I6). Both part documents use old names (AppSec Reviewer, Penetration Tester, Architect). |
| 13 Artist | `concept-artist.md` (`docs/concept/`), `2d-artist-illustrator.md` (`docs/art-2d/`) | 3D Artist, Animator, VFX Artist | merged document and spec; one asset/licence register instead of three (I9); prompt packs owned once (Creative vs Concept); "style check of finished art" (2D part) removed or made a self-check, since Creative reviews and QA Art QA checks. Creative spec Q6 says build it together with Creative & Art Director. |
| 14 Video & Sound Editor | `video-editor.md` (`docs/video/`) | Sound Designer | merged document and spec; licence list folded into the shared register; uses old names (Art QA). |
| 17 Designer | `ux-ui-designer.md` (`docs/ux-design/`) | Graphic & Motion Designer, Web Designer, UX Researcher | merged document and spec; it still names retired roles (Accessibility Specialist, Art Director, Content Writer, Product Manager, UX Researcher, Frontend Engineer) and a folder `docs/art-direction/` that no role owns (Creative uses `docs/creative/art-direction/`); usability research line with the Product & Business Analyst. |

## 3. Boundaries: who owns what

Legend: **O** owns (writes it); **c** contributes or provides input; **r** reviews or checks; **—** says it is not theirs. "(doc)" = role document, "(spec)" = spec.

| Work item | Owner(s) the documents name | Problem |
|---|---|---|
| Data pipelines | Data Engineer **O**; Integration Engineer may write one simple scheduled job "hand over to Data Engineer" until DE is built (split spec Q4) | ok; temporary exception is written down |
| Tracking code (analytics events, SDKs) | Data Scientist (doc) and UA (doc) say **Data Engineer**; the Data Engineer document never mentions tracking code or SDKs; Backend records server events for the DS's metrics; Game & Technical Engineer does not mention analytics SDKs | **zero owners that accept it** (I3) |
| Tracking plan (what to track) | Data Scientist & Analyst **O** (planned Metrics mode, `docs/analytics/tracking-plan.md`) | mode not built |
| Metric definitions | Data Scientist & Analyst **O** (planned); AI, UA, PBA, Creative all point to it; owner approves | one owner, but not built: today definitions come back as owner decisions |
| Held-out AI release cases | QA doc: QA by default; AI doc: "QA or DS"; DS doc: "may keep, if you choose"; DS merge spec Q3 default: **DS** (AI-Ops is built, so its condition is met); QA merge spec Q1 default: **QA** | **two conflicting defaults**; nobody keeps them today (B2) |
| Secrets register (key names) | DevOps **O** `docs/devops/secrets-register.md` (doc + decision 10); Security Engineer part **O** "a list of keys and services" in `docs/security/`; Integration register keeps key names that must match DevOps | **two owners** (I4) |
| Backup and restore | Architect: backup plan design **and** "the evidence that a restore was tried" (doc s.5); Backend: restore note and restore test (DevOps decision 8); DevOps: scheduled backup job watched, release gate; Data Engineer: pipeline restore runbook | Architect doc vs DevOps decision 8 disagree on who produces restore evidence (M3) |
| Unity build | Game & Technical: inside the build (settings, size, speed); DevOps: running the build, signing from secret store, test tracks; QA: tests the build; a person uploads | consistent (DevOps decision 9 matches both documents) |
| Store listings | UA & Growth **O** listing drafts (`docs/marketing/store/`); Writer **O** "store copy" (`docs/writing/content/`); Creative owns the look of screenshots; DevOps prepares store submission | **two owners of the listing text** (B3) |
| Accessibility | Designer: basics in the design; QA: audit of the built product; ux-ui part still says "Accessibility Specialist" | ok in QA doc; part document stale (M5) |
| Security review / audit | Security Reviewer **O** (code review, pre-launch pass, authorised test); Security Engineer part: "runs a sized security pass" and lists findings; Architect doc routes "deep security audits" to the **Security & Privacy Engineer**; AI doc sends them to the Security Reviewer; DevOps names both | **two owners, conflicting routes** (I5) |
| Incident response | DevOps: outages, bad releases, cost spikes (doc + decision 7); Security & Privacy: security incidents (Incident Responder part has **no document**); leaked key: DevOps Q6 default S&P leads | security incidents have no documented owner (I6) |
| User research | PBA: problem and market interviews, research summaries (doc + spec call 6); Designer / UX Researcher: usability research (no UX Researcher document) | split agreed in the PBA spec; usability half undocumented (M6) |
| Release notes | Writer **O** "release notes in plain words" (Technical docs mode; may edit `CHANGELOG.md`); DevOps **O** release plan with "version, notes" in `docs/devops/release/<version>.md` | **two owners** (I7) |
| Support replies | Writer **O** (Support mode, `docs/writing/support/`); UA spec: "replies to players are drafts" (social) | one owner; small overlap on social replies (M7) |
| Ad creative | Creative **O** concepts, ad test sets, variant table, "the test question for each concept"; UA **O** test plan and "names the test question"; Writer scripts; Video edits; Artist art; Game & Technical playables | **two owners of the test question and variant table** (I8) |
| Ad copy | Writer doc s.3 Content mode: "ad copy"; Writer spec Q6 default: Writer writes the words; UA doc: "writes ad copy and store text", "this role writes short marketing copy (ads, store text, posts, emails, press drafts)" | **two owners, conflicting answers** (B3) |

Other overlaps found while reading (not in the requested list):

| Item | Owners | Problem |
|---|---|---|
| Performance sheet | Game & Technical "the performance sheet" (`docs/game-engineering/`); QA "the performance sheet" (`docs/qa/performance/`) | same name, two files; lines are written (own budgets vs whole game) but the name invites a merge by mistake (M8) |
| Pipeline files | DevOps writes pipeline files; Security Engineer part writes "pipeline security settings" | two writers of `.github/workflows/` (I10) |
| Asset / licence register | Creative `docs/creative/asset-register.md`; Concept `docs/concept/image-register.md`; 2D `docs/art-2d/` asset and licence register; Video licence list; Game & Technical package list with licence | five registers (I9) |
| Data dictionary | Architect `docs/data/` (design); Backend `docs/backend/` (what the code has); Data Engineer `docs/data-pipelines/` (delivered data) | written down on purpose; drift risk only (M9) |
| Email sending code | UA doc sends it to "Backend & Integration Engineer" (retired name) | must say Backend (unsubscribe endpoint) or Integration (email provider) (I11) |

## 4. Folders

| Folder | Writer (role) | Status |
|---|---|---|
| `.team/runs/`, `.agents/events.jsonl` (via `team_event.py`) | Orchestrator | built |
| `docs/architecture/`, `docs/decisions/`, `docs/data/` | Solution Architect | built (`docs/decisions/` is the same series `hire-an-engineer` writes; agreed in the architect spec) |
| `docs/reviews/` | Code Reviewer | built |
| `docs/ai/`, `docs/ai/ops/` | AI Engineer | built |
| `docs/analysis/` (built), `docs/analytics/` (planned) | Data Scientist & Analyst | built / planned |
| `docs/backend/`, migrations folder | Backend Engineer | built (also holds the integrations register until 6b is built) |
| `docs/integrations/` | Integration Engineer | planned |
| `docs/devops/`, `.github/workflows/`, `infra/` (brief-named) | DevOps | planned |
| `docs/qa/` + `playtest/`, `art/`, `performance/`, `accessibility/`; `tests/e2e/` (brief-named) | QA / Test | planned |
| `docs/security-reviews/`, `.../pentests/` | Security Reviewer | planned |
| `docs/data-pipelines/`, `pipelines/` | Data Engineer | planned |
| `docs/creative/`, `docs/creative/art-direction/`, `docs/creative/ads/` (spec adds `docs/creative/scripts/`) | Creative & Art Director | planned |
| `docs/game-engineering/`, `.../tech-art/` | Game & Technical | planned |
| `docs/writing/` (+ `content/`, `storyboards/`, `localisation/<lang>/`, `support/`), `README.md`, `docs/guides/`, `CHANGELOG.md` (when named) | Writer | planned |
| `docs/marketing/` (+ `ua/`, `store/`, `social/`, `email/`, `flags.md`) | UA & Growth | planned |
| `docs/product/` (or existing `docs/brief.md`, `docs/plans/roadmap.md`) | Product & Business Analyst | planned |
| `docs/security/`, `docs/threats/` | Security & Privacy parts | parts only |
| `docs/concept/`, `docs/art-2d/` | Artist parts | parts only |
| `docs/video/` | Video part | parts only |
| `docs/ux-design/` | Designer part | parts only |
| `docs/art-qa/`, `docs/storyboards/`, `docs/ua-marketing/`, `docs/backend/integrations/` | superseded part documents | replaced by `docs/qa/art/`, `docs/writing/storyboards/`, `docs/marketing/`, `docs/integrations/` |

Collisions and writes outside the stated place:

1. **Scripts and storyboards in three places:** Writer `docs/writing/storyboards/`; Creative spec call 5 adds `docs/creative/scripts/` (not in the Creative role document); old part `docs/storyboards/`. (I12)
2. **`README.md`, `CHANGELOG.md`, `docs/guides/`:** the Writer may edit them, and the base `hire-an-engineer` skill already maintains them; release notes also in `docs/devops/release/`. (I7)
3. **Pipeline files:** DevOps and the Security Engineer part both write them. (I10)
4. **`docs/art-direction/`** is named by `ux-ui-designer.md` but owned by nobody. (M5)
5. **Held-out AI cases:** "a place the brief names that the AI Engineer is not given". Every specialist has Read, Grep and Glob over the whole project, so any folder inside the project can be read. Only a folder outside the project (or a tool block) keeps them hidden. (B2)
6. **`tests/`:** builders write unit tests and QA writes end-to-end tests into brief-named folders; the boss's "one owner per file per run" rule covers it, but no folder split is written down. (M10)
7. **Near-same names in one role:** `docs/analysis/` and `docs/analytics/` (DS). Works, but easy to confuse. (M11)
8. **Superseded documents name retired folders.** If a builder follows the agent template (which starts from the role document) and opens the wrong file, the agent writes in a retired folder. (I13)

## 5. Orchestrator: who the boss can call

| Source | Specialists |
|---|---|
| `agents/orchestrator.md` `tools: Agent(...)` | architect, code-reviewer, ai-engineer, data-scientist (4) |
| `agents/orchestrator.md` description text | the same 4, written out by name |
| `docs/agents/roster.md` | architect, code-reviewer, ai-engineer, data-scientist, **backend-engineer** (5) |
| `agents/*.md` files | the 5 above + orchestrator |
| `skills/orchestrator/references/team-roster.md` | routes migrations, access tests and server code to `backend-engineer` ("Backend & Integration Engineer", retired name) |
| Office (`docs/agents/visual-office/index.html` `ALIAS`) | old core-12 ids (pm, ba, ux, fe, be, qa, reviewer, security, devops, aieng, datasci, architect); `roles.json` registry from `event-mapping.md` section 3 does not exist |
| Roles in `TASKS.md` | 23 (22 specialists + the boss) |

So the boss can call **4 of 22 specialist roles**. It is told to send database build work to a 5th agent it cannot call, which forces the "general helper, ask the owner once" path for every build job (B1).

Work to add each remaining role (the same steps for every role, after it is built and its evals pass):

1. Name in `Agent(...)` in `agents/orchestrator.md` **and** in its `description` (both list names today).
2. Row in `docs/agents/roster.md` (name, skill, model, owned folders); later an effort column (I2).
3. Routing lines in `skills/orchestrator/references/team-roster.md`, and review gates in `references/quality-gates.md` if the role adds a gate (QA, Security Reviewer).
4. Office: an `ALIAS` entry (or the planned `roles.json`) with desk, zone and props; merged roles need new ids (for example `product-business-analyst` replacing `pm` and `ba`, PBA spec Q5). Unknown names still show as a generic monkey, so this is cosmetic, not breaking.
5. `check_roster.py` should also compare the roster with the `Agent(...)` list (today it does not, which is why B1 passes the check).
6. CHANGELOG, THIRD_PARTY_NOTICES, install with `--only`, and the headless `--allowedTools` / permission lines in `docs/agents/PERMISSIONS.md`.
7. Revisit the boss cap of **8 specialist calls per run**: one Ads Factory job could touch Creative, Writer, Artist, Video, Game & Technical, UA, QA, DS and the Code Reviewer; with fix rounds it passes 8. (I14)

## 6. Description limits (1,024 characters)

| File | Characters | Left |
|---|---|---|
| `agents/ai-engineer.md` | 876 | 148 |
| `agents/architect.md` | 640 | 384 |
| `agents/backend-engineer.md` | **1021** | **3** |
| `agents/code-reviewer.md` | 477 | 547 |
| `agents/data-scientist.md` | 771 | 253 |
| `agents/orchestrator.md` | 417 | 607 |
| `skills/ai-engineer/SKILL.md` | **1012** | **12** |
| `skills/backend-engineer/SKILL.md` | **1008** | **16** |
| `skills/code-reviewer/SKILL.md` | 691 | 333 |
| `skills/data-scientist/SKILL.md` | 925 | 99 |
| `skills/hire-an-engineer/SKILL.md` | 736 | 288 |
| `skills/orchestrator/SKILL.md` | 723 | 301 |
| `skills/software-architect/SKILL.md` | 714 | 310 |
| `skills/team-start/SKILL.md` | 561 | 463 |

(Agent counts are from the front matter, measured the same way as the validators; both validators enforce 1,024.)

Planned merges:

- **AI-Ops (already merged into AI Engineer):** fits today, but the skill has 12 characters left. Any new trigger word (for example a sixth mode or a new AI-Ops trigger) does not fit without cutting words.
- **Data Scientist & Analyst (Metrics, Report, Growth modes):** will **not fit** as written. The skill has 99 characters left; three new modes with their trigger words need an estimated 250 to 450 characters (estimate, not measured). The agent file (253 left) is tight. The description must be rewritten shorter, not extended.
- **Backend:** the merged "Backend & Integration" description would **not fit** (agent at 1021 before adding Connect and Check). The split helps: the Backend description should lose "connections to outside services ... integrations register" (about 150 characters, estimate) and the new Integration Engineer gets its own 1,024. Until the split is built, nothing can be added to the Backend description.
- New merged roles with many modes (UA & Growth 4 modes / 6 sub-roles, Writer 5, QA 5, Creative 4) will meet the same limit; write the description from the start as "role + 1 line per mode + not-for line", and measure it before review.

## 7. Status words and counts

| Count | TASKS.md | Tracker artifact (rows read) | Evidence in the files |
|---|---|---|---|
| Roles | 23 | 23 rows | ok |
| Documented | 16 | 16 | **12** meet the TASKS.md definition (role document and spec); 2, 10, 11, 15 have no spec for the merged role (I1) |
| Parts only / Not written | 4 / 3 | 4 / 3 | ok |
| Tested | 5 | 5 | Orchestrator 12 of 12 (one run each); Architect: tracker says "Data design evals 10 of 10", the role document does not say Data design was tested; Code Reviewer: TASKS 4.8 says 14 of 14, the CHANGELOG says `review-tests` not run, the tracker note says "no recorded pass rate", the role document says the sources disagree and no results file exists; AI Engineer: tracker "evals pass", document "13 of 14 + 9 of 9"; Data Scientist: TASKS "Tested (4 of 7 modes)", tracker "Tested" (note gives 4 of 7) (I1) |
| Built, not tested | 1 (Backend: "Built, not tested") | 1 (Backend: "Built") | Backend: 2 of 2 modes built, 0 tested, no `evals/backend-engineer/`, no `references/sources.md` |

Mode counts per role (from the role documents):

| # | Role | Modes | Built | Tested |
|---|---|---|---|---|
| 1 | Orchestrator | 1 (no modes) | 1 | 1 |
| 2 | Solution Architect | 2 (System design, Data design) | 2 | 1 per document, 2 per tracker |
| 3 | Code Reviewer | 1 | 1 | disputed (14 of 14 vs one case not run) |
| 4 | AI Engineer | 5 (Design/Build, Train/Evaluate, Release check, Monitor, Investigate) | 5 | 5 (13 of 14 and 9 of 9, one run each, offline) |
| 5 | Data Scientist & Analyst | 7 (Analyst, Experiment, Model, Forecast + Metrics, Report, Growth) | 4 | 4 (13 pass, 1 partial) |
| 6 | Backend Engineer | 2 (Build, Review/Fix) | 2 | 0 |
| 6b | Integration Engineer | 2 (Connect, Check) | 0 | 0 |
| 7 | DevOps | 4 | 0 | 0 |
| 8 | Security & Privacy | not set (parts) | 0 | 0 |
| 9 | QA / Test | 5 | 0 | 0 |
| 10 | Security Reviewer | 2 (Code review, Authorised test) | 0 | 0 |
| 11 | Data Engineer | 2 (Build, Repair; stated only in section 8, not in a status line) | 0 | 0 |
| 12 | Creative & Art Director | 4 | 0 | 0 |
| 13, 14, 17 | Artist, Video & Sound, Designer | not set (parts) | 0 | 0 |
| 15 | Game & Technical | 4 | 0 | 0 |
| 16 | Writer | 5 | 0 | 0 |
| 18, 20, 22 | Frontend & Mobile, Game Designer, Business Ops | not written | 0 | 0 |
| 19 | UA & Growth | 4 | 0 | 0 |
| 21 | Product & Business Analyst | 4 | 0 | 0 |

Honest totals (counting the orchestrator and the Code Reviewer as 1 mode each, and only roles whose modes are set): **15 of 54 named modes built, 11 to 13 tested** (depending on the Architect Data design and Code Reviewer evidence). "5 roles tested" is true at role level only with the labels in brackets kept.

Stale lines in `TASKS.md`: line 4 calls the live page "Agent Team Progress" (the artifact is "Agent Team Tracker"); DOC-1 and DOC-2 are unchecked although the Wave 1 documents exist; items 5.1 to 5.12 still list the pre-merge role names. (M1)

## 8. Models against the owner's table (`~/.claude/CLAUDE.md`)

| # | Role | Chosen model (where) | Owner's table says | Verdict |
|---|---|---|---|---|
| 1 | Orchestrator | opus (agent file) | planning large work: opus | ok; note: the table says the main session keeps the owner's chosen model, the agent file forces opus |
| 2 | Solution Architect | opus (roster) | architecture: opus | ok |
| 3 | Code Reviewer | opus (roster); spec says "high effort" | review: opus, high | model ok; **effort not set** |
| 4 | AI Engineer | opus | risky code, hard reasoning: opus | ok |
| 5 | Data Scientist & Analyst | opus | not listed; analysis and metric definitions are hard to undo (spec reason) | ok as an owner call; Report specs could run on sonnet later |
| 6 | Backend Engineer | sonnet (roster) | ordinary code: sonnet, **but** risky code (data formats, security, auth, migrations) is opus | **mismatch with the table's risky-code row**; the split spec keeps sonnet with the Code Reviewer as safeguard; needs the owner's explicit OK (I2) |
| 6b | Integration | opus (spec) | money, keys, outside text: opus | ok |
| 7 | DevOps | opus (spec, open Q4) | hard to undo, problems not yet understood: opus | ok |
| 8 | Security & Privacy | **none chosen** | security: opus | gap |
| 9 | QA / Test | opus (spec, open Q6) | tests for known behaviour: sonnet; verifying a fix: opus; running tests: haiku | ok if plain test runs go to haiku as the spec says |
| 10 | Security Reviewer | **none chosen** | review / security: opus | gap |
| 11 | Data Engineer | **none chosen** | ordinary code: sonnet; data formats: opus | gap |
| 12 | Creative & Art Director | opus (spec) | no row; not code | owner call; cost higher than sonnet (spec says so) |
| 13, 14, 17 | Artist, Video & Sound, Designer | none | UI / ordinary: sonnet | gap (parts only) |
| 15 | Game & Technical | **none chosen** | ordinary code: sonnet; save formats: opus | gap |
| 16 | Writer | sonnet, effort medium (spec) | docs: sonnet medium | ok |
| 19 | UA & Growth | opus (spec, open Q4) | no row | owner call; cheaper option (sonnet + DS check) is written in the spec |
| 21 | Product & Business Analyst | sonnet, medium (spec) | search, summaries: sonnet | ok |
| 18, 20, 22 | not written | none | — | — |

Cross-cutting model problems:

- **No agent file sets `effort`,** and the roster has no effort column. The owner's table says every sub-agent gets its model **and effort** set explicitly. (I2)
- **Step-up rule vs the boss's rule:** the table says a sonnet job that fails twice reruns on opus; `agents/orchestrator.md` says "use the model the roster gives; do not pick a different one". The boss cannot apply the owner's step-up rule. (I2)

## 9. Open questions of all specs, merged (38 items)

Ordered by what must be decided first. **Blocks** = building a role on the default would bake a conflict into skills, agents or evals. Every item has a default, so the owner can answer in one line (for example "Q1-Q38 haan, except ...").

### A. Decide first (cross-role, block building)

| # | Question | Sources | Default | Blocks |
|---|---|---|---|---|
| Q1 | Who keeps the held-out AI release cases, where, and who makes their recorded outputs? | AI-Ops Q1; DS merge Q3; QA Q1, Q2 | QA / Test Engineer keeps them **outside the project folder**; until QA is built, the owner keeps that folder; the owner's harness makes the outputs; the AI Engineer is never given the path | QA build, DS Metrics build, every AI-Ops release check |
| Q2 | Who writes ad copy and store-listing text? | Writer Q6; UA doc s.4 and s.5 (new conflict) | Writer writes all words (ads, store text, posts, emails); UA chooses keywords, tests, channels, spend and writes test plans | Writer and UA builds |
| Q3 | Who owns the ad test question and variant table? (new) | Creative doc s.5; UA doc s.4 | Creative owns concepts and the hypothesis per concept; UA owns the test plan, the test question, the variant table and the read | Creative and UA builds |
| Q4 | One secrets register: DevOps or Security? Who leads a leaked-key response? | DevOps Q6, decision 10; Security Engineer part s.5 (new) | DevOps owns `docs/devops/secrets-register.md`; Security & Privacy sets the rules and leads leaked-key incidents; the integrations register keeps matching key names | DevOps build, S&P merge |
| Q5 | Who does security audits: Security Reviewer or Security & Privacy Engineer? (new) | Architect doc s.4/s.7; Security Engineer part; Security Reviewer doc | Security Reviewer audits and tests; Security & Privacy builds safeguards, threat models, privacy guidance and leads security incidents | S&P merge, Security Reviewer build |
| Q6 | Who owns tracking code (client SDK calls, server events, ingestion)? (new) | DS doc; UA doc; Data Engineer doc silent | DS writes the tracking plan; Game & Technical (game client) and Backend (server) write the event calls; Data Engineer owns ingestion, checks and storage; Integration owns third-party analytics/attribution SDK setup | Data Engineer spec, DS Metrics, Game & Technical spec |
| Q7 | Who owns release notes? (new) | Writer doc; DevOps doc | Writer writes the plain notes; DevOps release plan links to them; `CHANGELOG.md` stays with the engineers / base skill unless the brief names the Writer | Writer, DevOps builds |
| Q8 | Models and effort for every agent; may the boss apply the step-up rule? | Integration split Q2; DevOps Q4; QA Q6; UA Q4; PBA Q4; Backend merge Q3 (obsolete); owner's table (new) | Spec defaults (section 8 table); effort column added to the roster (high for opus review/security roles, medium otherwise); the boss may step a sonnet role up to opus after two failures and must say so | every agent file |
| Q9 | Tool-level guards: one policy for live commands and network calls | DevOps Q3 (default yes); Integration split Q5 (default no) | One rule for both: a PreToolUse guard for live and network commands in roles that hold keys or deploy (DevOps, Integration); others rely on the rule plus evals | DevOps, Integration builds |

### B. Decide before the matching build (have safe defaults)

| # | Question | Sources | Default |
|---|---|---|---|
| Q10 | Who presses live buttons (deploy, store submit, rollout halt, spend, post, send, sign)? | DevOps Q1; UA Q3 | the owner; one more named person per project allowed |
| Q11 | Standing approval for test-system (sandbox) calls? | Backend merge Q1; split Q1 | one standing approval per provider and test key, recorded in the register; live keys always need a fresh approval |
| Q12 | Who owns the webhook receiving route? | split Q3 | Integration Engineer, calling a backend function for the business step |
| Q13 | Recurring data collection before the Data Engineer exists? | Backend merge Q2; split Q4 | Integration writes one simple job marked "hand over to Data Engineer" |
| Q14 | Scheduled runs (AI Monitor, Integration Check, DevOps monthly check, PBA status reports)? | AI-Ops Q2; merge Q4; split Q6; DevOps Q7; PBA Q7 | none; on request only |
| Q15 | Live read-only connectors (Pubforce, Adjust, email tool, helpdesk, task boards)? | DS Q2; UA Q2; Writer Q4; PBA Q2 | no; exports only |
| Q16 | Live eval harness and budget per run? | AI-Ops Q3 | none; offline runs on recorded outputs only |
| Q17 | Standing approval for one pre-written rollback? | DevOps Q2 | no; every rollback is an approval, prepared as one step |
| Q18 | Hosts, stores and build tools? | DevOps Q5 | GitHub Actions + the host's own deploy; store test tracks first |
| Q19 | Image and video tools: which, who runs them, ever give the role a generation tool? | Creative Q1, Q3 | a human runs them; the role writes prompt packs only; revisit when the Artist is built |
| Q20 | Build Creative & Art Director before or with the Artist? | Creative Q6 | together |
| Q21 | Does each game have a brand or style guide? | Creative Q2 | none; the role drafts, the owner approves |
| Q22 | Final sign-off on art before it ships? | Creative Q4 | the owner, after Art QA |
| Q23 | Markets and children's rules? | Creative Q5; UA Q5 | UK, US, EU rules flagged; audience age unknown, children's rules flagged every time; a lawyer decides |
| Q24 | Real players for playtests? | QA Q3 | no; QA writes the plan, the owner runs sessions |
| Q25 | Test copy of live services for load tests? | QA Q4 | no load test until one exists |
| Q26 | Target device floor? | QA Q5 | one mid-range Android the owner has + phone-size browser |
| Q27 | Who builds dashboards from the specs? | DS Q1 | the owner |
| Q28 | Which metrics are already official? | DS Q4 | none; every line starts `draft` |
| Q29 | Which ad channels matter now? | UA Q1 | those in the campaign exports |
| Q30 | May UA read and adapt the installed marketing skills? | UA Q6 | yes, after a licence check, with credit |
| Q31 | Who checks each language; which languages first? | Writer Q1, Q2 | nobody assumed; only languages the owner names; all lines stay `machine draft` |
| Q32 | Written refund and support policy? | Writer Q3 | none; no promises; point to the store refund route |
| Q33 | Who approves claims in store copy and ads? | Writer Q5 | the owner; legal-sensitive goes to a lawyer |
| Q34 | PBA folder? | PBA Q1 | `docs/product/`, continuing existing layout files when named |
| Q35 | Who runs interviews? | PBA Q3 | the owner or their team |
| Q36 | Paid research sources? | PBA Q6 | none |

### C. Housekeeping (no build blocked)

| # | Question | Sources | Default |
|---|---|---|---|
| Q37 | What happens to superseded documents (`backend-integration-engineer.md`, `art-qa.md`, `storyboard-scriptwriter.md`, `performance-ua-marketer.md`, `backend-integration-merge.md`)? | UA Q7; Writer call 6; QA call 5 | add a one-line "Superseded by ..." note at the top now; move to an `archive/` folder when the merged role is built |
| Q38 | Office characters for merged roles (one id per merged role, for example `product-business-analyst`)? | PBA Q5 | yes, one character per merged role, added when the role is built |

## 10. Findings by severity

### Blockers (fix or decide before building any further role)

- **B1. The boss cannot call the Backend Engineer, but is told to use it.** `agents/orchestrator.md` allows `Agent(architect, code-reviewer, ai-engineer, data-scientist)`; the roster lists `backend-engineer`; `skills/orchestrator/references/team-roster.md` line 19-20 routes migrations and server code to `backend-engineer`. Every build job in a team run falls to the "general helper" path. `check_roster.py` does not catch it. Fix (after the Backend evals pass): add the name to the `Agent(...)` list and the description; extend `check_roster.py` to compare roster and allowlist.
- **B2. Held-out AI cases: two conflicting defaults and no real keeper.** QA merge spec default QA; DS merge spec default DS (its condition "if AI-Ops modes are built" is already met). Neither QA nor DS keeps them today, so every AI-Ops release check so far was judged without a held-out set the builder could not see. Any location inside the project is readable by the AI Engineer (Read/Grep/Glob). Decide Q1.
- **B3. Ad copy and store-listing text have two owners.** Writer (document s.3 "ad copy", "store copy"; spec Q6 default "Writer writes the words") vs UA & Growth (document: "writes ad copy and store text", "short marketing copy"). Building either role now bakes the conflict into its skill. Decide Q2.
- **B4. Tracking code has no owner that accepts it.** DS and UA send it to the Data Engineer; the Data Engineer document does not list tracking code or SDKs; client-side events in a Unity game are named by nobody. The Ads Factory needs this data first. Decide Q6, then write it into the Data Engineer spec.
- **B5. Three "Documented" roles have no spec, and specs are what the build plan runs from.** Security Reviewer (10), Data Engineer (11), Game & Technical Engineer (15); and the Solution Architect's Data design merge has no spec of its own. A build cannot follow the agent template's "spec first" step for 10, 11 and 15. Write the three specs (with open questions and defaults) before building them.

### Important

- **I1. Status words say more than the evidence.** "Documented" counted 16; by the TASKS.md definition 12. "Tested" 5 at role level, but Code Reviewer's 14 of 14 has no results file and the CHANGELOG disagrees; DS is 4 of 7 modes; tracker drops "(4 of 7 modes)" and "not tested" from labels; AI Engineer "evals pass" while one case of 14 fails. Keep the bracketed labels in both TASKS.md and the tracker.
- **I2. Models and effort.** No agent file sets `effort`; no roster effort column; Backend on sonnet against the owner's "risky code: opus" row without the owner's explicit OK; no model chosen for 8, 10, 11, 15; the boss's "never change the roster model" rule blocks the owner's step-up rule. Decide Q8.
- **I3. Tracking plan vs tracking code** (see B4) also leaves the DS Metrics mode without a builder for what it specifies.
- **I4. Secrets register has two owners** (DevOps `docs/devops/secrets-register.md`; Security Engineer part "list of keys and services"). Decide Q4 and remove the duplicate in the S&P merge.
- **I5. Security audits have two owners and two routes.** Architect document sends deep audits to the Security & Privacy Engineer; the AI document and the Security Reviewer document send them to the Security Reviewer; the Security Engineer part runs its own "security pass". Decide Q5.
- **I6. Security incidents have no documented owner.** DevOps hands them to the Security & Privacy Engineer, whose Incident Responder part does not exist; the Security Engineer part says it does not lead incidents.
- **I7. Release notes have two owners** (Writer Technical docs mode; DevOps release plan "notes"), and the Writer may edit `CHANGELOG.md`, which the engineers and the base skill also maintain. Decide Q7.
- **I8. Ad test question and variant table have two owners** (Creative "the test question for each concept", "variant table"; UA "names the test question"). Decide Q3.
- **I9. Five asset / licence / image registers** (Creative, Concept part, 2D part, Video part, Game & Technical package list). Settle one register owned by the Creative & Art Director in the Artist merge; others add rows through the boss.
- **I10. Pipeline files have two writers** (DevOps owns pipeline files; Security Engineer part writes "pipeline security settings"). In the S&P merge, make security settings a review or a request to DevOps.
- **I11. Retired role names still in live files.** `ua-growth-marketer.md` (2 places, "Backend & Integration Engineer", for email sending code); `skills/orchestrator/references/team-roster.md` line 19; `skills/software-architect/references/data-design.md` line 23. The two skill files are installed, so the boss and the architect use the old name at run time. (Skill files were not edited by this review.)
- **I12. Scripts and storyboards in three folders** (Writer `docs/writing/storyboards/`; Creative spec `docs/creative/scripts/`; old `docs/storyboards/`). Remove `docs/creative/scripts/` from the Creative spec (the Writer owns scripts; the Creative document does not list that folder either).
- **I13. Superseded documents sit next to live ones** with different folders and status labels (`backend-integration-engineer.md` still says "Built (2 of 4 modes)"). A builder following the template can open the wrong one. Add a "Superseded by ..." line at the top (Q37).
- **I14. The boss's cap of 8 specialist calls per run** will be hit by one full Ads Factory job once the creative and growth roles exist (second-order effect of adding roles). Decide whether the cap is per run or per stage before those roles are built.

### Minor

- **M1.** `TASKS.md` stale lines: "Agent Team Progress" name, DOC-1/DOC-2 unchecked, Phase 5 lists pre-merge names.
- **M2.** The Description limits leave almost no room (Backend agent 3, AI skill 12, Backend skill 16 characters). Not failing, but the next edit will fail validation; plan shorter descriptions (section 6).
- **M3.** Backup and restore: the Architect document claims "the evidence that a restore was tried"; DevOps decision 8 gives the restore test to the Backend Engineer. Change the Architect line to "the restore test design; the Backend Engineer runs it".
- **M4.** `ai-engineer.md` section 4 has two near-duplicate legal bullets ("Give legal advice ..." and "Give legal certificates ...").
- **M5.** `ux-ui-designer.md` names retired roles (Accessibility Specialist, Art Director, Content Writer, Product Manager, UX Researcher, Frontend Engineer) and an unowned folder `docs/art-direction/`. Fix in the Designer merge.
- **M6.** Usability research has no document (UX Researcher part missing); the PBA document already points to the Designer for it.
- **M7.** Social replies: UA spec says replies to players are drafts; the Writer Support mode owns support replies. Say in the UA document that support replies go to the Writer.
- **M8.** "Performance sheet" is the name of two different files (Game & Technical, QA). Rename one (for example "build budget sheet").
- **M9.** Three data dictionaries (design, code, pipelines) are on purpose; add one line to each saying which wins on conflict (the code one for what exists, the design one for what is planned).
- **M10.** `tests/` folder: builders' unit tests and QA's end-to-end tests have no written folder split.
- **M11.** `docs/analysis/` and `docs/analytics/` inside one role are easy to confuse; consider `docs/analytics/` for both with sub-folders.
- **M12.** Status line style differs: built roles start with "Status:", others with "This role is not built yet"; the Data Engineer's 2 modes are only in section 8. One status line format in every document makes the counts checkable by a script.

## 11. Pre-mortem: "It is one month later and the team failed. Why?"

1. The boss ran the first real job, could not call the Backend Engineer, used a general helper, and the helper wrote migrations without the Backend's rules (B1).
2. The AI Engineer grepped the project, found the held-out cases, and its prompt was tuned to the test (B2).
3. Writer and UA both wrote the store listing; two versions reached the owner and nobody knew which was approved (B3).
4. The Ads Factory dashboard was empty because nobody built the event calls (B4).
5. The owner trusted "Tested" for a role whose evals never ran (I1).
6. A builder opened `backend-integration-engineer.md` instead of `integration-engineer.md` and the new agent wrote to `docs/backend/integrations/` (I13).
7. A description edit pushed a skill over 1,024 characters and the release check failed on the day of release (section 6).
8. The owner got 38 questions spread over 9 specs, answered half, and builds started on the unanswered defaults that conflict (section 9).

Each of these maps to a finding above with a fix or a default.

## 12. Recommended build order

The constraint today is **not** writing documents. It is (a) the owner's decisions, (b) the boss's ability to call specialists, and (c) the review gate, which is the Code Reviewer alone. Work that does not move these three does not raise the team's real output.

| Step | What | Why this order |
|---|---|---|
| 0 | **Decide Q1-Q9** in one message (defaults offered), add "Superseded by" lines (Q37), fix retired names in the two installed skill files, add the roster-vs-allowlist check. No new role. | Cheapest step; removes every blocker that would be copied into new skills and evals. |
| 1 | **Backend Engineer evals** (catch-up baseline, as the split spec says), then add it to the boss's list. | Already built; the only engineer role; unblocks the real-project trial (TASKS 6.3a). |
| 2 | **QA / Test Engineer**, Test mode first, plus the held-out case keeper. | Second independent gate after the Code Reviewer; every later builder needs it; makes AI-Ops release checks honest (B2). |
| 3 | **Integration Engineer** (split), moving the register out of `docs/backend/` and shrinking the Backend description. | Ads Factory foundation needs ad-network and analytics connections; money and keys need the stricter role. |
| 4 | **DevOps Engineer**. | Nothing goes live without release plans, rollback notes and the secrets register. |
| 5 | **Security & Privacy merge document + spec**, then the **Security Reviewer spec and build**. | Must exist before any live launch; settles Q4, Q5 and security incidents. |
| 6 | **Data Engineer spec and build**, then the **DS Metrics / Report / Growth modes** (with a shorter description). | Tracking (Q6) and metrics come before the growth roles that read them. |
| 7 | **Creative & Art Director together with the Artist merge**, then **Writer**, **Video & Sound Editor** (merge first), **Game & Technical** (spec first). | Creative lanes of the Ads Factory; build Creative and Artist together (Creative Q6) so briefs have a receiver. |
| 8 | **UA & Growth Marketer**. | Needs settled lines with Writer (Q2), Creative (Q3) and DS (Q6) first. |
| 9 | **Designer** (merge first), **Frontend & Mobile**, **Product & Business Analyst**, **Game Designer**, **Business Operations**. | Marked "Not needed for Ads Factory" or not written; other documents already point to them, so write the three missing documents before step 7 hand-offs are relied on. |

After each step, re-run the five checks and pytest, update the roster, the boss's list and the office, and re-count the status words with the bracketed labels.
