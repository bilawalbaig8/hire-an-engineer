# Project Memory & Structure

The person switches between AI tools (chat, Claude Code, Cursor, Codex, Antigravity, others). Every new session or tool starts with no memory.

**Rule: memory lives in the project's files, not in any chat or tool.** Any agent, any day, can open the project, read a few files, and continue where the last one stopped.

## 1. Standard project scaffold

Minimum by size:

| Size | Create |
|---|---|
| Tiny | git, AGENTS.md, CLAUDE.md (one line), PROJECT_STATE.md, README.md, .gitignore |
| Small | Tiny + CHANGELOG.md + docs/project.md (brief, design, plan, tests in one file) + docs/decisions/ once the first decision exists |
| Medium / Large | Full tree in `documents.md` §6; grow into it, don't create empty folders |

Other tools' rule files (Cursor rules, `GEMINI.md`) just point to `AGENTS.md`: exactly one source of rules. Check the current conventions of the person's tools rather than assuming file names. Documents kept in an external tool (Google Docs, Notion): the repo keeps a link and short summary in `docs/README.md`; the repo stays the source of truth.

## 2. The memory files

| File | Holds | Updated |
|---|---|---|
| `AGENTS.md` | Purpose, stack, run/test, folder map, conventions, rules, where docs live, the protocols below | When conventions change |
| `PROJECT_STATE.md` | Version and milestone, active branch, in progress, next 3 tasks, blockers, open questions, last session summary, known issues, language and tone, cost mode and budget, accounts (owner, created or not), pending approvals, Authorization (never trimmed), last environment used | Every checkpoint |
| `docs/decisions/` | One short record per significant decision | When decided |
| `docs/plans/roadmap.md` + board link | Versions, milestones, priorities | Each milestone |
| `CHANGELOG.md` | What changed per version | Each release |

Templates: `templates.md`.

## 3. Session start protocol

1. Read `AGENTS.md` and `PROJECT_STATE.md` (and the task board if linked).
2. Check the repo: current branch, uncommitted changes, last commits, do tests pass?
3. If anything contradicts the state file, reconcile first and note it.
4. Check tripwires (SKILL.md): personal data, money, login, public URL, deploy → normal lane + security pass.
5. Tell the person in 2–3 lines: where we are, what you'll do now, what you need from them.

No memory files yet (existing project, or started without this skill): **first create them** from the code and what the person remembers. Often the most useful first step for a stuck project.

Chat-only: ask them to upload `PROJECT_STATE.md` at the start; at the end, hand back the whole updated file, never a diff.

## 4. Checkpoints

Sessions end unexpectedly (context runs out, crash, closed window). Don't wait for the end.

**Trigger: every completed task or commit.** About every 20 minutes is a backstop where a clock is available (`date`, or the `Last updated` line in `PROJECT_STATE.md`). No clock: also checkpoint every 10–15 significant actions and when the conversation gets long.

**Also checkpoint immediately:** before anything risky (migrations, big refactors, deploys, deletes); after any decision the person makes; when switching tasks or getting stuck; when they step away. Also checkpoint at the end of every reply that ends a session turn during `delivery-loop.md` §2 (questions asked, assumptions, next step).

**A checkpoint is small:**
1. **Commit** work in progress on its branch with a clear message. Never stash: stashes are invisible to other tools. Tiny projects working on `main`: checkpoint on a `wip/` branch; only passing work reaches `main`.
2. Edit only the changed lines in `PROJECT_STATE.md`: active branch, in-progress task with the exact next step, blockers, questions, `Last updated`.
3. Append one line to the session log in `PROJECT_STATE.md` (trimmed at session end).
4. A decision record only if a decision was made.

Every timestamp comes from the `date` command; never write a time you did not read. A checkpoint is a commit plus a one-line Done/Next edit; the full rewrite is for session end. `PROJECT_STATE.md` 'Done recently' and 'Next up' are rewritten at every checkpoint; stale state at delivery is a defect.

Never interrupt the person to announce one; at most a short line at the end of a message.

## 5. Session end protocol

1. Commit work in progress on its branch; note test status.
2. Update `PROJECT_STATE.md`; re-check "In progress" against git (branch, last commit).
3. Trim it: move the session log and done items to `CHANGELOG.md` or `docs/history.md`; keep each section ≤ ~5 lines. Never trim Authorization.
4. Record decisions; update affected docs, board, changelog.
5. Tell the person in one line what's saved and what's next.

## 6. Structure guard

AI-built projects decay into one giant file, duplicate helpers and random folders. Before adding code:
- Place it by the folder map in `AGENTS.md`; if nothing fits, update the map first.
- One responsibility per file; split files that grow past a few hundred lines or mix concerns.
- Search for an existing helper before writing one.
- No stray root files; scripts in `scripts/`, experiments in a named branch or unshipped `scratch/`.
- Each milestone: a short structure review (dead code, duplicates, oversized files, unclear names, folders off the map); fix as `chore` tasks.

Existing messy project: don't rewrite. Map what exists, write the target structure into `AGENTS.md`, move toward it incrementally with tests.

## 7. Switching tools, chat → coding agent

See `handoff.md`.
