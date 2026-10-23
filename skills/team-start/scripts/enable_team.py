#!/usr/bin/env python3
"""Turn the specialist team on (or record "solo") for a folder, and start the office window.

Usage: python enable_team.py --project DIR [--no-browser] [--solo]

Team: creates DIR/.agents/enabled (the marker the global hooks look for), removes DIR/.agents/solo, starts the local
office server for DIR (once) and opens the window in the browser unless --no-browser, and prints the address.
Solo: writes DIR/.agents/solo and starts nothing, so the owner is not asked again for this folder.
Writes only inside DIR/.agents. Exit 2 with a message on stderr when DIR does not exist.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent / "runtime"


def office_status(project: Path) -> str:
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
    r = subprocess.run([sys.executable, str(RUNTIME / "office_launch.py"), "--project", str(project), "--status"],
                       capture_output=True, text=True, encoding="utf-8", env=env, timeout=30)
    return r.stdout.strip()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--project", type=Path, required=True)
    p.add_argument("--no-browser", action="store_true")
    p.add_argument("--solo", action="store_true")
    args = p.parse_args(argv)
    project = args.project.resolve()
    if not project.is_dir():
        print(f"error: folder not found: {project}", file=sys.stderr)
        return 2
    agents = project / ".agents"
    agents.mkdir(exist_ok=True)
    if args.solo:
        (agents / "solo").write_text("solo\n", encoding="utf-8")
        enabled = agents / "enabled"
        if enabled.exists():
            enabled.unlink()
        print("Solo mode recorded for this folder; the team is not used.")
        return 0
    (agents / "enabled").write_text("team\n", encoding="utf-8")
    solo = agents / "solo"
    if solo.exists():
        solo.unlink()
    cmd = [sys.executable, str(RUNTIME / "office_launch.py"), "--project", str(project)]
    if args.no_browser:
        cmd.append("--no-browser")
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
    try:
        subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env, timeout=60, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"warning: could not start the office window: {e}", file=sys.stderr)
    status = office_status(project)
    print("Team is on for this folder.")
    print(status if status else "The office window did not start; the team still works without it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
