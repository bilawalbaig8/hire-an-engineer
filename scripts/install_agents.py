"""Copy the repo's skills and agents into a Claude Code folder (default ~/.claude).

Never overwrites a file that differs unless --force is given.
Usage: python scripts/install_agents.py [--dest PATH] [--dry-run] [--force] [--verbose]
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Action:
    kind: Literal["new", "same", "differs"]
    src: Path
    dst: Path


def _skip(path: Path, base: Path) -> bool:
    return any(p.startswith(".") or p == "__pycache__" for p in path.relative_to(base).parts)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _classify(src: Path, dst: Path) -> Action:
    if not dst.exists():
        return Action("new", src, dst)
    kind = "same" if _digest(src) == _digest(dst) else "differs"
    return Action(kind, src, dst)


def plan_install(src_root: Path, dest: Path) -> list[Action]:
    actions: list[Action] = []
    skills = src_root / "skills"
    if skills.is_dir():
        for f in sorted(skills.rglob("*")):
            if f.is_file() and not _skip(f, skills):
                actions.append(_classify(f, dest / "skills" / f.relative_to(skills)))
    agents = src_root / "agents"
    if agents.is_dir():
        for f in sorted(agents.glob("*.md")):
            if f.is_file() and not f.name.startswith("."):
                actions.append(_classify(f, dest / "agents" / f.name))
    return actions


def install(
    src_root: Path,
    dest: Path,
    force: bool = False,
    dry_run: bool = False,
    verbose: bool = False,
) -> int:
    actions = plan_install(src_root, dest)
    for a in actions:
        if a.kind != "same" or verbose:
            print(f"{a.kind} {a.dst}")
    counts = {k: sum(1 for a in actions if a.kind == k) for k in ("new", "same", "differs")}
    print(f"{counts['new']} new, {counts['same']} same, {counts['differs']} differ")
    if dry_run:
        return 0
    differing = [a.dst for a in actions if a.kind == "differs"]
    if differing and not force:
        listing = "\n".join(f"  {p}" for p in differing)
        raise FileExistsError(
            f"{len(differing)} file(s) differ and were not overwritten (use --force):\n{listing}"
        )
    written = 0
    for a in actions:
        if a.kind == "same":
            continue
        a.dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(a.src, a.dst)
        written += 1
    return written


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--dest", type=Path, default=Path.home() / ".claude")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args(argv)
    try:
        install(REPO_ROOT, args.dest, force=args.force, dry_run=args.dry_run, verbose=args.verbose)
    except FileExistsError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
