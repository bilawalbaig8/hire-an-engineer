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
- [ ] AI-3 Add to roster, boss allowlist, team-roster, CHANGELOG, THIRD_PARTY_NOTICES; set Tested if evals pass
- [ ] AI-4 Install with --only, commit and push (only after the owner says OK)

## Data Scientist

- [x] DS-1 Build evals, knowledge files and agent file, then run the evals and fix failures (headless agent working; owner approved the role file)
- [x] DS-2 Checks: validate_agents, validate_skills, check_sources, check_evals, full pytest; read the eval table
- [ ] DS-3 Add to roster, boss allowlist, team-roster, CHANGELOG, THIRD_PARTY_NOTICES; set Tested if evals pass
- [ ] DS-4 Install with --only, commit and push (only after the owner says OK)

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

## Roles (70), in the order I recommend building them

Order follows the Ads Factory build order (owner request 2026-10-24); the owner still names which roles to build.

| # | Role | Wave | Group | Priority | Status | Why |
|---|---|---|---|---|---|---|
| 1 | Orchestrator | 0 Ban chuke / ban rahe | Boss | core 12 | Tested | Boss, ban chuka (Ads Factory ka Master agent isi par bana hoga) |
| 2 | Solution Architect | 0 Ban chuke / ban rahe | Architecture | core 12 | Tested | Design aur structure, ban chuka |
| 3 | Code Reviewer | 0 Ban chuke / ban rahe | Quality | core 12 | Tested | Code ka review, ban chuka |
| 4 | Data Scientist | 0 Ban chuke / ban rahe | Data & AI | wave 2 core | In progress | Ban raha hai; Ads Factory ka Analyst (step 3) aur Learner (step 10) isse madad lete hain |
| 5 | AI Engineer (mode) | 0 Ban chuke / ban rahe | Data & AI | mode of another role | In progress | Ban raha hai; agents ke AI hisse (step 3 se 10) |
| 6 | Backend Engineer | 1 Buniyaad (Ads Factory step 1) | Engineering | core 12 | Not started | Step 1 foundation aur sab services ka code |
| 7 | Database Architect | 1 Buniyaad (Ads Factory step 1) | Architecture | core 12 | Not started | Step 1: schemas aur lineage IDs |
| 8 | DevOps Engineer | 1 Buniyaad (Ads Factory step 1) | Infra & release | core 12 | Not started | Step 1: cloud workers aur GPU servers par chalana (sab kuch server par) |
| 9 | Security Engineer | 1 Buniyaad (Ads Factory step 1) | Security | core 12 | Not started | Step 1: keys, accounts aur access; spend ka haq insaan ke paas hi rahega |
| 10 | QA/Test Engineer | 1 Buniyaad (Ads Factory step 1) | Quality | core 12 | Not started | Services ke code ki testing, pehle se hi chahiye |
| 11 | AppSec Reviewer | 1 Buniyaad (Ads Factory step 1) | Security | later | Not started | Services ke code me security ki ghalti |
| 12 | Integration Engineer | 2 Collector aur data (step 2) | Engineering | later | Not started | Step 2 Collector: Pubforce Ad Library, Looker, Sensor Tower, Meta Ad Library ke APIs |
| 13 | Data Engineer | 2 Collector aur data (step 2) | Engineering | later | Not started | Step 2: collector ka data kahan aur kaise rakhna |
| 14 | Prompt / AI-Ops Engineer | 3 Analyst, Learner aur dashboards (step 3, 10) | Data & AI | later | Not started | Agents ke prompts aur unki quality, step 3 ke baad har agent ke liye |
| 15 | BI Developer | 3 Analyst, Learner aur dashboards (step 3, 10) | Data & AI | later | Not started | Looker aur dashboards se data parhna aur dikhana |
| 16 | Art Director | 4 Creative lanes (step 4 se 6) | Art & creative | wave 2 core | Not started | Step 5: creative ki disha, pehla creative agent |
| 17 | Creative Director | 4 Creative lanes (step 4 se 6) | Art & creative | wave 2 core | Not started | Concepts aur creative ka faisla (step 4) |
| 18 | Concept Artist | 4 Creative lanes (step 4 se 6) | Art & creative | later | Not started | Step 4 Visualizer: concept images |
| 19 | 2D Artist / Illustrator | 4 Creative lanes (step 4 se 6) | Art & creative | wave 2 core | Not started | Static ads aur art |
| 20 | Storyboard / Scriptwriter | 4 Creative lanes (step 4 se 6) | Art & creative | wave 2 core | Not started | Video lane (step 6): script aur storyboard |
| 21 | Video Editor | 4 Creative lanes (step 4 se 6) | Art & creative | wave 2 core | Not started | Video lane (step 6): Remotion aur FFmpeg |
| 22 | Technical Artist | 4 Creative lanes (step 4 se 6) | Art & creative | later | Not started | Playables, APK aur capture scenes (aap ke Tech Artists ka kaam) |
| 23 | Game/Unity Engineer | 4 Creative lanes (step 4 se 6) | Engineering | later | Not started | Unity capture aur playables ka code |
| 24 | Animator | 4 Creative lanes (step 4 se 6) | Art & creative | later | Not started | Video lane me motion |
| 25 | 3D Artist | 4 Creative lanes (step 4 se 6) | Art & creative | later | Not started | 3D assets (Meshy ya Tripo) |
| 26 | Sound Designer | 4 Creative lanes (step 4 se 6) | Art & creative | later | Not started | Video ads ki awaz aur music |
| 27 | Motion/Graphic Designer | 4 Creative lanes (step 4 se 6) | Design | later | Not started | Graphics aur motion pieces |
| 28 | Art QA | 5 QA gate (step 7) | Art & creative | later | Not started | Step 7 QA gate: art ki quality check |
| 29 | Frontend Engineer | 6 Approval aur launch handoff (step 9) | Engineering | core 12 | Not started | Step 9 checkpoint: insaan ke approve karne ki screens |
| 30 | UX/UI Designer | 6 Approval aur launch handoff (step 9) | Design | core 12 | Not started | Approval aur review screens ka design |
| 31 | Performance / UA Marketer | 6 Approval aur launch handoff (step 9) | Marketing | wave 2 core | Not started | Launch aur monitoring UA team ka kaam hai; Ads Factory sirf handoff deta hai |
| 32 | Ad Marketer | 6 Approval aur launch handoff (step 9) | Marketing | wave 2 core | Not started | Ads Factory ke output ko market me le jana |
| 33 | Analytics/Growth Analyst | 6 Approval aur launch handoff (step 9) | Growth | later | Not started | Live ads ke results parhna (step 10 ki khuraak) |
| 34 | Threat Modeler | 7 Hifazat aur chalte rehna (Ads Factory ke baad) | Security | later | Not started | Pehle se soch lena ke hamla kahan se aa sakta hai |
| 35 | Penetration Tester / Red Team | 7 Hifazat aur chalte rehna (Ads Factory ke baad) | Security | later | Not started | Sirf aap ke apne system par, aap ki ijazat se hamla karke kamzori dikhata hai |
| 36 | SRE/Monitoring | 7 Hifazat aur chalte rehna (Ads Factory ke baad) | Infra & release | later | Not started | Chalne ke baad nigrani |
| 37 | Incident Responder | 7 Hifazat aur chalte rehna (Ads Factory ke baad) | Security | later | Not started | Keys leak ya breach ho to kya karna hai: plan aur steps, insaan amal karta hai |
| 38 | Privacy/Compliance | 7 Hifazat aur chalte rehna (Ads Factory ke baad) | Security | later | Not started | Personal data aur qaide |
| 39 | Release Manager | 7 Hifazat aur chalte rehna (Ads Factory ke baad) | Infra & release | later | Not started | Release ka intezam |
| 40 | Technical Writer | 7 Hifazat aur chalte rehna (Ads Factory ke baad) | Docs & support | later | Not started | Docs aur playbook |
| 41 | Product Manager | 8 Ads Factory ke liye zaroori nahi (baad me) | Product | core 12 | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 42 | Business Analyst | 8 Ads Factory ke liye zaroori nahi (baad me) | Product | core 12 | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 43 | Market Researcher | 8 Ads Factory ke liye zaroori nahi (baad me) | Product | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 44 | Delivery Manager | 8 Ads Factory ke liye zaroori nahi (baad me) | Product | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 45 | UX Researcher | 8 Ads Factory ke liye zaroori nahi (baad me) | Design | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 46 | Content Writer | 8 Ads Factory ke liye zaroori nahi (baad me) | Design | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 47 | Mobile Engineer | 8 Ads Factory ke liye zaroori nahi (baad me) | Engineering | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 48 | AI/ML Engineer | 8 Ads Factory ke liye zaroori nahi (baad me) | Engineering | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 49 | Performance Engineer | 8 Ads Factory ke liye zaroori nahi (baad me) | Quality | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 50 | Accessibility Specialist | 8 Ads Factory ke liye zaroori nahi (baad me) | Quality | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 51 | Support Analyst | 8 Ads Factory ke liye zaroori nahi (baad me) | Docs & support | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 52 | ASO/SEO/Marketing | 8 Ads Factory ke liye zaroori nahi (baad me) | Growth | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 53 | VFX Artist | 8 Ads Factory ke liye zaroori nahi (baad me) | Art & creative | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 54 | Game Designer | 8 Ads Factory ke liye zaroori nahi (baad me) | Game design | wave 2 core | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 55 | Level Designer | 8 Ads Factory ke liye zaroori nahi (baad me) | Game design | wave 2 core | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 56 | Systems / Economy Designer | 8 Ads Factory ke liye zaroori nahi (baad me) | Game design | wave 2 core | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 57 | Live-Ops Manager | 8 Ads Factory ke liye zaroori nahi (baad me) | Game design | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 58 | Playtest QA | 8 Ads Factory ke liye zaroori nahi (baad me) | Game design | wave 2 core | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 59 | Data Analyst (mode) | 8 Ads Factory ke liye zaroori nahi (baad me) | Data & AI | mode of another role | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 60 | Social / Community Manager | 8 Ads Factory ke liye zaroori nahi (baad me) | Marketing | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 61 | Influencer / PR Manager | 8 Ads Factory ke liye zaroori nahi (baad me) | Marketing | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 62 | Email / CRM Marketer | 8 Ads Factory ke liye zaroori nahi (baad me) | Marketing | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 63 | HR / Recruiter | 8 Ads Factory ke liye zaroori nahi (baad me) | Business | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 64 | Finance / FP&A | 8 Ads Factory ke liye zaroori nahi (baad me) | Business | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 65 | Legal / Contracts | 8 Ads Factory ke liye zaroori nahi (baad me) | Business | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 66 | Sales / Account Manager | 8 Ads Factory ke liye zaroori nahi (baad me) | Business | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 67 | Operations / Procurement | 8 Ads Factory ke liye zaroori nahi (baad me) | Business | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 68 | Localisation | 8 Ads Factory ke liye zaroori nahi (baad me) | Business | later | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 69 | Web Designer (mode) | 8 Ads Factory ke liye zaroori nahi (baad me) | Web | mode of another role | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
| 70 | Web Developer (mode) | 8 Ads Factory ke liye zaroori nahi (baad me) | Web | mode of another role | Not started | Ads Factory ko iski zaroorat nahi; baad me, jab zaroorat ho |
