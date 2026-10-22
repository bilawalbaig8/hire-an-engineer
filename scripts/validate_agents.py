#!/usr/bin/env python3
"""Validate every agents/<role>.md (optional argument: another project root): frontmatter, linked skill folder, and the Handoff section."""
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
    # The Claude Code docs allow a comma-separated string or a YAML list.
    items = [t.strip() for t in tools.split(",")] if isinstance(tools, str) else tools
    if not isinstance(items, list) or not items or not all(isinstance(t, str) and t.strip() for t in items):
        errors.append("tools must be a comma-separated string or a YAML list, with no empty items")
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


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:] if argv is None else argv
    root = Path(args[0]) if args else ROOT
    agents_dir = root / "agents"
    files = sorted(agents_dir.glob("*.md")) if agents_dir.is_dir() else []
    if not files:
        print("No agents found")
        return 0
    failed = False
    for f in files:
        errs = validate_agent_file(f, root / "skills")
        if errs:
            failed = True
            for e in errs:
                print(f"✗ {f.name}: {e}")
        else:
            print(f"✓ {f.stem}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
