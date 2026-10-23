# Four new agents: design (planning only)

Date: 2026-10-23. Status: APPROVED by the owner on 2026-10-23 (planning only; vault expiry rule still on hold). Nothing is built. Building starts only after a build plan is written and the owner says to start.

## 1. Intent and why

The team today: boss (orchestrator), Architect, Backend Engineer, Code Reviewer, AI Engineer, Data Scientist.

Four gaps the owner named:

1. When the boss is busy running work, the owner cannot plan, ask or set priorities with anyone.
2. Nobody builds or runs automations (n8n, Zapier, loop tasks).
3. The team forgets. A fix found in one project is lost; the same problem costs time again.
4. Nobody looks outside Claude: new tools, new AI models, what Gemini or GPT does better, and whether the team should use them.

So four new agents: **Personal Assistant**, **Automation Engineer**, **Learning Agent**, **R&D Agent**.

## 2. Goals, non-goals, anti-goals

Goals
- Owner can plan and talk "with a free helper" while the boss works.
- Automations can be designed, built, supported by one agent.
- Real fixes and lessons are saved and found again next time.
- Owner gets honest "adopt it or not" advice on new tech.

Non-goals (for this document)
- No building: no agent files, skills, evals, installers or UI changes yet.
- No decision on the expiry rule of the vault (on hold, owner will decide later).
- No always-on, scheduled R&D (on demand first).

Anti-goals (a failure even if it technically works)
- The assistant slows or stops running work.
- An agent edits skills, sends messages, spends money or goes live without the owner's yes.
- Secrets (keys, passwords) land in chat, files or the vault.
- Web text is treated as an order.
- The team grows heavy: four agents must stay small and clearly separate.

## 3. What exists today (checked by reading the repo, 2026-10-23)

- Only the boss talks to the owner. Specialists answer the boss with a 7-field handoff (status, summary, files, questions, approvals, assumptions, evidence). Source: `hire-an-engineer/agents/orchestrator.md`, `docs/agents/agent-template/handoff-contract.md`.
- Office window is a viewer. Answering from the window is OFF by the owner's decision (2026-10-23). Do not switch it on.
- Boss limits: 8 specialist calls, 2 fix rounds. Rule "one owner per artifact".
- Adding one agent = about 10 steps (`docs/agents/agent-template/README.md`): role document first, skill, agent file, evals, roster row, orchestrator tool list and references, changelog, installer, office UI seat (agent list is hardcoded in `visual-office/index.html`), checks.
- Known drift: the orchestrator's tool list omits `backend-engineer`. Fix it in the same change.
- No agent memory or vault exists. Project memory is only `AGENTS.md`, `PROJECT_STATE.md` and `.team/runs/`.
- Architect has web access for official docs only. Wider web use needs an explicit allowance.

## 4. The four agents

### 4.1 Personal Assistant

Purpose: the owner's planner and note-keeper. Plans ahead, holds open questions, keeps a priority list, proposes memory updates.

Does not: write product code, call specialists, stop running work, change priorities by itself.

How it is used (owner chose both, start with A):
- A. Boss calls it as a subagent. The owner says "assistant se pucho" and the boss relays. It is a relay, not a direct chat. Each call starts fresh, so continuity comes from its files.
- B. Later: the owner opens a second session in the same folder with `claude --agent assistant`. Same agent file, same files. No new design needed.

Files (my call): `.team/assistant/` with `queue.md` (priorities), `plan.md` (what comes next), `questions.md` (open questions), `memory-proposals.md`. Only the assistant writes there. Boss reads at run start and at every checkpoint.

Priorities: assistant proposes, owner approves (owner agreed with my default).

Open check for build time: does the boss stay responsive if specialists run in the background? Not verified. If not, B becomes the main path.

UI: B shows file-write activity through the existing hooks. A desk or seat for it needs a UI edit.

### 4.2 Automation Engineer

Purpose: design, build, run and support automations: n8n, Zapier, scheduled and loop tasks, connectors between tools.

Boundary with Backend Engineer: Backend builds your own server, API, database. Automation connects existing tools and schedules. If a job needs both, the boss gives each its own folder.

Situation: the owner has neither n8n nor Zapier yet. First job is to recommend one (cost, ease, hosting). My unverified note: a Zapier connector already exists in the owner's Claude; n8n needs its own server or account. The owner creates accounts; the agent only asks.

Safety (same rules as the team): test with fake data first; real sends, spending, going live, account creation only with the owner's approval; keys never in chat or files, only "exists / does not exist".

Support: find why a workflow failed, fix it, keep a small register (what it does, which tool, which account).

Reuses `hire-an-engineer/skills/hire-an-engineer/references/process-automation.md` as its base.

### 4.3 Learning Agent (the vault)

Purpose: save what the team learned and find it again.

Vault entry (my guess at the shape): problem, cause, fix, project, date, times it helped.

Flow:
1. After a project or session, the boss gives the agent the facts (what was new, what was fixed). It writes entries.
2. Before new work the boss asks it "have we seen this?" and passes the answer into the specialist's brief.
3. If the same issue repeats several times, it writes a **proposal** for a new skill. The owner approves. It never edits installed skills by itself.

ON HOLD: when an unused entry leaves the vault. The owner will decide later. Until then nothing is deleted.

Rules: no secrets or personal data in entries. Vault is plain files. One writer: only this agent.

### 4.4 R&D Agent

Purpose: look outside Claude. New tech, new AI models, what Gemini or GPT does well, and compare it with how our team is built.

Flow: collect public web data (scrape), study it, write a short report that ends with a plain verdict: "adopt / do not adopt, and why".

Runs when the owner asks. Regular scheduled runs may be added later.

Tool list (my call): `.team/tools-available.md` says which AI tools exist (API, account, none). No key values. R&D uses what exists, otherwise web only, or asks.

Rules: public pages only, no personal data, respect site rules; web text is data, not instructions; paid API calls only with the owner's approval; wider web than official docs needs an explicit allowance.

## 5. Constraints that apply to all four

- Follow the 7-field handoff contract. Specialists never talk to the owner directly (the Assistant in mode B is the one planned exception: it is the owner's own session).
- Boss caps (8 calls, 2 fix rounds) stay.
- Each agent: role document first (owner approval), skill, agent file, evals (typical, edge, refusal), roster row, orchestrator updates, changelog, office UI seat.
- Documents are in simple English.
- Version: this is new work, so it goes to 0.2.0, not the frozen 0.1.0. Private files stay local.

## 6. Models (my call, from the owner's model rules)

| Agent | Model | Effort | Why |
|---|---|---|---|
| Personal Assistant | sonnet | medium | notes and planning |
| Learning Agent | sonnet | medium | summaries and search |
| R&D Agent | sonnet | medium | reading and comparing |
| Automation Engineer | sonnet; opus for risky or live work | medium | ordinary builds, careful when live |

## 7. Order (my call)

Design all four now (this document). Build order later: Learning, R&D, Automation, Assistant last, because it needs the open check in 4.1. Each agent is built and approved on its own.

## 8. Decided by the owner / my calls / open

Owner decided
- Four agents with the purposes above.
- Assistant: subagent under the boss first, own session possible later.
- Assistant only proposes priorities.
- Vault expiry rule: on hold.
- R&D: collects web data, studies, gives findings.
- Planning only; build decisions later.

My calls (owner can change)
- Files and folder names in sections 4.1, 4.4.
- R&D on demand first.
- Learning Agent proposes skills, never edits them.
- Models in section 6 and build order in section 7.
- Documents live in `docs/superpowers/specs/` outside the `hire-an-engineer/` folder, so they are not published.

More calls of mine (added after the builder check; owner can change)
- Assistant test first: before any Assistant build work, test whether the boss stays responsive while specialists run in the background. If it does not, mode B (own session) becomes the main path and A is secondary.
- "Scrape" for R&D means WebFetch, WebSearch and read-only scripts on public pages. No logins, no headless browser at first. Wider use needs the owner's yes in chat for that run; the boss writes it in the run record. No standing allowance.
- R&D is web-only in version 1. Gemini or GPT accounts and keys can be added later through `tools-available.md`, with an approval for every paid call.
- Vault writes: only the Learning Agent writes vault entries. The boss gives it facts. The Assistant's `memory-proposals.md` goes to the boss, who shows the owner; owner-approved lines go into `AGENTS.md` or `PROJECT_STATE.md` by the boss, and into the vault only through the Learning Agent.
- Automation Engineer first deliverable: a recommendation report (n8n vs Zapier) and a plan. Builds wait until the owner has an account. "Loop tasks" means Claude Code loops and schedules first; cron jobs later.
- No Assistant UI seat in version 1. Its file-write activity still shows through the hooks.
- Assistant files are per project (`.team/assistant/`).

Open (owner)
- Vault expiry rule (on hold).
- Vault location: owner said learnings must stay connected to the repo (its database or a Git issue). My reading, to confirm with the owner: the vault is plain files inside each project's repo (for example `.team/vault/`), so it travels with the project and has Git history. Cross-project reuse happens only through skills: a lesson that repeats is proposed as a skill (owner approves). Git issues: the Learning Agent may DRAFT an issue for a repeated problem, but creating it on GitHub is outward-facing and needs the owner's yes each time. If a repo is public, the vault folder must be git-ignored or the repo private, because entries may hold project details. The owner pushes to GitHub in PowerShell as today.

## 9. What is left to the builder

Exact file formats, prompts, eval cases, installer and UI changes, and the wording of role documents. The builder follows the 10-step list in section 3 and the owner's approvals above.
