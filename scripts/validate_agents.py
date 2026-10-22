#!/usr/bin/env python3
"""Validate every agents/<role>.md: frontmatter, linked skill folder, and the Handoff section."""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MODELS = {"opus", "sonnet", "haiku", "inherit"}


def validate_agent_file(path: Path, skills_dir: Path) -> list:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        return ["missing YAML frontmatter"]
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return [f"invalid YAML frontmatter: {e}"]
    if not isinstance(fm, dict):
        return ["frontmatter must be a YAML mapping"]
    body = m.group(2)
    errors = []

    if fm.get("name") != path.stem:
        errors.append(f"frontmatter name '{fm.get('name')}' must match file name '{path.stem}'")
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append("empty description")
    elif len(desc) > 1024:
        errors.append(f"description is {len(desc)} chars (max 1024)")
    if fm.get("model") not in MODELS:
        errors.append(f"model '{fm.get('model')}' must be one of {', '.join(sorted(MODELS))}")
    tools = fm.get("tools")
    if not isinstance(tools, list) or not tools or not all(isinstance(t, str) and t.strip() for t in tools):
        errors.append("tools must be a YAML list of non-empty strings")
    skill = fm.get("skill")
    if not isinstance(skill, str) or not skill.strip():
        errors.append("missing skill")
    elif not (Path(skills_dir) / skill).is_dir():
        errors.append(f"skill folder '{skill}' not found under {Path(skills_dir).name}/")

    lines = body.splitlines()
    if "## Handoff" not in lines:
        errors.append("body must contain a '## Handoff' heading")
    else:
        section = []
        for line in lines[lines.index("## Handoff") + 1:]:
            if re.match(r"^#{1,2} ", line):
                break
            section.append(line)
        if "handoff-contract.md" not in "\n".join(section):
            errors.append("'## Handoff' section must mention handoff-contract.md")
    return errors


def main() -> int:
    agents_dir = ROOT / "agents"
    files = sorted(agents_dir.glob("*.md")) if agents_dir.is_dir() else []
    if not files:
        print("No agents found")
        return 0
    failed = False
    for f in files:
        errs = validate_agent_file(f, ROOT / "skills")
        if errs:
            failed = True
            for e in errs:
                print(f"✗ {f.name}: {e}")
        else:
            print(f"✓ {f.stem}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
