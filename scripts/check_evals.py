#!/usr/bin/env python3
"""Check an evals.json file: {"skill_name": ..., "evals": [...]}.

Every case needs id, prompt, kind (typical|edge|refusal) and expect as a non-empty list of text lines.
Legacy exception: a file where every case uses expected_output and none has kind or expect is
checked with the old rules (id, prompt, expected_output). Mixed files are errors.

Usage: python scripts/check_evals.py evals/<name>/evals.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

KINDS = ("typical", "edge", "refusal")


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_evals(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as e:
        return [f"{path}: cannot read JSON ({e})"]
    if not isinstance(data, dict):
        return [f"{path}: top level must be an object with skill_name and evals"]
    errors: list[str] = []
    if not _text(data.get("skill_name")):
        errors.append(f"{path}: skill_name must be non-empty text")
    cases = data.get("evals")
    if not isinstance(cases, list) or not cases:
        errors.append(f"{path}: evals must be a non-empty list")
        return errors
    legacy = all(
        isinstance(c, dict) and "kind" not in c and "expect" not in c and "expected_output" in c
        for c in cases
    )
    require_kind = not legacy
    seen: set[object] = set()
    for i, case in enumerate(cases):
        where = f"{path}: evals[{i}]"
        if not isinstance(case, dict):
            errors.append(f"{where}: must be an object")
            continue
        id_ = case.get("id")
        if not (_text(id_) or (isinstance(id_, int) and not isinstance(id_, bool))):
            errors.append(f"{where}: id must be a number or text")
        elif id_ in seen:
            errors.append(f"{where}: duplicate id {id_!r}")
        else:
            seen.add(id_)
        if not _text(case.get("prompt")):
            errors.append(f"{where}: prompt must be non-empty text")
        expect = case.get("expect")
        expect_ok = (
            isinstance(expect, list) and bool(expect) and all(_text(x) for x in expect)
        )
        if require_kind:
            if case.get("kind") not in KINDS:
                errors.append(f"{where}: kind {case.get('kind')!r} must be one of {', '.join(KINDS)}")
            if not expect_ok:
                errors.append(f"{where}: expect must be a non-empty list of text lines")
        elif not (expect_ok or _text(case.get("expected_output"))):
            errors.append(f"{where}: needs expected_output text or an expect list")
        if "fixture" in case and not _text(case["fixture"]):
            errors.append(f"{where}: fixture must be non-empty text when present")
    return errors


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: python scripts/check_evals.py evals/<name>/evals.json", file=sys.stderr)
        return 2
    path = Path(args[0])
    if not path.exists():
        print(f"skipped: {path} not found")
        return 0
    errors = check_evals(path)
    for e in errors:
        print("✗ " + e)
    if errors:
        return 1
    print(f"✓ {path}: evals ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
