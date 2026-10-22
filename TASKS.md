# Agent team: task list

Source of truth for progress. `[x]` done, `[~]` in progress, `[?]` waiting for owner, `[ ]` to do.
Master plan: `docs/superpowers/specs/2026-10-22-agent-team-master-plan.md`. Live view: Artifact "Agent Team Progress".


## Phase 0 Plan & spec

- [x] 0.1 Architect agent design spec (written, builder-checked)
- [x] 0.2 Master plan for the whole agent team
- [x] 0.3 Task list in repo (TASKS.md) + live progress page
- [?] 0.4 Owner approves Architect spec and master plan
- [x] 0.5 Commit specs on feat/specialized-agents
- [ ] 0.6 Implementation plan for Phases 1-2 (writing-plans)

## Phase 1 Contract & template

- [ ] 1.1 Handoff contract: what boss sends, what specialist returns
- [ ] 1.2 templates/agent-template (agent file + skill-shaped folder)
- [ ] 1.3 Validator and packager support for agents/
- [ ] 1.4 Install script + INSTALL.md section (copy to ~/.claude)
- [ ] 1.5 Eval pattern for agents (typical, edge, refusal cases)
- [ ] 1.6 Event log in the contract: every agent start, stop, handoff and file written is one line in .agents/events.jsonl (feeds the visual office)

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

## Phase 6 Integration

- [ ] 6.1 Router line in hire-an-engineer pointing to the team
- [ ] 6.2 Plugin bundle (skills + agents) if worth it
- [ ] 6.3 End-to-end test: build a small real app with the whole team
- [ ] 6.4 Docs, CHANGELOG, release hire-an-engineer 0.3.0

## Phase 7 Visual office

- [ ] 7.1 Design spec: office floor, one desk per role, who is working / waiting / idle, handoffs as moving files, approvals inbox
- [ ] 7.2 Event pipeline: Claude Code hooks write events, a small local server streams them to the browser
- [ ] 7.3 Web UI: office view, timeline, files panel, approvals inbox
- [ ] 7.4 Boss opens the office automatically when a team run starts; owner answers approvals inside it
- [ ] 7.5 Test with a replay of a recorded team run
- [ ] 7.6 Package, install script, docs

## Roles (31)

| Role | Group | Core 12? | Status |
|---|---|---|---|
| Orchestrator | Boss | yes | Not started |
| Product Manager | Product | yes | Not started |
| Business Analyst | Product | yes | Not started |
| Market Researcher | Product |  | Not started |
| Delivery Manager | Product |  | Not started |
| UX Researcher | Design |  | Not started |
| UX/UI Designer | Design | yes | Not started |
| Motion/Graphic Designer | Design |  | Not started |
| Content Writer | Design |  | Not started |
| Solution Architect | Architecture | yes | Next |
| Database Architect | Architecture | yes | Not started |
| Frontend Engineer | Engineering | yes | Not started |
| Mobile Engineer | Engineering |  | Not started |
| Backend Engineer | Engineering | yes | Not started |
| Game/Unity Engineer | Engineering |  | Not started |
| Integration Engineer | Engineering |  | Not started |
| AI/ML Engineer | Engineering |  | Not started |
| Data Engineer | Engineering |  | Not started |
| QA/Test Engineer | Quality | yes | Not started |
| Code Reviewer | Quality | yes | Not started |
| Performance Engineer | Quality |  | Not started |
| Accessibility Specialist | Quality |  | Not started |
| Security Engineer | Security | yes | Not started |
| Privacy/Compliance | Security |  | Not started |
| DevOps Engineer | Infra & release | yes | Not started |
| SRE/Monitoring | Infra & release |  | Not started |
| Release Manager | Infra & release |  | Not started |
| Technical Writer | Docs & support |  | Not started |
| Support Analyst | Docs & support |  | Not started |
| Analytics/Growth Analyst | Growth |  | Not started |
| ASO/SEO/Marketing | Growth |  | Not started |
