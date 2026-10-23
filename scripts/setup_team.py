#!/usr/bin/env python3
"""Put the whole specialist team and the virtual office into one project, in one command.

Usage: python scripts/setup_team.py --project DIR [--dry-run] [--force] [--no-default-agent]

Does what `install_agents.py --dest DIR/.claude --only orchestrator --only software-architect --only code-reviewer --only ai-engineer --only data-scientist
--only backend-engineer`
and `install_office.py --project DIR` do, together: skills and agents in DIR/.claude, the office in DIR/.agents/office,
the hooks and the deny rule in DIR/.claude/settings.json, and (unless --no-default-agent) the project's default agent
set to the boss, so plain `claude` in DIR starts the Orchestrator. Never touches anything outside DIR, never deletes,
never overwrites a file that differs unless --force is given. Run it again any time: it only reports "same".
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import install_agents  # noqa: E402
import install_office  # noqa: E402

TEAM = ("orchestrator", "software-architect", "code-reviewer", "ai-engineer", "data-scientist", "backend-engineer")
REPO_ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--project", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--no-default-agent", action="store_true")
    args = p.parse_args(argv)
    project = args.project.resolve()
    if not project.is_dir():
        print(f"error: project folder not found: {project}", file=sys.stderr)
        return 2
    try:
        print("== skills and agents")
        install_agents.install(REPO_ROOT, project / ".claude", force=args.force, dry_run=args.dry_run, only=list(TEAM))
        print("== office, hooks, settings")
        install_office.install(REPO_ROOT, project, force=args.force, dry_run=args.dry_run,
                               default_agent=not args.no_default_agent)
    except FileExistsError as e:
        print(e, file=sys.stderr)
        return 1
    except (ValueError, FileNotFoundError, NotADirectoryError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if args.dry_run:
        print("\nDry run: nothing was written.")
        return 0
    agent_line = ("  Start the boss:   claude   (plain claude in this folder starts the Orchestrator)"
                  if not args.no_default_agent else "  Start the boss:   claude --agent orchestrator")
    print("\nTeam is ready in", project)
    print(agent_line)
    print("  Office window:    opens by itself at session start; else: python .agents/office/office_launch.py --status")
    print("  Stop the office:  python .agents/office/office_launch.py --stop")
    return 0


if __name__ == "__main__":
    sys.exit(main())
