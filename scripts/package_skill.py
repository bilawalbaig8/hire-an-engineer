#!/usr/bin/env python3
"""Package a skill folder into <name>.skill (zip) and <name>.zip in an output dir.

Usage: python scripts/package_skill.py <skill-folder> [output-dir]
Example: python scripts/package_skill.py skills/hire-an-engineer dist
"""
import sys, zipfile
from pathlib import Path

USAGE = "Usage: python scripts/package_skill.py <skill-folder> [output-dir]\nExample: python scripts/package_skill.py skills/hire-an-engineer dist"

if len(sys.argv) < 2 or len(sys.argv) > 3 or sys.argv[1] in ("-h", "--help"):
    print(USAGE, file=sys.stderr)
    sys.exit(2)

skill_dir = Path(sys.argv[1]).resolve()
if not skill_dir.is_dir():
    print(f"error: '{sys.argv[1]}' is not a folder.\n{USAGE}", file=sys.stderr)
    sys.exit(2)
if not (skill_dir / "SKILL.md").is_file():
    print(f"error: {skill_dir / 'SKILL.md'} is missing; this is not a skill folder.", file=sys.stderr)
    sys.exit(1)

out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "dist").resolve()
out_dir.mkdir(parents=True, exist_ok=True)
name = skill_dir.name
for ext in (".skill", ".zip"):
    target = out_dir / f"{name}{ext}"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file() and not f.name.startswith("."):
                z.write(f, Path(name) / f.relative_to(skill_dir))
    print(f"packaged {target}")
