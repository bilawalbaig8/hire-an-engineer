#!/usr/bin/env python3
"""Package a skill folder into <name>.skill (zip) and <name>.zip in an output dir."""
import sys, zipfile
from pathlib import Path

skill_dir = Path(sys.argv[1]).resolve()
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
