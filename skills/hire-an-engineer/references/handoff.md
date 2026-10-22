# Handoff — switching tools and chat → coding agent

Covers switching AI tools and chat → coding agent only. Handing a project to a person (developer, hire): `documents.md` §5 Handoff & maintenance, `workflow.md` Phase 9.

Read when the person switches AI tools, or when a chat-only environment reaches the build stage.

## Switching tools

- Scaffold and memory files are plain Markdown + git, so every tool can read them.
- Don't rely on any tool's private memory, chat history or proprietary features; copy anything useful into the project files.
- At session start check what this tool can do (terminal, git, browser, sub-agents, connectors). If a step needs a capability it lacks, say which tool to use and prepare everything for it.
- Old tool: session end protocol. New tool: session start protocol (`project-memory.md` §3, §5).

## Chat → coding agent

Chat is good for discovery, plans, design, documents, prototypes. It usually can't keep a project folder, run git or deploy. At the build stage:

1. **Say it plainly and early**, in their language: a coding tool (Claude Code, Cursor, Codex, Antigravity, whichever they use) is better for building the real software; you'll prepare everything so it starts exactly here.
2. **Prepare the handoff pack** as downloadable files (or straight into their repo/drive via a connector):
   - the scaffold (`project-memory.md` §1) with `AGENTS.md`, `PROJECT_STATE.md` ("ready to build, M1 next"), `README.md`, `.gitignore`, `.env.example`
   - all documents so far in `docs/`
   - prototype code in `src/` or `prototypes/`
   - the task board export or link
3. **Give a first prompt to paste** (in English, ending with their language):
   ```
   In this folder, read AGENTS.md and PROJECT_STATE.md, then docs/README.md.
   Follow the hire-an-engineer skill. Start milestone M1: write the
   implementation plan first, then build test-first.
   Reply to me in [their language].
   ```
4. **Tell them exactly where to put the folder** and how to open it in their tool (copy-paste steps).
5. The coding agent's session start protocol picks up from `PROJECT_STATE.md`.

Reverse: when they come back to chat to plan v2 or write documents, ask them to upload `PROJECT_STATE.md` (and relevant docs) first; at the end give the updated files to download and drop back into the repo.
