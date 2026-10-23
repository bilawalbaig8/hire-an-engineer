# Put the virtual office into your project

The office is a small window that shows your agent team working. One command installs it into any project folder.
You need Python 3 only (nothing to download).

## Install

Install the team first (once per project), then the office:

```
python scripts/install_agents.py --dest <project>/.claude
python scripts/install_office.py --project <project> --dry-run    # preview: shows what would change
python scripts/install_office.py --project <project>              # do it
```

What it does, all inside `<project>`:

- copies the office files to `.agents/office/` (server, launcher, event logger, window page, team list);
- adds the office hooks and a deny rule (agents may not write to `/.agents/**`) to `.claude/settings.json`, keeping everything already there;
- adds an `office` entry to `.mcp.json`, keeping every other entry. If you already have an `office` entry it is left alone and reported.

Running it again is safe: it says "all same". If a copied file was edited by you it refuses and lists it; use `--force` to replace it.
It never adds allow or ask permission rules. It prints the optional ones so you can decide.

## Use it

- Start the team: `claude --agent orchestrator`. The window opens by itself (once per session).
- Find the window again: `python .agents/office/office_launch.py --status` prints the address (http://127.0.0.1:8765/ or the next free port).
- Stop it: `python .agents/office/office_launch.py --stop`.
- Headless runs (`claude -p`): add `--allowedTools "Bash(python .claude/skills/orchestrator/scripts/team_event.py:*)" mcp__office`.

The team list comes from `<project>/docs/agents/roster.md` if you have one, else the installed `.agents/office/roster.md`
(or `--roster FILE` on `office_server.py`), else the names in `.claude/agents/*.md`.

## Update

Pull the repo, run `install_office.py` again; changed files are listed as "differs", add `--force` to take the new ones.
To remove: delete `.agents/office/`, the office hooks in `.claude/settings.json`, and the `office` entry in `.mcp.json`.
