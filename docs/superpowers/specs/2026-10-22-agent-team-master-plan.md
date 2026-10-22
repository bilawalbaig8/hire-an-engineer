# Agent team ("software house") — master plan and spec

Status: DRAFT for owner approval. Date: 2026-10-22. Branch: `feat/specialized-agents`.
Task list (source of truth): `TASKS.md` in the repo root. A live view of it is published as an Artifact ("Agent Team Progress").

## 1. Why

`hire-an-engineer` (0.2.0) is one skill that plays the whole team. The owner wants the real thing: **a software house of specialised agents**, one per professional role, run by a **boss (Orchestrator)** that hands each agent its share of the work. People with no engineering background give an idea; the team plans, designs, builds, tests, ships and documents it, asking the owner only for decisions that are theirs.

## 2. Goals, non-goals, anti-goals

Goals
- Every role a real software house has, as a specialist agent with real depth (verified, credited sources; checklists; evals).
- One Orchestrator that is the only agent talking to the owner, splits work, passes context, enforces approvals.
- One reusable pattern (template + handoff contract) so each new role is cheap to add.
- Works with `hire-an-engineer` (project memory, plain-language rules, approvals) instead of replacing it.
- Progress always visible: `TASKS.md` + live artifact.

Non-goals
- A hosted service or a UI. This is files for Claude Code (and skill-compatible tools).
- Rewriting `hire-an-engineer` before the team works.
- Copying book text. Ideas in our own words, credited.

Anti-goals (failure even if it "works")
- 30 shallow agents instead of fewer deep ones.
- Agents that invent facts, skip verification or take irreversible decisions alone.
- A boss that does the specialists' work itself, or a team that costs far more than one agent for small tasks.
- Roles that overlap so much they contradict each other.

## 3. Shape of the system

```
Owner  ⇄  Orchestrator (boss)  ⇄  Specialist agents (one per role)
                 │                          │
          project memory (AGENTS.md, PROJECT_STATE.md, docs/decisions/)  ← shared by all
```
- **Specialist** = skill-shaped knowledge folder (`skills/<role>/`) + thin Claude Code agent file (`agents/<role>.md`). Decided in the Architect design.
- **Handoff contract** (defined in Phase 1): what the boss sends (goal, context files, constraints, definition of done) and what the specialist returns (result, files written, questions for the owner, decisions needing approval, assumptions, verification evidence).
- **Orchestrator** decides: which roles for this task, in what order, what runs in parallel, when the owner must approve, which model each role uses (Opus hard reasoning/review, Sonnet ordinary build, Haiku mechanical).
- Small tasks use few roles; the boss may refuse to wake the whole house for a one-line change.

## 4. Roles (31 = 30 specialists + boss). Core-12 first.

| Group | Roles (★ = core 12) |
|---|---|
| Boss | Orchestrator/Tech Lead ★ |
| Product | Product Manager ★, Business Analyst ★, Market/Competitor Researcher, Project/Delivery Manager |
| Design | UX Researcher, UX/UI Designer ★, Motion/Graphic Designer, Content/UX Writer |
| Architecture | Solution Architect ★ (first to build), Data/Database Architect ★ |
| Engineering | Frontend ★, Mobile, Backend/API ★, Game/Unity, Integration, AI/ML, Data Engineer |
| Quality | QA/Test ★, Code Reviewer ★, Performance, Accessibility |
| Security | Security Engineer ★, Privacy/Compliance |
| Infra and release | DevOps/Platform ★, SRE/Monitoring, Release Manager |
| Docs and support | Technical Writer, Support/Feedback Analyst |
| Growth | Analytics/Growth Analyst, ASO/SEO/Marketing |

## 5. Phases (details and status in `TASKS.md`)

- **Phase 0 — Plan and spec:** this plan, the Architect design, task list, owner approval.
- **Phase 1 — Contract and template:** handoff contract, `templates/agent-template/`, validator/packager support for `agents/`, install script, eval pattern for agents.
- **Phase 2 — Architect:** research written into `sources.md`, knowledge files for every field, two modes (Design, Recover/Review), diagrams, evals, release `software-architect` 0.1.0.
- **Phase 3 — Second specialist (Reviewer or QA):** proves the contract on two agents.
- **Phase 4 — Orchestrator:** own design doc, built and tested against the first two specialists.
- **Phase 5 — Remaining roles** in six groups (product, design, engineering, quality+security, release+ops, docs+growth), each group: research → spec → build → evals → release.
- **Phase 6 — Integration:** router line in `hire-an-engineer`, optional plugin bundle, end-to-end test (build a small real app with the whole team), docs, release.

## 6. Definition of done for one agent

1. Spec approved by owner. 2. Sources researched and verified (verified/unverified marked), credited in `THIRD_PARTY_NOTICES.md`. 3. Knowledge files written in own words. 4. Agent file with role, model, tools, handoff behaviour. 5. Evals (typical case, edge case, refusal case) written **before** the build and passing after. 6. `validate_skills.py` green. 7. CHANGELOG entry. 8. Repo and installed copies identical. 9. Committed; release only when the owner says.

## 7. Risks (pre-mortem: "it failed, why?")

| Risk | Early sign | Answer |
|---|---|---|
| Too many shallow agents | Role files under ~1 page of real content | Core-12 first; a role ships only when evals pass |
| Context loss between agents | Specialist re-asks things already decided | Shared project memory is the handoff; contract requires context files listed |
| Cost explosion | Small tasks wake many roles | Boss sizes the task; model per role; one-agent mode stays |
| Contradicting roles | Architect and Backend disagree | Boss resolves; one-way-door decisions go to the owner |
| Invented sources or facts | Unverifiable citations | Only verified items cited; claims labelled verified/inferred/unknown |
| Drift between repo and installed copies | `diff -rq` differs | Script checks both on every change |
| Orchestrator written on guesses | Handoff changes after the boss exists | Build boss only after two specialists work |

## 8. Decisions already made by the owner

- New branch `feat/specialized-agents`; every software-house role as a specialist agent.
- Architect first; Orchestrator ("boss") that delegates; knowledge in skill shape with a thin agent file on top.
- Plan, spec and a live task list before building agents.
## 9. My calls (please check)

Order Architect → second specialist → boss → rest; copy-install before plugin bundle; Opus for Architect/Reviewer/Orchestrator, Sonnet for ordinary-build roles, Haiku for mechanical steps; core-12 chosen as listed; releases per skill with tags `<skill>-v<version>`.
