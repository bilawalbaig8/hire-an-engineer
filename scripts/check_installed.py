#!/usr/bin/env python3
"""Check that the installed copies of the team match the repo.

Compares the team's skills (skills/<name>) and agent files (agents/<name>.md) in the repo with the Claude Code folder
(default ~/.claude), ignoring line endings. Exit 0 when everything is the same, 1 when something is missing or
differs. Run `python scripts/install_agents.py --only NAME --force` to fix a difference (only for our own skills).

Usage: python scripts/check_installed.py [--dest DIR] [--only NAME ...]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# The owner's own generalist skill is installed by hand and may be newer; never reported here.
SKIP = {"hire-an-engineer"}


def _norm(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def compare(repo: Path, dest: Path, only: list[str] | None = None) -> list[str]:
    """Return one line per missing or different file (empty list: all same)."""
    problems: list[str] = []
    skills = sorted(d.name for d in (repo / "skills").iterdir() if d.is_dir() and d.name not in SKIP)
    for name in skills:
        if only and name not in only:
            continue
        for f in sorted((repo / "skills" / name).rglob("*")):
            if not f.is_file() or "__pycache__" in f.parts:
                continue
            rel = f.relative_to(repo / "skills" / name)
            g = dest / "skills" / name / rel
            if not g.exists():
                problems.append(f"missing {g}")
            elif _norm(f) != _norm(g):
                problems.append(f"differs {g}")
    for f in sorted((repo / "agents").glob("*.md")):
        if only and f.stem not in only:
            continue
        g = dest / "agents" / f.name
        if not g.exists():
            problems.append(f"missing {g}")
        elif _norm(f) != _norm(g):
            problems.append(f"differs {g}")
    return problems


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--dest", type=Path, default=Path.home() / ".claude")
    p.add_argument("--only", action="append", default=None)
    args = p.parse_args(argv)
    problems = compare(REPO_ROOT, args.dest.resolve(), args.only)
    for line in problems:
        print(line)
    print("all installed copies match the repo" if not problems else f"{len(problems)} file(s) missing or different")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
