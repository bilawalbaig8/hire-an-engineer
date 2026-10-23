#!/usr/bin/env python3
"""Copy the office runtime into skills/team-start/runtime so the global skill is self-contained.

Usage: python scripts/sync_team_start.py [--check]

The sources stay where they are (scripts/, docs/agents/); the copy is what gets installed into ~/.claude with
install_agents.py --only team-start. --check changes nothing and exits 1 when a copy is missing or out of date.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNTIME = REPO_ROOT / "skills" / "team-start" / "runtime"
PAIRS = (
    ("scripts/office_server.py", "office_server.py"),
    ("scripts/office_launch.py", "office_launch.py"),
    ("scripts/log_event.py", "log_event.py"),
    ("scripts/agent_contract.py", "agent_contract.py"),
    ("scripts/check_roster.py", "check_roster.py"),
    ("docs/agents/roster.md", "roster.md"),
    ("docs/agents/visual-office/index.html", "ui/index.html"),
    ("docs/agents/visual-office/mock-v2.html", "ui/mock-v2.html"),
)


def _same(a: Path, b: Path) -> bool:
    return b.is_file() and a.read_bytes().replace(b"\r\n", b"\n") == b.read_bytes().replace(b"\r\n", b"\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    stale = []
    for src_rel, dst_rel in PAIRS:
        src, dst = REPO_ROOT / src_rel, RUNTIME / dst_rel
        if not src.is_file():
            print(f"error: missing source {src}", file=sys.stderr)
            return 2
        if _same(src, dst):
            continue
        stale.append(dst_rel)
        if not args.check:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
    if args.check:
        for name in stale:
            print(f"out of date: {name}")
        return 1 if stale else 0
    print(f"copied {len(stale)} file(s)" if stale else "runtime already in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
