#!/usr/bin/env python3
"""Check docs/agents/roster.md against agents/*.md.

The roster is a table with the columns Name | Skill | Model | Owns. Every row needs an agent file with the same
model and skill, and every agent file except the boss (`orchestrator`) needs a row.

Usage: python scripts/check_roster.py [ROSTER] [--agents DIR]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BOSS = "orchestrator"


def _frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    found: dict[str, str] = {}
    if m:
        for line in m.group(1).splitlines():
            key, sep, value = line.partition(":")
            if sep and key and not key[0].isspace():
                found.setdefault(key.strip(), value.strip())
    return found


def _rows(text: str) -> list[list[str]] | None:
    """Data rows of the first table whose header is Name | Skill | Model | Owns, or None."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        cells = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        if cells == ["name", "skill", "model", "owns"]:
            rows = []
            for row in lines[i + 2:]:
                if not row.strip().startswith("|"):
                    break
                rows.append([c.strip() for c in row.strip().strip("|").split("|")])
            return rows
    return None


def check_roster(roster: Path, agents_dir: Path) -> list[str]:
    try:
        text = roster.read_text(encoding="utf-8-sig")
    except OSError as e:
        return [f"{roster}: cannot read ({e})"]
    rows = _rows(text)
    if rows is None:
        return [f"{roster}: no table with the columns Name | Skill | Model | Owns"]
    errors: list[str] = []
    seen: set[str] = set()
    for row in rows:
        if len(row) != 4:
            errors.append(f"{roster}: row {row!r} must have 4 cells")
            continue
        name, skill, model, owns = row
        if name in seen:
            errors.append(f"{roster}: duplicate row for {name}")
            continue
        seen.add(name)
        if not owns:
            errors.append(f"{roster}: {name} has an empty owns cell")
        path = agents_dir / f"{name}.md"
        if not path.is_file():
            errors.append(f"{roster}: {name} has no agent file {path}")
            continue
        front = _frontmatter(path)
        if front.get("model") != model:
            errors.append(f"{path}: model is {front.get('model')!r}, roster says {model!r}")
        if front.get("skill") != skill:
            errors.append(f"{path}: skill is {front.get('skill')!r}, roster says {skill!r}")
    if agents_dir.is_dir():
        for path in sorted(agents_dir.glob("*.md")):
            if path.stem != BOSS and path.stem not in seen:
                errors.append(f"{path}: {path.stem} is not in the roster")
    return errors


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("roster", nargs="?", type=Path, default=REPO_ROOT / "docs" / "agents" / "roster.md")
    p.add_argument("--agents", type=Path, default=REPO_ROOT / "agents")
    args = p.parse_args(argv)
    errors = check_roster(args.roster, args.agents)
    for e in errors:
        print(e, file=sys.stderr)
    if not errors:
        print(f"ok: {args.roster}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
