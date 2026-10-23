# Agent team: task list

Source of truth for progress. `[x]` done, `[~]` in progress, `[?]` waiting for owner, `[ ]` to do.
Master plan: `docs/superpowers/specs/2026-10-22-agent-team-master-plan.md`. Live view: Artifact "Agent Team Progress".


## Phase 0 Plan & spec

- [x] 0.1 Architect agent design spec (written, builder-checked)
- [x] 0.2 Master plan for the whole agent team
- [x] 0.3 Task list in repo (TASKS.md) + live progress page
- [x] 0.4 Owner approves Architect spec and master plan
- [x] 0.8 Owner reviews implementation plan and picks execution method
- [x] 0.5 Commit specs on feat/specialized-agents
- [x] 0.6 Implementation plan for Phases 1-2 (writing-plans)
- [x] 0.7 Second-wave roles researched; ownership rules and human-approval rule added to master plan

## Phase 1 Contract & template

- [x] 1.1 Handoff contract: what boss sends, what specialist returns (done, reviewed)
- [x] 1.2 Agent template (agent file + skill folder + 10-step checklist) in docs/agents/agent-template (done)
- [x] 1.3 Validator and packager support for agents/ (done, reviewed)
- [x] 1.4 Install script + INSTALL.md section (copy to ~/.claude) (done, reviewed; now with --only; real install only after owner OK)
- [x] 1.5 Eval pattern for agents (typical, edge, refusal cases) and sources/evals checkers (done, whole-branch review passed after one fix wave)
- [x] 1.6 Event log in the contract: every agent start, stop, handoff and file written is one line in .agents/events.jsonl (feeds the visual office) (done, reviewed)

## Phase 2 Architect

- [x] 2.1 sources.md: 123 sources, 86 verified / 37 unverified; fact-check of 25 verified rows found no mismatch (5 links bot-blocked, check in a browser)
- [x] 2.2 core-principles, method-design, method-recover, review-checklists (done; commands verified on a throwaway repo)
- [x] 2.3 Field references: web/backend/cloud, distributed/data, mobile, desktop/plugins, game/engine, real-time/netcode, AI systems, security, data pipelines (done, 9 files)
- [x] 2.4 diagrams.md (C4, Mermaid default; 6 templates rendered and checked in a browser) (done)
- [x] 2.5 SKILL.md router and agents/architect.md (done)
- [x] 2.6 Evals written first: 12 cases + test project; re-review done (4 Important items fixed, 4 further fixes applied)
- [x] 2.7 Evals run, fixed, rerun: 7 of 7 first-batch cases pass; the 2 recover cases were run by the owner in fresh sessions
- [x] 2.8 THIRD_PARTY_NOTICES, CHANGELOG (done), whole-branch review fixes (done); installed copy of skill + agent in ~/.claude (done 2026-10-23, identical to repo; hire-an-engineer untouched)
- [?] 2.9 Commit; release software-architect 0.1.0 (only when owner says)

## Phase 3 Second specialist

- [x] 3.1 Code Reviewer chosen; spec approved by the owner; plan written; 87 sources written (81 verified); evals written first (14 cases + test repo with planted defects, local)
- [x] 3.2 Knowledge files, SKILL.md and agent built; 10 of 11 evals pass (review-tests not run); installed in ~/.claude with --only; independent review of the knowledge files still pending
- [x] 3.3 Contract tested on two agents (Architect and Reviewer both answered in the 7-field shape; one wording gap fixed: questions may ride with needs_approval)

## Phase 4 Orchestrator

- [x] 4.1 Orchestrator design spec written and approved by the owner; Claude Code docs checked (boss runs in the main session, claude --agent works, subagents can nest)
- [x] 4.2 Built: skill (SKILL.md + 7 references), agents/orchestrator.md, roster.md + check_roster.py (tests first), 58 sources (57 verified); installed in ~/.claude with --only (10 files, identical to repo)
- [x] 4.2b Roster check, agent validator, 125 tests pass; skill fixed after eval (run folder for every specialist run, boss never redoes a specialist check)
- [x] 4.3 Evals: all 12 cases pass (headless, stub and real specialists); fixes made along the way: run folder for every run, no self-checking, real UTC timestamps, event log always written, roster models, who reviews designs. Complex end-to-end test on the shop code with the real team passed (7 specialist calls, ADR written and reviewed 3 times)
- [x] 4.4 CHANGELOG entries for code-reviewer and orchestrator (done)
- [?] 4.5 Release orchestrator 0.1.0 (only when the owner says; nothing is released now)
- [x] 4.6 Hardening: team_event.py (boss writes events with a script, validated, real UTC time) + check-run (automatic run folder gate), hook and boss events share one run_id (done, 313+ tests)
- [x] 4.7 Permission rules: specialists cannot write .agents/ (tested in main session and subagent); event script allowed; headless needs --allowedTools (tested); caveats in docs/agents/PERMISSIONS.md
- [x] 4.8 Code Reviewer 14 of 14 evals pass after fixes; Architect sources 122 of 123 verified (+78 game sources); game references deepened (4 files), architect asks architecture-changing questions before writing files
- [x] 4.9 Code Reviewer safe test runner (run_tests_safe.py: scratch copy, stripped environment, timeout; tested on a real review) + owner-language rule for boss and specialists (done)

## Phase 5 Remaining roles

- [?] 5.1 ON HOLD, owner will say which roles to build: Group A Product: PM, Business Analyst, Researcher, Delivery Manager
- [?] 5.2 ON HOLD, owner will say which roles to build: Group B Design: UX Researcher, UX/UI, Motion, Content writer
- [?] 5.3 ON HOLD, owner will say which roles to build: Group C Engineering: Frontend, Backend, Mobile, Game, Integration, AI/ML, Data
- [?] 5.4 ON HOLD, owner will say which roles to build: Group D Quality & security: QA, Reviewer, Performance, Accessibility, Security, Privacy
- [?] 5.5 ON HOLD, owner will say which roles to build: Group E Release & ops: DevOps, SRE, Release Manager, Technical Writer, Support
- [?] 5.6 ON HOLD, owner will say which roles to build: Group F Growth: Analytics, ASO/SEO/Marketing
- [?] 5.7 ON HOLD, owner will say which roles to build: Wave 2 Art & creative: Creative Director, Art Director, Concept Artist, 2D Artist, 3D Artist, Animator, VFX, Technical Artist, Sound Designer, Video Editor, Storyboard/Scriptwriter, Art QA
- [?] 5.8 ON HOLD, owner will say which roles to build: Wave 2 Game design: Game Designer, Level Designer, Systems/Economy Designer, Live-Ops Manager, Playtest QA
- [?] 5.9 ON HOLD, owner will say which roles to build: Wave 2 Data & AI: Data Scientist, BI Developer, Prompt/AI-Ops (+ modes: Data Analyst, applied AI Engineer)
- [?] 5.10 ON HOLD, owner will say which roles to build: Wave 2 Marketing: Ad Marketer, Performance/UA Marketer, Social/Community, Influencer/PR, Email/CRM
- [?] 5.11 ON HOLD, owner will say which roles to build: Wave 2 Business (draft-only, human signs off): HR, Finance, Legal, Sales, Operations, Localisation
- [?] 5.12 ON HOLD, owner will say which roles to build: Wave 2 Web modes: Web Designer (UX/UI mode), Web Developer (Frontend mode)

## AI Engineer

- [x] AI-1 Build evals, knowledge files and agent file, then run the evals and fix failures (headless agent working; owner approved the role file)
- [x] AI-2 Checks: validate_agents, validate_skills, check_sources, check_evals, full pytest; read the eval table
- [x] AI-3 Add to roster, boss allowlist, team-roster, CHANGELOG, THIRD_PARTY_NOTICES; set Tested if evals pass
- [x] AI-4 Install with --only, commit and push (only after the owner says OK)

## Data Scientist

- [x] DS-1 Build evals, knowledge files and agent file, then run the evals and fix failures (headless agent working; owner approved the role file)
- [x] DS-2 Checks: validate_agents, validate_skills, check_sources, check_evals, full pytest; read the eval table
- [x] DS-3 Add to roster, boss allowlist, team-roster, CHANGELOG, THIRD_PARTY_NOTICES; set Tested if evals pass
- [x] DS-4 Install with --only, commit and push (only after the owner says OK)

## Visual office

- [x] OFF-1 Own characters, props, desks and a Data & AI zone for AI Engineer and Data Scientist in the live office UI (agent working)

## Role documents

- [ ] DOC-1 Gemini CLI installed (done); you log in once: run gemini in a terminal, then /auth
- [ ] DOC-2 Wave 1 role documents with Gemini research: Backend, Database Architect, DevOps, Security Engineer, QA/Test, AppSec Reviewer

## Phase 6 Integration

- [x] 6.1 Router row in hire-an-engineer pointing to the team (done in repo and installed copy; CHANGELOG 0.4.0 Unreleased); branch merged with main (0.2.1, 0.3.0)
- [x] 6.2 Plugin bundle: ruled not worth it yet (install scripts copy skills, agents and the office with --only / --project; revisit when more roles exist)
- [?] 6.3 End-to-end test building a small real app with the whole team: needs engineer roles (not built yet); an analysis, design and review run on real code passed several times
- [?] 6.3a FIRST finish the roles the owner names for the real trial (owner will say which), THEN real-project trial: run the team on one of the owner's real projects (game or app), 3 real jobs, log every miss, fix the skills
- [?] 6.4 Docs (INSTALL, PERMISSIONS, LAUNCH, INSTALL-OFFICE) and CHANGELOG done; release of the agents (0.1.0 each) and hire-an-engineer 0.4.0 only when the owner says
- [x] 6.5 Automatic team start in any folder: team-start global skill asks one question (team or solo), setup_team.py one command, global rule in CLAUDE.md and guarded global hooks (both reversible); tested in new empty folders

## Phase 7 Visual office

- [x] 7.1 Design final: mock v2 (docs/agents/visual-office/mock-v2.html) approved by the owner on 2026-10-23 (all three themes and layouts stay switchable; no more mocks). Implement and test this; new roles are added to the office as they are built
- [x] 7.2 Implementation spec written: docs/agents/visual-office/event-mapping.md (event to scene mapping, new boss events, role registry, test plan) and research-channel.md (window to session channel options)
- [x] 7.3 Event pipeline done: server (/events /roster /state /answer), hook launcher, boss events via team_event.py, one shared run_id
- [x] 7.4 Live UI built from mock v2 (docs/agents/visual-office/index.html), tested on real logs in all 3 themes and layouts
- [x] 7.5 Boss opens the office automatically (SessionStart hook, tested headless, server survives the session); answers in the window or the terminal via the office MCP tool (42 tests, real CLI tested; interactive behaviour and Desktop app unverified)
- [x] 7.6 Tested with real problems: the boss, Architect and reviews on the shop code, 4 live runs; found and fixed 8 problems (event format, permissions, install location, run_id, files tab)
- [x] 7.7 Truth check: replayed a real log against a reference timeline (25 cut points, 9 theme/layout combinations): see docs/agents/visual-office/truth-check-report.md
- [x] 7.8 Package and install: scripts/install_office.py (office into any project) + INSTALL-OFFICE.md; verified on a fresh project: install, boss run (one run_id, check-run OK), hook launch
- [x] 7.9 Review round (thinking skills): window answers off by default (server and installer), Your move strip, labels say who needs what and why, quiet-run warning, parked runs, /truth disk check, specialist calls N of 8 (done)
- [x] 7.10 Polish from the owner's tests: owner label Your OK needed, cards say what to answer (a1 haan), boss keeps handed-back one-way doors open, full brief text on hover, boss default agent per project

## Roles (22): the merged list (owner decisions 2026-10-24)

Small roles are merged into bigger ones with modes; Backend and Integration were split for a short time and are merged again (role 6, four modes). Order follows the Ads Factory build order. Details and next steps for each role are in `docs/superpowers/specs/` and `docs/agents/roles/`.

Documentation: Not written / Parts only / Documenting (role document written, spec still needed) / Documented (role document and spec done). Build: Not started / Built, not tested / Tested.

| # | Role | Sub-roles | Documentation | Build |
|---|---|---|---|---|
| 1 | Orchestrator | The boss | Documented | Tested |
| 2 | Solution Architect | Architect + Database Architect | Documented | Tested |
| 3 | Code Reviewer | Code Reviewer | Documented | Tested |
| 4 | AI Engineer | AI Engineer + Prompt / AI-Ops | Documented | Tested |
| 5 | Data Scientist & Analyst | Data Scientist + Data Analyst + BI Developer + Analytics / Growth Analyst | Documented | Tested (5 of 5 modes; BI / Analytics 10 of 10 runs, older cases 15 of 15) |
| 6 | Backend & Integration Engineer | Backend Engineer + Integration Engineer (modes: Build, Review/Fix, Connect, Check) | Documented | Tested (4 of 4 modes; 13 of 13 local evals after 1 fix, one run each) |
| 7 | DevOps Engineer | DevOps + SRE / Monitoring + Release Manager | Documented | Not started |
| 8 | Security & Privacy Engineer | Security Engineer + Threat Modeler + Incident Responder + Privacy / Compliance | Documented | Not started |
| 9 | QA / Test Engineer | QA + Playtest QA + Art QA + Performance + Accessibility | Documented | Built, not tested |
| 10 | Security Reviewer | AppSec Reviewer + Penetration Tester | Documented | Not started |
| 11 | Data Engineer | Data Engineer | Documented | Not started |
| 12 | Creative & Art Director | Creative Director + Art Director | Documented | Not started |
| 13 | Artist | Concept Artist + 2D Artist + 3D Artist + Animator + VFX Artist | Documented | Not started |
| 14 | Video & Sound Editor | Video Editor + Sound Designer | Documented | Not started |
| 15 | Game & Technical Engineer | Game / Unity Engineer + Technical Artist | Documented | Not started |
| 16 | Writer | Content Writer + Storyboard / Scriptwriter + Technical Writer + Support Analyst (Localisation parked) | Documented | Built, not tested |
| 17 | Designer | UX/UI Designer + Graphic & Motion Designer + Web Designer + UX Researcher | Documented | Not started |
| 18 | Frontend & Mobile Engineer | Frontend + Mobile + Web Developer | Not written | Not started |
| 19 | UA & Growth Marketer | Performance / UA + Ad Marketer + ASO / SEO + Social + Influencer / PR + Email / CRM | Documented | Built, not tested |
| 20 | Game Designer | Game Designer + Level + Systems / Economy + Live-Ops | Not written | Not started |
| 21 | Product & Business Analyst | Product Manager + Business Analyst + Market Researcher + Delivery Manager | Documented | Not started |
| 22 | Business Operations | Finance + Operations / Procurement + Sales / Account + HR + Legal (draft only) | Not written | Not started |
| 27 | Project Manager | Plan + Track (drift check) + Release readiness + Retro | Documented | Not started |
| 28 | Software Engineer | Structure applied + Algorithms and data structures + Performance and resources | Documented | Not started |

## Backlog: one place for all later work (owner request 2026-10-24, X5)

Do not build everything at once. Phase 1: make the current system solid with the 6 built roles on a real job. Phase 2: build the documented roles one at a time (order: QA / Test Engineer, DevOps, Security & Privacy with Security Reviewer, Data Engineer, the creative group (Creative & Art Director with Artist, Designer, Writer, Video & Sound Editor), UA & Growth, Product & Business Analyst, Game & Technical Engineer, then Project Manager and Software Engineer). Phase 3: grow roles with the lists below. Every build follows the 'Also part of every build' list in `docs/agents/agent-template/README.md`. Nothing below is started.

### List A: new roles (kept apart from the rest)
- [ ] A1 Project Manager: documented (role document and spec written)
- [ ] A2 Software Engineer: documented (role document and spec written)
- [ ] A3 Game Designer (game design, level, systems and economy, live-ops and monetisation, narrative): document not written
- [ ] A4 Frontend & Mobile Engineer (frontend, mobile, web, UI code from the Designer's screens): document not written
- [ ] A5 The 4 team helpers (Personal Assistant, Automation Engineer, Learning Agent, R&D Agent): documents drafted, builds later in their own order
- [ ] A6 Later, only if needed: IT / helpdesk

### List B: updates and new skills for roles that are already built (6 roles)
**Orchestrator**
- [ ] B1 Add each new role to its allowlist, `team-roster.md` and the roster when that role is built (part of every build).
- [ ] B2 Add the step-up rule (a sonnet role goes to opus after two failed runs) and the effort column.
- [ ] B3 Write a lesson to `docs/lessons/<role>.md` when the owner reports an issue (decision X2).
- [ ] B4 Save the eval results file (12 of 12, one run each) if it is missing.
**Solution Architect**
- [ ] B5 Add the Project structure mode (spec written, 27 evals planned; description fits: 904 and 946 of 1,024).
- [ ] B6 Move the 40 data design sources from the role document into the skill, so an installed copy can find them.
- [ ] B7 Back the "Tested" label: save results for the 15 system design cases; rerun the 3 relaxed data design cases.
**Code Reviewer**
- [ ] B8 Run the case `review-tests` that was never run, and save a results file with the pass rate of the 14 evals.
**AI Engineer**
- [ ] B9 Held-out cases: run the release check on two files (open set for the AI Engineer, held-out set kept by QA outside the project), opaque case ids like `h01`; fix `agents/ai-engineer.md` lines 50 and 83 and `eval_compare.py` (decision Q1).
- [ ] B10 Save the AI-Ops results file (9 of 9, offline, one run each) if it is missing.
**Data Scientist & Analyst**
- [ ] B11 Make room in the descriptions (skill 978, agent 1,016 of 1,024) before any new mode.
- [ ] B12 Add the read-only live access tool when it exists (decision Q15) and test that it cannot edit or save.
- [ ] B13 Fix the `pii-read-preview` fixture quirk (login day and sessions are independent) and rerun that case.
**Backend & Integration Engineer** (one role, 4 modes: Build, Review/Fix, Connect, Check)
- [ ] B14 Make room in the descriptions: agent 1,019 and skill 1,017 of 1,024.
- [ ] B15 Rerun the evals twice per case and report "k of n runs"; rerun the 12 cases that were not rerun after the fix.
- [ ] B16 Trial through the boss on one real job.
- [ ] B17 Add the PreToolUse guard for live and network commands (decision Q9) and test it.
- [ ] B18 Live providers stay uncalled (mocks and test keys only) until the owner approves a test-system run.
**All built roles**
- [ ] B19 Add `docs/lessons/<role>.md` to each role's reading list.
- [ ] B20 Decide whether to split Backend and Integration again later (kept as one role for now).

### List C: wider responsibilities planned for documented roles (include when each role is built)
- [ ] C1 DevOps: FinOps (AI and cloud cost) and platform and store submission
- [ ] C2 Security & Privacy: AI safety and responsible AI
- [ ] C3 UA & Growth Marketer: community (answering players, reviews)
- [ ] C4 Data Engineer: dataset curation and labelling
- [ ] C5 Writer: Localise mode (parked, English only for now)
- [ ] C6 Architect, Software Engineer and Project Manager: align the lines between them (the Architect spec was written before the other two existed)
- [ ] C7 Product & Business Analyst: now 3 modes; drop the Delivery tracking part when it is built

### List D: checks and small items
- [ ] D1 Verify the 3 sources that now open and mark them verified in the skill `sources.md` files.
- [ ] D2 Owner: look at the office window once (seats, tags, Waiting state) and report anything wrong.
