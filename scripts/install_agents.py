"""Copy the repo's skills and agents into a Claude Code folder (default ~/.claude).

Never overwrites a file that differs unless --force is given.
With --only NAME (repeatable) it plans just that skill folder and the agent files that name it
(`skill: NAME` in their frontmatter); nothing else is read, compared or written.
Usage: python scripts/install_agents.py [--dest PATH] [--only NAME ...] [--dry-run] [--force] [--verbose]
"""
from __future__ import annotations

import argparse
import hashlib
import re
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


def _agent_skill(path: Path) -> str | None:
    """The `skill:` value in an agent file's frontmatter, or None."""
    text = path.read_text(encoding="utf-8-sig")
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None
    found = re.search(r"^skill:\s*(\S+)\s*$", m.group(1), re.M)
    return found.group(1) if found else None


def plan_install(src_root: Path, dest: Path, only: list[str] | None = None) -> list[Action]:
    actions: list[Action] = []
    skills = src_root / "skills"
    if only:
        available = sorted(d.name for d in skills.iterdir() if d.is_dir()) if skills.is_dir() else []
        unknown = [name for name in only if name not in available]
        if unknown:
            raise ValueError(
                f"unknown skill(s): {', '.join(unknown)}. Available: {', '.join(available) or 'none'}"
            )
    wanted = set(only) if only else None
    if skills.is_dir():
        for f in sorted(skills.rglob("*")):
            if not f.is_file() or _skip(f, skills):
                continue
            if wanted is not None and f.relative_to(skills).parts[0] not in wanted:
                continue
            actions.append(_classify(f, dest / "skills" / f.relative_to(skills)))
    agents = src_root / "agents"
    if agents.is_dir():
        for f in sorted(agents.glob("*.md")):
            if not f.is_file() or f.name.startswith("."):
                continue
            if wanted is not None and _agent_skill(f) not in wanted:
                continue
            actions.append(_classify(f, dest / "agents" / f.name))
    return actions


def install(
    src_root: Path,
    dest: Path,
    force: bool = False,
    dry_run: bool = False,
    verbose: bool = False,
    only: list[str] | None = None,
) -> int:
    actions = plan_install(src_root, dest, only=only)
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
    p.add_argument("--only", action="append", metavar="NAME", help="install only this skill and its agent files (repeatable)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args(argv)
    try:
        install(REPO_ROOT, args.dest, force=args.force, dry_run=args.dry_run, verbose=args.verbose, only=args.only)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
    except FileExistsError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
