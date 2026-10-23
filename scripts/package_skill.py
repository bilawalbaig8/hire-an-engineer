#!/usr/bin/env python3
"""Package a skill folder into <name>.skill (zip) and <name>.zip in an output dir.

Agent files agents/<role>.md whose frontmatter `skill` matches the skill name are
added under agents/ at the archive root, next to the <name>/ folder.
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

import yaml


def agent_files_for_skill(skill_name: str, agents_dir: Path) -> list[Path]:
    """Return the agents/*.md files whose frontmatter `skill` equals skill_name."""
    agents_dir = Path(agents_dir)
    if not agents_dir.is_dir():
        return []
    found = []
    for f in sorted(agents_dir.glob("*.md")):
        m = re.match(r"^---\n(.*?)\n---\n", f.read_text(encoding="utf-8"), re.S)
        fm = None
        if m:
            try:
                fm = yaml.safe_load(m.group(1))
            except yaml.YAMLError:
                fm = None
        if not isinstance(fm, dict):
            print(f"warning: agents/{f.name} skipped: cannot read frontmatter", file=sys.stderr)
            continue
        if fm.get("skill") == skill_name:
            found.append(f)
    return found


def main(argv: list[str]) -> int:
    skill_dir = Path(argv[1]).resolve()
    if not (skill_dir / "SKILL.md").is_file():
        print(f"error: {skill_dir} is not a skill folder (no SKILL.md)", file=sys.stderr)
        return 2
    out_dir = Path(argv[2] if len(argv) > 2 else "dist").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    name = skill_dir.name
    agents = agent_files_for_skill(name, skill_dir.parent.parent / "agents")
    for ext in (".skill", ".zip"):
        target = out_dir / f"{name}{ext}"
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(skill_dir.rglob("*")):
                if f.is_file() and not f.name.startswith(".") and "__pycache__" not in f.parts:
                    z.write(f, Path(name) / f.relative_to(skill_dir))
            for a in agents:
                z.write(a, Path("agents") / a.name)
        print(f"packaged {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
