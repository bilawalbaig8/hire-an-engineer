#!/usr/bin/env python3
"""Check a skill's references/sources.md and that every S-AREA-n citation points at it.

Usage: python scripts/check_sources.py skills/<name>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HEADER = ["ID", "Title", "Author", "Year", "URL", "Use", "Cost/licence", "Status"]
ID_RE = re.compile(r"^S-[A-Z]+-\d+$")
REF_RE = re.compile(r"\bS-[A-Z]+-\d+\b")
SEPARATOR_RE = re.compile(r"^:?-+:?$")
STATUSES = ("verified", "unverified")


def _cells(line: str) -> list[str]:
    parts = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [c.replace("\\|", "|").strip() for c in parts]


def load_sources(path: Path) -> tuple[dict[str, str], list[str]]:
    """Return ({id: status}, errors) for the source tables in a sources.md file."""
    statuses: dict[str, str] = {}
    first_line: dict[str, int] = {}
    errors: list[str] = []
    header_seen = False
    in_table = False
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip().startswith("|"):
            in_table = False
            continue
        cells = _cells(line)
        if [c.lower() for c in cells] == [h.lower() for h in HEADER]:
            header_seen = True
            in_table = True
            continue
        if not in_table or all(SEPARATOR_RE.match(c) for c in cells):
            continue
        where = f"{path}:{n}:"
        if len(cells) != len(HEADER):
            errors.append(f"{where} row has {len(cells)} cells, expected {len(HEADER)} columns")
            continue
        id_, url, status = cells[0], cells[4], cells[7]
        if not ID_RE.match(id_):
            errors.append(f"{where} ID '{id_}' must look like S-AREA-n (capital letters, then a number)")
            continue
        if id_ in first_line:
            errors.append(f"{where} duplicate ID {id_} (first used on line {first_line[id_]})")
        else:
            first_line[id_] = n
            statuses[id_] = status
        if status not in STATUSES:
            errors.append(f"{where} Status '{status}' must be verified or unverified")
        if not url.startswith("http"):
            errors.append(f"{where} URL '{url}' must start with http")
    if not header_seen:
        errors.append(f"{path}: no table with columns {' | '.join(HEADER)}")
    return statuses, errors


def check_sources(path: Path) -> list[str]:
    return load_sources(path)[1]


def check_refs(skill_dir: Path) -> list[str]:
    refs_dir = skill_dir / "references"
    sources = refs_dir / "sources.md"
    if not sources.exists():
        return [f"{sources}: missing"]
    statuses, _ = load_sources(sources)
    errors: list[str] = []
    for md in sorted(refs_dir.glob("*.md")):
        if md.name == "sources.md":
            continue
        for n, line in enumerate(md.read_text(encoding="utf-8-sig").splitlines(), 1):
            for m in REF_RE.finditer(line):
                id_ = m.group(0)
                where = f"{md}:{n}:"
                if id_ not in statuses:
                    errors.append(f"{where} {id_} is unknown (not in sources.md)")
                elif statuses[id_] == "unverified" and "unverified" not in line.lower():
                    errors.append(f"{where} {id_} is unverified; say 'unverified' on the same line or cite a verified source")
    return errors


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: python scripts/check_sources.py skills/<name>", file=sys.stderr)
        return 2
    skill_dir = Path(args[0])
    sources = skill_dir / "references" / "sources.md"
    if not sources.exists():
        print(f"skipped: {sources} not found")
        return 0
    errors = check_sources(sources) + check_refs(skill_dir)
    for e in errors:
        print("✗ " + e)
    if errors:
        return 1
    print(f"✓ {sources}: sources and citations ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
