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
- [x] 1.4 Install script + INSTALL.md section (copy to ~/.claude) (done, reviewed; real install only after owner OK)
- [~] 1.5 Eval pattern for agents (typical, edge, refusal cases) and sources/evals checkers (built; independent review waiting for the Part 1 final review)
- [x] 1.6 Event log in the contract: every agent start, stop, handoff and file written is one line in .agents/events.jsonl (feeds the visual office) (done, reviewed)

## Phase 2 Architect

- [ ] 2.1 Write sources.md from the four verified research passes
- [ ] 2.2 core-principles, method-design, method-recover
- [ ] 2.3 Field references: web/backend/cloud, distributed/data, mobile, desktop/plugins, game/engine, real-time/netcode, AI systems, security, data pipelines
- [ ] 2.4 diagrams.md (C4, Mermaid default, render + check) and review-checklists.md
- [ ] 2.5 SKILL.md router and agents/architect.md
- [ ] 2.6 Evals written first: 5 design cases, 2 recover cases, refusal cases
- [ ] 2.7 Run evals, fix, rerun
- [ ] 2.8 THIRD_PARTY_NOTICES, CHANGELOG, validate, repo + installed copies identical
- [ ] 2.9 Commit; release software-architect 0.1.0 (only when owner says)

## Phase 3 Second specialist

- [ ] 3.1 Choose Reviewer or QA; research and spec
- [ ] 3.2 Build, evals, install copies
- [ ] 3.3 Contract tested on two agents; fix contract gaps

## Phase 4 Orchestrator

- [ ] 4.1 Orchestrator design spec (splitting, handoffs, approvals, model per role)
- [ ] 4.2 Build orchestrator against Architect + second specialist
- [ ] 4.3 Evals: small task, big task, conflict, approval gate, cost sizing
- [ ] 4.4 Release orchestrator

## Phase 5 Remaining roles

- [ ] 5.1 Group A Product: PM, Business Analyst, Researcher, Delivery Manager
- [ ] 5.2 Group B Design: UX Researcher, UX/UI, Motion, Content writer
- [ ] 5.3 Group C Engineering: Frontend, Backend, Mobile, Game, Integration, AI/ML, Data
- [ ] 5.4 Group D Quality & security: QA, Reviewer, Performance, Accessibility, Security, Privacy
- [ ] 5.5 Group E Release & ops: DevOps, SRE, Release Manager, Technical Writer, Support
- [ ] 5.6 Group F Growth: Analytics, ASO/SEO/Marketing
- [ ] 5.7 Wave 2 Art & creative: Creative Director, Art Director, Concept Artist, 2D Artist, 3D Artist, Animator, VFX, Technical Artist, Sound Designer, Video Editor, Storyboard/Scriptwriter, Art QA
- [ ] 5.8 Wave 2 Game design: Game Designer, Level Designer, Systems/Economy Designer, Live-Ops Manager, Playtest QA
- [ ] 5.9 Wave 2 Data & AI: Data Scientist, BI Developer, Prompt/AI-Ops (+ modes: Data Analyst, applied AI Engineer)
- [ ] 5.10 Wave 2 Marketing: Ad Marketer, Performance/UA Marketer, Social/Community, Influencer/PR, Email/CRM
- [ ] 5.11 Wave 2 Business (draft-only, human signs off): HR, Finance, Legal, Sales, Operations, Localisation
- [ ] 5.12 Wave 2 Web modes: Web Designer (UX/UI mode), Web Developer (Frontend mode)

## Phase 6 Integration

- [ ] 6.1 Router line in hire-an-engineer pointing to the team
- [ ] 6.2 Plugin bundle (skills + agents) if worth it
- [ ] 6.3 End-to-end test: build a small real app with the whole team
- [ ] 6.4 Docs, CHANGELOG, release hire-an-engineer 0.3.0

## Phase 7 Visual office

- [ ] 7.1 Starts only after the boss and two specialists work (Phase 4). Mock designs: 2-3 clickable office layouts, owner picks one
- [ ] 7.2 Owner approves the final design; written spec (desks, states, handoff animation, files panel, approvals inbox)
- [ ] 7.3 Event pipeline: Claude Code hooks write events, a small local server streams them to the browser
- [ ] 7.4 Working UI built from the approved design (office view, timeline, files panel, approvals inbox)
- [ ] 7.5 Boss opens the office automatically when a team run starts; owner answers approvals inside it
- [ ] 7.6 Test with a real problem: give the boss a task, specialists work, check the result is correct
- [ ] 7.7 Check the office tells the truth: replay the events and compare with what really happened; fix mismatches
- [ ] 7.8 Package, install script, docs

## Roles (66)

| Role | Group | Priority | Status |
|---|---|---|---|
| Orchestrator | Boss | core 12 | Not started |
| Product Manager | Product | core 12 | Not started |
| Business Analyst | Product | core 12 | Not started |
| Market Researcher | Product | later | Not started |
| Delivery Manager | Product | later | Not started |
| UX Researcher | Design | later | Not started |
| UX/UI Designer | Design | core 12 | Not started |
| Motion/Graphic Designer | Design | later | Not started |
| Content Writer | Design | later | Not started |
| Solution Architect | Architecture | core 12 | Next |
| Database Architect | Architecture | core 12 | Not started |
| Frontend Engineer | Engineering | core 12 | Not started |
| Mobile Engineer | Engineering | later | Not started |
| Backend Engineer | Engineering | core 12 | Not started |
| Game/Unity Engineer | Engineering | later | Not started |
| Integration Engineer | Engineering | later | Not started |
| AI/ML Engineer | Engineering | later | Not started |
| Data Engineer | Engineering | later | Not started |
| QA/Test Engineer | Quality | core 12 | Not started |
| Code Reviewer | Quality | core 12 | Not started |
| Performance Engineer | Quality | later | Not started |
| Accessibility Specialist | Quality | later | Not started |
| Security Engineer | Security | core 12 | Not started |
| Privacy/Compliance | Security | later | Not started |
| DevOps Engineer | Infra & release | core 12 | Not started |
| SRE/Monitoring | Infra & release | later | Not started |
| Release Manager | Infra & release | later | Not started |
| Technical Writer | Docs & support | later | Not started |
| Support Analyst | Docs & support | later | Not started |
| Analytics/Growth Analyst | Growth | later | Not started |
| ASO/SEO/Marketing | Growth | later | Not started |
| Creative Director | Art & creative | wave 2 core | Not started |
| Art Director | Art & creative | wave 2 core | Not started |
| Concept Artist | Art & creative | later | Not started |
| 2D Artist / Illustrator | Art & creative | wave 2 core | Not started |
| 3D Artist | Art & creative | later | Not started |
| Animator | Art & creative | later | Not started |
| VFX Artist | Art & creative | later | Not started |
| Technical Artist | Art & creative | later | Not started |
| Sound Designer | Art & creative | later | Not started |
| Video Editor | Art & creative | wave 2 core | Not started |
| Storyboard / Scriptwriter | Art & creative | wave 2 core | Not started |
| Art QA | Art & creative | later | Not started |
| Game Designer | Game design | wave 2 core | Not started |
| Level Designer | Game design | wave 2 core | Not started |
| Systems / Economy Designer | Game design | wave 2 core | Not started |
| Live-Ops Manager | Game design | later | Not started |
| Playtest QA | Game design | wave 2 core | Not started |
| Data Scientist | Data & AI | wave 2 core | Not started |
| BI Developer | Data & AI | later | Not started |
| Prompt / AI-Ops Engineer | Data & AI | later | Not started |
| Data Analyst (mode) | Data & AI | mode of another role | Not started |
| AI Engineer (mode) | Data & AI | mode of another role | Not started |
| Ad Marketer | Marketing | wave 2 core | Not started |
| Performance / UA Marketer | Marketing | wave 2 core | Not started |
| Social / Community Manager | Marketing | later | Not started |
| Influencer / PR Manager | Marketing | later | Not started |
| Email / CRM Marketer | Marketing | later | Not started |
| HR / Recruiter | Business | later | Not started |
| Finance / FP&A | Business | later | Not started |
| Legal / Contracts | Business | later | Not started |
| Sales / Account Manager | Business | later | Not started |
| Operations / Procurement | Business | later | Not started |
| Localisation | Business | later | Not started |
| Web Designer (mode) | Web | mode of another role | Not started |
| Web Developer (mode) | Web | mode of another role | Not started |
