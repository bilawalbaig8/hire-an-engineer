# Agent team: map of the project

The specialist team (a boss and specialists) lives in this repo next to the older `hire-an-engineer` skill. This page says where everything is, which file is the source of truth for which fact, and how to keep it safe.

## Where things are
| Folder or file | What it holds |
|---|---|
| `agents/<name>.md` | One thin file per specialist: who it is, model, tools, how it answers. `orchestrator.md` is the boss. |
| `skills/<role>/` | The knowledge of a role: `SKILL.md` (short router), `references/` (topics, one `method-*.md` per mode, `sources.md`, `credits.txt`). |
| `docs/agents/roster.md` | The single list of specialists the boss may call. |
| `docs/agents/roles/<role>.md` | The role document for the owner: what the role is, does, owns, and where it learned it. |
| `docs/superpowers/specs/` | Design decisions per role (why it was built this way). `plans/` holds implementation plans. |
| `docs/agents/agent-template/` | The checklist for building a new role and the handoff contract. |
| `docs/agents/visual-office/` | The live office window (UI, launch notes, event mapping). |
| `docs/agents/reports/` | Test reports. |
| `scripts/` | Validators, installers, the office server, event logging, backups. |
| `tests/` | The automatic tests. |
| `evals/` | Local only (git-ignored): eval cases, fixtures and answer keys. Back it up with `scripts/backup_evals.py`. |
| `TASKS.md`, `CHANGELOG.md`, `THIRD_PARTY_NOTICES.md` | Progress and role order, changes per skill, credits. |

## One source of truth per fact
- Who may be called: `docs/agents/roster.md` (the boss allowlist in `agents/orchestrator.md` must match; `check_roster.py` checks the files).
- What a role does and why: its spec. What the owner reads: its role document. How it works: its skill. Do not copy a rule into a second place; link to it.
- Task and role order: `TASKS.md`. The progress dashboard is a view of it.
- Sources: `skills/<role>/references/sources.md`; only `verified` ones are cited as fact.

## Keeping it safe
- Before a commit: `python scripts/validate_agents.py`, `python scripts/validate_skills.py`, `python scripts/check_roster.py`, `python -m pytest -q`.
- Installed copies match the repo: `python scripts/check_installed.py` (fix a difference with `python scripts/install_agents.py --only NAME --force`; our own skills only, never `hire-an-engineer`).
- Evals survive a lost disk: `python scripts/backup_evals.py` keeps the newest 5 dated zips next to the repo (`hire-an-engineer-evals-backup`). Run it after every eval change.
- Test projects stay local and are deleted after the test.

## Adding a role
Follow `docs/agents/agent-template/README.md` (10 steps). Evals come before knowledge; the role document is written first and approved by the owner; a role is added to the roster in the same commit as its agent file.
