# Architect agent — design

Status: DRAFT, waiting for owner approval. Nothing is built yet.
Branch: `feat/specialized-agents`. Date: 2026-10-22.

## 1. Intent and why

`hire-an-engineer` (released 0.2.0) is one skill that plays the whole software team for people who build with AI but have no engineering background. The owner wants to go further: a **full software house of specialised agents**, one per role (about 30 roles, a first core of 12). This document covers the **first** agent only: the **Architect**. It becomes the pattern for every later role.

The Architect must be the best architect the owner can get from an AI: it designs and reviews the architecture of **any kind of software** (web, backend, mobile, game and game engine, desktop, API/platform, AI/agent systems, data pipelines) and produces the diagrams and decision records that go with it. It must also **recover and review the architecture of existing code** (reverse engineering).

The people it serves are non-engineers: it explains in plain language, then also leaves precise written artifacts an engineer can build from.

## 2. Goals, non-goals, anti-goals

Goals
- One Architect that handles every software field, with real depth per field.
- Two modes: **Design** (new project) and **Recover/Review** (existing code).
- Output is files in the project repo (`docs/architecture/`), versioned, plus a short plain-language summary in chat.
- Every important decision records its reasons, the options turned down and what is given up (trade-offs).
- Knowledge comes from verified, credited sources, summarised in our own words.
- Built so the same pattern can produce the other roles with little extra work.

Non-goals
- Writing product code. (It may write checks that enforce architecture rules, e.g. dependency rules, only on request.)
- Copying text from books or papers. Ideas only, in our own words, always credited.
- The other roles (PM, QA, DevOps...). Later, one at a time.
- Rewriting `hire-an-engineer`. It only gets a router line later (see section 8).

Anti-goals (would be a failure even if it technically works)
- Confident but invented architecture: claims about existing code that were never checked.
- One-size-fits-all answers (microservices for a small app, a web pattern forced on a game).
- Diagrams that are pretty but wrong, unreadable, or never rendered and checked.
- Big irreversible decisions taken without the owner's approval.
- Fake or unverified source references.

## 3. Chosen format (owner decision: option 3)

Knowledge and behaviour live in a **skill-shaped folder**; a **thin Claude Code agent file** sits on top.

```
skills/software-architect/            ← the knowledge (works in any tool that reads skills)
  SKILL.md                            ← router + core rules, short
  references/
    core-principles.md                ← trade-offs, quality attributes, reversibility, ADRs
    method-design.md                  ← Design mode: questions → options → decision → docs
    method-recover.md                 ← Recover/Review mode: the 6 steps
    web-backend-cloud.md
    distributed-data.md
    mobile.md
    desktop-plugins.md
    game-engine.md
    realtime-netcode-state.md
    ai-systems.md
    security-architecture.md
    data-pipelines.md
    diagrams.md                       ← C4 levels, toolchain, readability rules, render + check
    review-checklists.md              ← design review, 10x growth, pre-launch, drift
    sources.md                        ← verified sources, what each is for, licence, status
agents/architect.md                   ← thin Claude Code subagent: role, model, tools, which skill to load
```

Why: knowledge is written once; later roles reuse the same shape. The agent file only says who it is, which model it runs on, and what it may touch.

## 4. How it works

### Design mode (new project)
1. Ask the few questions that change the design: who uses it and how many, what data and how much, where it runs (browser, phone, console, server), what already exists, budget, team, deadline, what must never fail.
2. Turn answers into **quality-attribute scenarios** (testable: "page loads in under 2 s for 10k users").
3. Generate 2–3 candidate architectures; pick by trade-off; say what each gives up. Default to the simplest that meets the scenarios (e.g. a modular monolith before services; a single AI call before an agent).
4. Write the artifacts (section 5). Show a simple diagram and a plain-language summary in chat.
5. Mark one-way-door decisions and ask for approval before they are final.

### Recover/Review mode (existing code), six steps
1. Inventory and entry points (repo layout, build/deploy files, all ways execution starts).
2. Data model and state (schema, who writes what).
3. Static structure (dependency graph; cycles, layers, high fan-in/out). Automatic clustering is a hint, not truth.
4. Behaviour trace of 3–5 key use cases from entry to data store.
5. History and hotspots from git (change frequency × complexity, change coupling, ownership; `git log -S` for when/why).
6. Hypothesise the intended architecture, check conformance, write the C4 views and arc42 sections, list risks ATAM-style, propose steps (strangler-fig style) if modernising.
Every claim is labelled **verified in code**, **inferred**, or **unknown**. Inferred decisions are written as ADRs marked "inferred".

## 5. Artifacts (written into the user's project)

```
docs/architecture/
  overview.md            ← arc42-style: goals, constraints, context, building blocks, runtime, deployment, risks
  decisions/NNNN-*.md    ← ADRs (MADR style), superseded not rewritten
  diagrams/              ← model + views, source files and rendered SVG/PNG
  risks.md               ← what breaks at 10x, top risks, how to retire each
  scenarios.md           ← quality-attribute scenarios
```
Plus, where useful, automated architecture checks (ArchUnit / dependency-cruiser / import-linter) in CI, on the owner's request.

## 6. Diagrams

- Default: **C4 levels** (context, container, component), kept as a text model in the repo. Tool choice **[my call, to confirm in the plan]**: LikeC4 or Structurizr DSL as the model source; Mermaid for diagrams that must render inline in GitHub/Markdown (sequence, flow, ER).
- Fallbacks: D2 (layout quality), PlantUML (heavy UML), draw.io/Excalidraw only for hand-edited sketches.
- Rules: one question per diagram, one C4 level per diagram, ≤ ~9 elements, every arrow labelled and directional, legend, boundaries and external systems shown, inferred links dashed, no mixed levels. Builds on `hire-an-engineer` `documents.md` §7.
- The agent **renders every diagram and looks at it** before presenting. If it cannot render, it says so.

## 7. Knowledge and sources

- Knowledge files summarise the **ideas** from the verified sources in our own words. No copied passages.
- `sources.md` lists each source with title, author, year, URL, what it is for, free/paid, licence, and a status: `verified` or `unverified`. Only verified items are cited as fact; unverified ones are marked.
- Source lists were researched on 2026-10-22 (four research passes: foundations; web/backend/security/AI/data; game/mobile/desktop/real-time; recovery and diagram tools, about 125 items). Items checked only through search snippets stay marked accordingly (e.g. O'Reilly pages returned 403).
- Credits go into `THIRD_PARTY_NOTICES.md`. CC BY-SA material (arc42, OWASP) is summarised, not copied, so share-alike does not carry over.
- Decision rules distilled so far (examples): monolith first unless several independent teams; split a service only for a concrete reason; timeout + bounded retry + circuit breaker on every remote call; choose consistency per use case; set SLOs first; threat-model during design; simplest AI pattern that works; server-or-client owns the truth for multiplayer; fixed timestep for game simulation; local database as source of truth on mobile; out-of-process plugins with narrow APIs; explicit state machines for long-lived behaviour.

## 8. Fit with the rest of the repo

- New skill `software-architect` with its own version (starts 0.1.0, unreleased); tag `software-architect-v0.1.0` when the owner says release. The existing release workflow already handles any `<skill>-v<version>` tag, and `validate_skills.py` already validates every folder under `skills/`.
- `agents/` is a new top-level folder for Claude Code agent files. The packaging script and validator need a small extension to cover it **[builder to check]**.
- `hire-an-engineer` later gets one router line: "architecture questions → the Architect agent/skill". Not part of this change.
- Follows `AGENTS.md`: CHANGELOG entry, `THIRD_PARTY_NOTICES.md` credits, run `validate_skills.py`, SKILL.md lean with detail in `references/`, description ≤ 1024 chars.
- The installed copy under `~/.claude` is updated together with the repo copy (owner's standing rule), for both the skill and the agent file.

## 9. Model and cost

Per the owner's model rules: the Architect agent runs on **Opus** (hard reasoning, hard-to-undo decisions), high effort. Diagram rendering, file listing and similar mechanical steps may be handed to a smaller model. **[my call]**

## 10. How we will know it is good (tests)

Evals in `evals/software-architect/`, each a prompt with a pass/fail checklist:
- Design a small web app, a mobile app with offline use, a multiplayer game, an AI agent product, a data pipeline: it asks the right questions, picks a proportionate architecture, names trade-offs, produces valid artifacts and a rendered diagram.
- Recover a small real open-source repo: every claim carries a label, the dependency graph and entry points match reality, no invented components.
- Refusal cases: tries to over-engineer (microservices for a to-do app), or is asked to approve a one-way-door decision without the owner.

## 11. Left to the builder

File sizes and exact wording; exact ordering of references; exact CLI invocations for the diagram tools (each must be run and confirmed before it is written down); how the validator and packager treat `agents/`; the eval cases in detail.

## 11b. Calls added after the builder check (my calls, please check)

6. **Research results:** the four research passes are not yet in the repo. Writing them into `sources.md` and the field references is the **first build step** (raw results are still available in this session's agent outputs).
7. **0.1.0 scope:** core files plus all field references, each at a depth the verified sources support; the thinnest fields are marked "starter" and deepened in later versions.
8. **One decision-record series:** the Architect uses `docs/decisions/NNNN-*.md`, the same series `hire-an-engineer` already writes, and continues an existing series in Recover mode. Only the overview, diagrams, risks and scenarios go in `docs/architecture/`. No migration note needed.
9. **Rendering and installs:** follow `hire-an-engineer`'s rule: ask before installing anything. Baseline is **Mermaid** (renders on GitHub, needs no install to be read). LikeC4/Structurizr/D2 only if the tool is already present or the owner approves installing it. If nothing can be rendered, the agent gives the diagram source, says it was not rendered, and does not claim it was checked.
10. **Reuse for later roles:** a `templates/agent-template/` (agent file + skill-shaped folder with the standard sections) is built now alongside the Architect. No generator yet. Shared material stays inside `software-architect` until a second role needs it, then moves.

## 11c. Owner decision: orchestrator ("boss") agent (2026-10-22)

The owner decided there will be an **Orchestrator** that gives every specialist agent its share of the work. Consequences for this design:
- The Orchestrator is the **only agent that talks to the owner**. Specialists (Architect first) do their part and return a result. If a specialist needs an answer from the owner, it returns its questions to the Orchestrator, which asks the owner and resumes the specialist with the answer. The same applies to approvals of one-way-door decisions.
- The Architect is therefore built as a **specialist that works under a boss**: its Design mode is split into "return questions" → "receive answers" → "produce artifacts and return decisions needing approval". Its skill folder still works standalone, so until the Orchestrator exists the main session plays the boss.
- The Orchestrator is a **separate, later design** (its own document and branch step): task splitting, who does what, handoff format, project memory shared between agents, approval gates, model per role. It is not built in this change. Order: Architect first (this document), then Orchestrator, then the other roles.
- The handoff format between boss and specialist (what goes in, what comes back: result, questions, decisions needing approval, assumptions, files written) is defined in `templates/agent-template/` so the Orchestrator can be written against it.

## 11d. Order of work and distribution (2026-10-22)

- **Order:** (1) handoff contract in `templates/agent-template/`, (2) Architect, (3) a second core specialist (Reviewer or QA) so the contract is tested on two agents, (4) Orchestrator, built against those two, (5) remaining roles in groups of 3–4.
- **Distribution (owner left it to me):** copy-install first. `agents/*.md` plus an install script and `docs/INSTALL.md` section that copies them (and the skill folder) to `~/.claude/agents/` and `~/.claude/skills/`. A Claude Code plugin bundle is considered later, when there are enough roles.

## 12. Calls made without the owner (please check)

1. Skill name `software-architect`; agent file `agents/architect.md`.
2. Starts as version 0.1.0 of a new skill, not part of `hire-an-engineer` 0.3.0.
3. Opus for the Architect, smaller model for mechanical steps.
4. LikeC4/Structurizr plus Mermaid as the diagram default.
5. Artifacts live in `docs/architecture/` of the user's project.
