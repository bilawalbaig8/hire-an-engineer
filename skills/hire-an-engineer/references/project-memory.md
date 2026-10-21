# Project Memory, Structure & Docs-as-Code

The person builds with AI tools — and switches between them (chat, Claude Code, Cursor, Codex, Antigravity, others). Every new session or tool starts with no memory. Without an engineering background they don't know to keep state, decisions and docs in the project itself, so work gets repeated, contradicted or lost, and structure decays.

**Rule: memory lives in the project's files, not in any chat or tool.** Any agent, any day, can open the project, read a few files, and continue exactly where the last one stopped.

## Contents
1. Standard project scaffold
2. The memory files
3. Session start protocol
4. Checkpoints — memory update every ~20 minutes
5. Session end protocol
6. Docs-as-code
7. Structure guard
8. Working across different AI tools (only when switching tools)
9. Chat → coding agent handoff (only in chat-only environments)
10. Templates (in `templates.md`)

---

## 1. Standard project scaffold

Minimum by size:

| Size | Create |
|---|---|
| Tiny | git, AGENTS.md, CLAUDE.md (one line), PROJECT_STATE.md, README.md, .gitignore |
| Small | Tiny + CHANGELOG.md + docs/project.md (brief, design, plan, tests in one file) + docs/decisions/ once the first decision exists |
| Medium / Large | The full tree below; grow into it, don't create empty folders |

Full tree for Medium/Large (adapt folder names to the stack):

```
project/
├── AGENTS.md            ← rules for ANY AI agent working here (tool-agnostic)
├── CLAUDE.md            ← one line: "Read AGENTS.md" (+ Claude-specific notes if any)
├── PROJECT_STATE.md     ← where we are right now; read first, update last
├── README.md            ← what it is, how to run, links
├── CHANGELOG.md
├── .gitignore  .env.example
├── docs/
│   ├── README.md        ← index of all docs
│   ├── brief.md
│   ├── design/          ← system-design.md, ux-ui.md, data-dictionary.md, diagrams
│   ├── decisions/       ← 0001-use-supabase.md … (one file per decision)
│   ├── plans/           ← roadmap.md, milestone plans, implementation plans
│   ├── tests/           ← test-plan.md, reports/
│   ├── ops/             ← tools-setup.md, integrations.md, costs.md, release-checklist.md, runbook.md
│   └── guides/          ← user-guide.md, handoff.md
├── src/                 ← code, organised by feature/responsibility
├── tests/
└── scripts/             ← one-off and maintenance scripts, each with a comment header
```

Other tools' rule files (e.g. a Cursor rules file, `GEMINI.md`) should also just point to `AGENTS.md`, so there is exactly **one** source of rules. Check the current conventions of the person's tools rather than assuming file names.

If documents also live in an external doc tool (Google Docs, Notion, Claude Docs), the repo keeps a link and a short summary in `docs/README.md`; the repo remains the source of truth for agents.

## 2. The memory files

| File | Holds | Updated |
|---|---|---|
| `AGENTS.md` | Project purpose (2 lines), stack, how to run/test, folder map, coding conventions, rules ("tests before merge", "never commit secrets"), where docs live, the session protocols below | When conventions change |
| `PROJECT_STATE.md` | Current version and milestone, what's done, in progress, next 3 tasks, blockers, open questions for the person, last session summary, known issues | **End of every session** |
| `docs/decisions/` | One short record per significant decision: context, decision, alternatives, consequences, date | When decided |
| `docs/plans/roadmap.md` + task board link | Versions, milestones, priorities | Each milestone |
| `CHANGELOG.md` | What changed per version | Each release |

Keep `PROJECT_STATE.md` short (one screen). History goes in the changelog and decisions, not here.

## 3. Session start protocol

At the start of every session, in any tool:
1. Read `AGENTS.md` and `PROJECT_STATE.md` (and the task board if linked).
2. Check the repo state: current branch, uncommitted changes, last commits, do tests pass?
3. If anything contradicts the state file (e.g. code changed outside a session), reconcile first and note it.
4. Tell the person in 2–3 lines: where we are, what you'll do now, anything you need from them.

If the project has no memory files yet (an existing project, or one started without this skill): **first create them** by reading the code and asking the person what they remember — this is often the single most useful thing you can do for a stuck project.

## 4. Checkpoints — memory update every ~20 minutes

Sessions end unexpectedly (context runs out, the tool crashes, the person closes the window). Don't wait for the end to save memory.

**The rule: update memory at least every ~20 minutes of work**, plus at every natural checkpoint.

How to measure the 20 minutes (most agents have no built-in timer):
- `PROJECT_STATE.md` carries a `Last updated: YYYY-MM-DD HH:MM` line.
- At every task boundary (a task finished, a commit, a test run), check the current time — with `date` in a terminal, or the environment's clock if it shows one — and compare. If ≥ 20 minutes have passed, checkpoint now.
- If time can't be checked, use work as the proxy: checkpoint after every completed task or commit, roughly every 10–15 significant actions (tool calls/edits), and whenever the conversation is getting long.
- If the tool supports automation (hooks, scheduled reminders, rules that run on events), you may set one up to prompt a checkpoint — with the person's approval — but never rely on it alone.

**Always checkpoint immediately, regardless of time:**
- before anything risky (migrations, big refactors, deploys, deleting things)
- after any decision the person makes
- when switching tasks, or when you notice you're getting stuck
- when the person says they're stepping away

**A checkpoint is small and cheap** (token-efficient):
1. Commit or stash work in progress on its branch with a clear message.
2. Edit only the changed lines in `PROJECT_STATE.md`: in-progress task with the exact next step, anything newly done, blockers, questions, and the `Last updated` time. Append one line to the session log (`HH:MM — what changed`).
3. Add a decision record only if a decision was made.
Don't rewrite whole documents at checkpoints; full doc updates happen at task completion and session end.

Never interrupt the person to announce a checkpoint; at most a short line at the end of a message when it matters ("progress save kar di").

## 5. Session end protocol

Before ending a session or when the person says they're stopping:
1. Commit work in progress on a branch (never leave unsaved changes), tests status noted.
2. Update `PROJECT_STATE.md`: done, in progress (with exact next step), next tasks, blockers, questions.
3. Record any decisions made in `docs/decisions/`.
4. Update affected docs, board, changelog.
5. Tell the person in one line what's saved and what's next.

(Between session start and end, the ~20-minute checkpoints in §4 keep memory current.)

## 6. Docs-as-code

- Docs live in `docs/` as Markdown with Mermaid diagrams, versioned with the code, reviewed in the same pull request as the change.
- **Definition of Done includes docs**: a change that alters behaviour, data, setup or decisions isn't done until the relevant doc is updated.
- `docs/README.md` indexes every document with one line each.
- Person-facing documents can additionally be exported or published (PDF, Word, Google Docs, doc tools) when they need to share them; the Markdown stays the source.
- Small projects: fewer files — a single `docs/project.md` combining brief, design, tests and guide is fine.

## 7. Structure guard

AI-built projects decay into one giant file, duplicate helpers and random folders. Before adding any code:
- Decide where it belongs according to the folder map in `AGENTS.md`; if nowhere fits, update the map first.
- One responsibility per file; split files that grow past a few hundred lines or mix concerns.
- Reuse existing helpers; search before writing a new one.
- No stray files in the root; scripts go in `scripts/`, experiments in a clearly named branch or `scratch/` that isn't shipped.
- At each milestone, run a short **structure review**: dead code, duplicates, oversized files, unclear names, folders that no longer match the map. Fix as tasks (label `chore`).

For an existing messy project: don't rewrite. Map what exists, write the target structure into `AGENTS.md`, and move toward it incrementally with tests protecting behaviour.

## 8. Working across different AI tools (only when switching tools)

- The scaffold and memory files are plain Markdown + git, so every tool can read them.
- Don't rely on any tool's private memory, chat history or proprietary features for project knowledge; if a tool stores something useful, copy it into the project files.
- Capabilities differ by tool (terminal, git, browser, sub-agents, connectors). At session start, check what's available and plan accordingly; if a step needs a capability this tool lacks, say which tool or step the person should use and prepare everything for it.
- When the person switches tools mid-project, the session end protocol in the old tool + start protocol in the new one makes the switch safe.

## 9. Chat → coding agent handoff (only in chat-only environments)

Chat environments are good for discovery, planning, design, documents and prototypes, but usually can't keep a persistent project folder, run git, or deploy. When the build stage arrives in a chat-only environment:

1. **Say it plainly and early** (before the person expects code from chat): "Ab asal software banane ke liye coding tool behtar hai — Claude Code (desktop app ya terminal), Cursor, Codex ya Antigravity, jo aap use karte hain. Main sab tayyar kar deta hoon taake wahan se bilkul wahin se shuru ho."
2. **Prepare the handoff pack** as files the person can download (or, if a connector is available, put straight into their repo/drive):
   - the full scaffold (§1) with `AGENTS.md`, `PROJECT_STATE.md` (status: "ready to build, M1 next"), `README.md`, `.gitignore`, `.env.example`
   - all documents so far in `docs/` (brief, design, UX/UI, data dictionary, plans, test plan, decisions)
   - any prototype code from the chat in `src/` or `prototypes/`
   - the task board export or link
3. **Give a first prompt to paste** in the coding agent:
   ```
   Is folder mein AGENTS.md aur PROJECT_STATE.md parho, phir docs/README.md.
   hire-an-engineer skill follow karo. Milestone M1 shuru karo:
   pehle implementation plan banao, phir test-first build.
   ```
4. **Tell them exactly where to put the folder** and how to open it in their tool (copy-paste steps).
5. In the coding agent, the session start protocol (§3) picks up from `PROJECT_STATE.md`: full build, git, tests and deploy continue there.

The same works in reverse: if they come back to chat to plan v2 or write documents, ask them to share `PROJECT_STATE.md` (and relevant docs) first, and give them updated files to drop back into the repo.

## 10. Templates

See `templates.md`.
