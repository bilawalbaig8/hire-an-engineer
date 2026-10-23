#!/usr/bin/env python3
"""Zip the local evals/ folder into a backup folder outside the repo.

The evals (cases, fixtures, answer keys) are git-ignored on purpose: the answer keys must never be published. That
leaves them on one disk, so this script keeps dated zip copies somewhere else. Default folder: next to the repo,
`<repo parent>/hire-an-engineer-evals-backup`. The newest --keep copies stay; older ones are deleted.

Usage: python scripts/backup_evals.py [--dest DIR] [--keep N]
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PREFIX = "evals-"


def backup(repo: Path, dest: Path, keep: int = 5) -> Path | None:
    src = repo / "evals"
    if not src.is_dir():
        print(f"nothing to back up: {src} does not exist")
        return None
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / f"{PREFIX}{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.zip"
    count = 0
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, f.relative_to(repo).as_posix())
                count += 1
    print(f"backed up {count} files to {target}")
    old = sorted(dest.glob(f"{PREFIX}*.zip"))[:-keep] if keep > 0 else []
    for f in old:
        f.unlink()
        print(f"removed old copy {f.name}")
    return target


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--dest", type=Path, default=REPO_ROOT.parent / "hire-an-engineer-evals-backup")
    p.add_argument("--keep", type=int, default=5)
    args = p.parse_args(argv)
    backup(REPO_ROOT, args.dest.resolve(), args.keep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
