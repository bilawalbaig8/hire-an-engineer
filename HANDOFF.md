# Handoff → Claude Code (or any coding agent)

**From:** claude.ai planning session, 2026-10-21
**To:** the coding agent that will publish and maintain this repo
**Owner:** Bilawal (talks in Roman Urdu + English; prefers direct, actionable replies)

Read this file, then `AGENTS.md` and `PROJECT_STATE.md`. Ask the owner before anything that creates, publishes, changes settings or costs money.

---

## 1. What this project is

`hire-an-engineer` — an open-source **agent skill** that turns an AI tool into a senior software engineer / full software team for people who use AI tools (Claude Code, claude.ai, Cursor, Codex, Antigravity) but have **no software engineering background**. Their pains: getting stuck, messy structure, no memory or docs between sessions. The skill does the engineering; it does not teach.

Skill lives in `skills/hire-an-engineer/`:
- `SKILL.md` — lean core (~1.9k tokens): rule priority, session protocol, environment check, fast lane, limits, gap reporting, **router table** to references.
- `references/` — 20 files (project-memory, getting-unstuck, workflow, ui-ux, database, integrations, process-automation, technical-products, cost-management, engineering-discipline/principles, github, versioning-release, project-management, tools-and-stack, documents, plain-language, thinking-toolkit, project-cases, roles).

## 2. Decisions already made (don't re-open without the owner)

| Decision | Detail |
|---|---|
| Name | `hire-an-engineer` (repo and skill) |
| License | MIT; adapted sources credited in `THIRD_PARTY_NOTICES.md` (Superpowers MIT, frontend-design Apache-2.0, Orchestra Research MIT, Anthropic PM/design plugins as inspiration) |
| Contributions | Owner-only. Issues open to everyone; **pull requests disabled**; no collaborators |
| Repo layout | Multi-skill: `skills/<name>/`, `evals/<name>/`, `templates/skill-template/` |
| Releases | Tag `<skill-name>-v<version>` → `.github/workflows/release.yml` validates, packages `.skill` + `.zip`, publishes a GitHub Release |
| Issues | 3 forms (gap / improvement / new skill), auto-triage workflow labels by skill/area/tool and flags possible secrets |
| Skill self-reporting | Skill offers to draft an anonymised gap issue (`gh issue create` or pre-filled link) — only with the user's explicit OK |
| Audience framing | AI-tool users without engineering background; plain language; no teaching |
| Memory | Project memory in files (`AGENTS.md`, `PROJECT_STATE.md`), checkpoint every ~20 min of work |

## 3. Your tasks, in order

### Task 1 — Publish the repo
1. Ask the owner for their **GitHub username** (and confirm repo name `hire-an-engineer`, public).
2. `./scripts/set_owner.sh <username> hire-an-engineer` — fills `bilawalbaig8/hire-an-engineer` and `@bilawalbaig8` placeholders. Verify: `grep -rn "bilawalbaig8/hire-an-engineer\|@bilawalbaig8" .` returns nothing.
3. `python3 scripts/validate_skills.py` (needs `pip install pyyaml`) — must pass.
4. Check `gh auth status`. If not logged in, ask the owner to run `gh auth login` themselves.
5. With owner approval:
   ```bash
   git init -b main && git add . && git commit -m "feat: initial release of hire-an-engineer"
   gh repo create <username>/hire-an-engineer --public --source . --push \
     --description "AI senior software engineer for non-technical builders & vibe coders. Plans, structures, builds, tests, ships & documents your project. Claude Code, Cursor, Codex, Antigravity."
   ./scripts/setup_labels.sh
   gh repo edit --add-topic ai-software-engineer,vibe-coding,claude-code,claude-skills,agent-skills,ai-agents,cursor,codex,antigravity,agents-md,ai-coding-assistant,non-technical-founders,no-code,mvp,software-engineering,project-management,prompt-engineering,context-engineering,developer-tools,llm
   ```
6. Confirm the **Validate skills** workflow ran green on `main` (`gh run list`).

### Task 2 — First release
1. With approval: `git tag hire-an-engineer-v0.1.0 && git push origin hire-an-engineer-v0.1.0`
2. Confirm the Release exists with `hire-an-engineer.skill` and `.zip` attached (`gh release view hire-an-engineer-v0.1.0`). If the workflow fails, debug root-cause first.

### Task 3 — Lock the repo (owner does settings in the browser; you guide step by step)
Follow `docs/OWNER_SETUP.md` §2–3:
- Settings → General → Features → **Pull requests: off**; Issues: on; Wiki: off
- Settings → Collaborators: none
- Settings → Rules → Rulesets: branch ruleset on `main` — block force pushes, restrict deletions, require status check "Validate skills", owner in bypass list
- Settings → Code security: secret scanning, push protection, private vulnerability reporting, Dependabot alerts
- Account: 2FA on
- Optional: social preview image (`docs/GITHUB_ABOUT.md`), a Project board auto-adding issues
You may use `gh api` for settings only if the owner prefers and approves each change.

### Task 4 — Test the skill (most important open item)
Prompts are in `evals/hire-an-engineer/evals.json`; extend them to these four:
1. A stuck, half-built AI-generated project (ideally a real one from the owner)
2. A new medium idea (e.g. bakery orders app)
3. Process automation (invoice emails → sheet)
4. Negative case: an experienced developer's routine coding question (skill should NOT take over)

For each run, record: which reference files were read, whether the right lane (normal/fast) and size were chosen, questions asked before the first visible result, whether memory files were created/updated, token use if visible, and gaps. File each real gap as a GitHub issue (anonymised) and fix in `0.2.0`.

### Task 5 — Fix → release 0.2.0
Fix from issues; `CHANGELOG.md` entry; bump version in README; commit with `Fixes #n`; tag `hire-an-engineer-v0.2.0`.

## 4. Known open items
- Untested (Task 4).
- Skill description is at 1008/1024 chars — new triggers must replace words, not add.
- License of Anthropic PM/design plugin skills not verified; only ideas were paraphrased. Owner may want to double-check before promotion.
- README badges/links depend on Task 1 step 2.

## 5. Rules while working here
- Session start: read `AGENTS.md`, `PROJECT_STATE.md`, check `git status`. Every ~20 min of work and before anything risky: commit + update `PROJECT_STATE.md`. Session end: full update.
- `python3 scripts/validate_skills.py` before every commit.
- Keep `SKILL.md` lean; details go in `references/`.
- Never commit secrets. Never push tags, change settings, or publish without the owner's OK.
- Talk to the owner in Roman Urdu + English, short and direct.
