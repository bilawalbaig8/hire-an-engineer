#!/usr/bin/env python3
"""Add (or remove) the three event-log hooks of the specialist team in the user-level Claude Code settings.

Usage: python scripts/install_global_hooks.py [--settings PATH] [--dry-run] [--remove]

Default settings file: ~/.claude/settings.json. The hooks run the log_event.py that ships inside the team-start skill
(<settings folder>/skills/team-start/runtime/log_event.py) with --only-if-enabled, so they do NOTHING in a folder that
did not switch the team on (no .agents/enabled file). Existing settings and hooks are kept; a backup of the old file is
written once as settings.json.before-team-start; an invalid settings file is refused untouched.
--remove deletes only the hooks this script added.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

MARK = "team-start/runtime/log_event.py"
HOOKS = (("SubagentStart", None), ("SubagentStop", None), ("PostToolUse", "Write|Edit"))


def command_for(settings: Path) -> str:
    script = (settings.parent / "skills" / "team-start" / "runtime" / "log_event.py").as_posix()
    return f'python "{script}" --only-if-enabled'


def _ours(hook) -> bool:
    return isinstance(hook, dict) and MARK in str(hook.get("command", "")).replace("\\", "/")


def load(settings: Path) -> dict:
    if not settings.exists():
        return {}
    try:
        data = json.loads(settings.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as e:
        raise ValueError(f"{settings}: cannot read as JSON ({e}); nothing was changed")
    if not isinstance(data, dict):
        raise ValueError(f"{settings}: top level is not an object; nothing was changed")
    if "hooks" in data and not isinstance(data["hooks"], dict):
        raise ValueError(f"{settings}: 'hooks' is not an object; nothing was changed")
    return data


def add_hooks(data: dict, cmd: str) -> list[str]:
    added = []
    hooks = data.setdefault("hooks", {})
    for event, matcher in HOOKS:
        groups = hooks.setdefault(event, [])
        if not isinstance(groups, list):
            raise ValueError(f"hooks.{event} is not a list; nothing was changed")
        if any(isinstance(g, dict) and any(_ours(h) for h in g.get("hooks", []) or []) for g in groups):
            continue
        hook = {"type": "command", "command": cmd}
        groups.append({"matcher": matcher, "hooks": [hook]} if matcher else {"hooks": [hook]})
        added.append(event)
    return added


def remove_hooks(data: dict) -> list[str]:
    removed = []
    hooks = data.get("hooks")
    if not isinstance(hooks, dict):
        return removed
    for event in list(hooks):
        groups = hooks[event]
        if not isinstance(groups, list):
            continue
        keep = []
        for g in groups:
            if isinstance(g, dict) and isinstance(g.get("hooks"), list):
                rest = [h for h in g["hooks"] if not _ours(h)]
                if len(rest) != len(g["hooks"]):
                    removed.append(event)
                if rest:
                    keep.append({**g, "hooks": rest})
            else:
                keep.append(g)
        if keep:
            hooks[event] = keep
        else:
            del hooks[event]
    if not hooks:
        del data["hooks"]
    return removed


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--settings", type=Path, default=Path.home() / ".claude" / "settings.json")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--remove", action="store_true")
    args = p.parse_args(argv)
    settings = args.settings.expanduser()
    try:
        data = load(settings)
        changed = remove_hooks(data) if args.remove else add_hooks(data, command_for(settings))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    verb = "removed" if args.remove else "added"
    if not changed:
        print("nothing to remove" if args.remove else "already installed: nothing to do")
        return 0
    if args.dry_run:
        print(f"Dry run: would have {verb} hooks for {', '.join(changed)} in {settings}")
        return 0
    settings.parent.mkdir(parents=True, exist_ok=True)
    backup = settings.with_name(settings.name + ".before-team-start")
    if settings.exists() and not backup.exists():
        shutil.copyfile(settings, backup)
    tmp = settings.with_name(settings.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(settings)
    print(f"{verb} hooks for {', '.join(changed)} in {settings}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
