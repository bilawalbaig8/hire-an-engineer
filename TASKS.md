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

## Roles (22): the merged list of 22 (owner decision 2026-10-24)

Small roles are merged into bigger ones with modes. The old 70-role list is replaced; order follows the Ads Factory build order.

| # | Role | Wave | Status | Includes | Why |
|---|---|---|---|---|---|
| 1 | Orchestrator | 0 Built or in build | Tested | The boss | Talks to you, hands out work, keeps the run record |
| 2 | Solution Architect | 0 Built or in build | Tested | Architect + Database Architect | System design and data design |
| 3 | Code Reviewer | 0 Built or in build | Tested | Code Reviewer | Reads changes for mistakes; stays apart from the builders |
| 4 | AI Engineer | 0 Built or in build | Tested | AI Engineer + Prompt / AI-Ops | The AI part of products and agent teams (evals 13 of 14 pass) |
| 5 | Data Scientist & Analyst | 0 Built or in build | Tested | Data Scientist + Data Analyst + BI Developer + Analytics / Growth Analyst | Honest answers from data, tests, forecasts, dashboards (evals 13 of 14 pass) |
| 6 | Backend & Integration Engineer | 0 Built or in build | In progress | Backend Engineer + Integration Engineer | Server code and outside services; the backend part is built |
| 7 | DevOps Engineer | 1 Foundation (Ads Factory steps 1-2) | Not started | DevOps + SRE / Monitoring + Release Manager | Build, deploy, run, watch and release |
| 8 | Security & Privacy Engineer | 1 Foundation (Ads Factory steps 1-2) | Not started | Security Engineer + Threat Modeler + Incident Responder + Privacy / Compliance | Builds the safeguards, thinks like an attacker at design time, plans for incidents, guards personal data |
| 9 | QA / Test Engineer | 1 Foundation (Ads Factory steps 1-2) | Not started | QA + Playtest QA + Art QA + Performance + Accessibility | Checks that the whole thing really works; stays apart from the builders |
| 10 | Security Reviewer | 1 Foundation (Ads Factory steps 1-2) | Not started | AppSec Reviewer + Penetration Tester | Reads code for security mistakes and tests your own systems with permission; never builds |
| 11 | Data Engineer | 1 Foundation (Ads Factory steps 1-2) | Not started | Data Engineer | Moves and shapes data so others can trust it |
| 12 | Creative & Art Director | 2 Creative lanes (steps 4-6) | Not started | Creative Director + Art Director | The big idea and the visual direction; judges the art, never makes it |
| 13 | Artist | 2 Creative lanes (steps 4-6) | Not started | Concept Artist + 2D Artist + 3D Artist + Animator + VFX Artist | Concepts, final art and motion for games and ads |
| 14 | Video & Sound Editor | 2 Creative lanes (steps 4-6) | Not started | Video Editor + Sound Designer | Cuts, captions, exports and audio for ads |
| 15 | Game & Technical Engineer | 2 Creative lanes (steps 4-6) | Not started | Game / Unity Engineer + Technical Artist | Gameplay code and the bridge between art and engine |
| 16 | Writer | 2 Creative lanes (steps 4-6) | Not started | Content Writer + Storyboard / Scriptwriter + Localisation + Technical Writer + Support Analyst | Words: scripts, copy, translations, docs and support answers |
| 17 | Designer | 2 Creative lanes (steps 4-6) | Not started | UX/UI Designer + Graphic & Motion Designer + Web Designer + UX Researcher | Screens, flows, graphics and brand pieces |
| 18 | Frontend & Mobile Engineer | 3 Approval and launch (step 9) | Not started | Frontend + Mobile + Web Developer | What people see and touch, including approval screens |
| 19 | UA & Growth Marketer | 3 Approval and launch (step 9) | Not started | Performance / UA + Ad Marketer + ASO / SEO + Social + Influencer / PR + Email / CRM | Advises and prepares launches and growth; a human spends and publishes |
| 20 | Game Designer | 4 Not needed for Ads Factory | Not started | Game Designer + Level + Systems / Economy + Live-Ops | Game rules, levels, economy and live content |
| 21 | Product & Business Analyst | 4 Not needed for Ads Factory | Not started | Product Manager + Business Analyst + Market Researcher + Delivery Manager | What to build and why, requirements, market and delivery tracking |
| 22 | Business Operations | 4 Not needed for Ads Factory | Not started | Finance + Operations / Procurement + Sales / Account + HR + Legal (draft only) | Drafts for business paperwork; a human signs and decides |
