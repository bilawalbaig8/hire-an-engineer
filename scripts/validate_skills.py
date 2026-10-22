#!/usr/bin/env python3
"""Validate every skill under skills/: frontmatter, description length, and referenced files."""
import re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
errors = []

for skill_dir in sorted((ROOT / "skills").iterdir()):
    if not skill_dir.is_dir():
        continue
    skill_md = skill_dir / "SKILL.md"
    name = skill_dir.name
    if not skill_md.exists():
        errors.append(f"{name}: missing SKILL.md"); continue
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{name}: missing YAML frontmatter"); continue
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"{name}: invalid YAML frontmatter: {e}"); continue
    if fm.get("name") != name:
        errors.append(f"{name}: frontmatter name '{fm.get('name')}' must match folder name")
    desc = fm.get("description") or ""
    if not desc:
        errors.append(f"{name}: empty description")
    if len(desc) > 1024:
        errors.append(f"{name}: description is {len(desc)} chars (max 1024)")
    # every `something.md` mentioned in the skill must exist in references/ or the skill root
    mentioned = set(re.findall(r"`([a-z0-9-]+\.md)`", text))
    for ref in (skill_dir / "references").glob("*.md") if (skill_dir / "references").exists() else []:
        mentioned |= set(re.findall(r"`([a-z0-9-]+\.md)`", ref.read_text(encoding="utf-8")))
    allowed_project_files = {"agents.md", "project_state.md", "readme.md", "changelog.md", "claude.md", "gemini.md", "plan.md", "summary.md", "decisions.md"}
    for ref in sorted(mentioned):
        if ref.lower() in allowed_project_files:
            continue
        if not ((skill_dir / "references" / ref).exists() or (skill_dir / ref).exists()):
            errors.append(f"{name}: references missing file `{ref}`")
    lines = text.count("\n")
    if lines > 500:
        errors.append(f"{name}: SKILL.md has {lines} lines (keep under 500)")
    print(f"✓ {name}: description {len(desc)} chars, SKILL.md {lines} lines")

if errors:
    print("\n".join("✗ " + e for e in errors))
    sys.exit(1)
print("All skills valid.")
