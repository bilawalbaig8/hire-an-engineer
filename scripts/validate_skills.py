#!/usr/bin/env python3
"""Validate every skill under skills/: frontmatter, description length, and referenced files."""
import re, sys
from pathlib import Path
import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent.parent
errors = []

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
KNOWN_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def read_text(path):
    """Read a file as UTF-8 with line endings normalised to LF (handles CRLF checkouts)."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def path_exists(rel, bases):
    """True if rel (a path like references/x.md, optional #anchor) exists under any base folder."""
    rel = rel.split("#", 1)[0].strip()
    if not rel:
        return True
    return any((base / rel).exists() for base in bases)


for skill_dir in sorted((ROOT / "skills").iterdir()):
    if not skill_dir.is_dir():
        continue
    skill_md = skill_dir / "SKILL.md"
    name = skill_dir.name
    if not skill_md.exists():
        errors.append(f"{name}: missing SKILL.md"); continue
    text = read_text(skill_md)
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{name}: missing YAML frontmatter"); continue
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"{name}: invalid YAML frontmatter: {e}"); continue
    if not isinstance(fm, dict):
        errors.append(f"{name}: frontmatter must be a YAML mapping (key: value lines), got {type(fm).__name__}"); continue
    skill_name = fm.get("name")
    if skill_name != name:
        errors.append(f"{name}: frontmatter name '{skill_name}' must match folder name")
    if isinstance(skill_name, str) and not NAME_RE.match(skill_name):
        errors.append(f"{name}: frontmatter name '{skill_name}' must be lowercase letters, digits and hyphens, at most 64 characters")
    unknown = sorted(str(k) for k in fm if k not in KNOWN_KEYS)
    if unknown:
        errors.append(f"{name}: unknown frontmatter key(s) {', '.join(unknown)} (allowed: {', '.join(sorted(KNOWN_KEYS))})")
    desc = fm.get("description") or ""
    if not isinstance(desc, str):
        errors.append(f"{name}: description must be text"); desc = ""
    if not desc:
        errors.append(f"{name}: empty description")
    if len(desc) > 1024:
        errors.append(f"{name}: description is {len(desc)} chars (max 1024)")
    # every `something.md` mentioned in the skill must exist in references/ or the skill root
    mentioned = set(re.findall(r"`([a-z0-9-]+\.md)`", text))
    refs_dir = skill_dir / "references"
    ref_files = sorted(refs_dir.glob("*.md")) if refs_dir.exists() else []
    for ref in ref_files:
        mentioned |= set(re.findall(r"`([a-z0-9-]+\.md)`", read_text(ref)))
    allowed_project_files = {"agents.md", "project_state.md", "readme.md", "changelog.md", "claude.md", "gemini.md"}
    for ref in sorted(mentioned):
        if ref.lower() in allowed_project_files:
            continue
        if not ((skill_dir / "references" / ref).exists() or (skill_dir / ref).exists()):
            errors.append(f"{name}: references missing file `{ref}`")
    # every reference file must be routed from SKILL.md
    for ref in ref_files:
        if ref.name not in text:
            errors.append(f"{name}: references/{ref.name} is not mentioned in SKILL.md (unrouted)")
    # every `file.md` §N link must point to a heading "## N." / "## N " / "### N" in that file
    for src in [skill_md] + ref_files:
        for target, num in re.findall(r"`?([a-z0-9-]+\.md)`? ?§ ?(\d+)", read_text(src)):
            target_path = refs_dir / target
            if not target_path.exists():
                continue  # a missing file is reported by the check above
            heading = re.compile(rf"^#{{2,3}} {num}(\.| |$)", re.M)
            if not heading.search(read_text(target_path)):
                errors.append(f"{name}: {src.name} links `{target}` §{num} but that file has no '## {num}.' heading")
    # path mentions like `references/x.md` and markdown links ](references/x.md) must resolve
    for src in [skill_md] + ref_files:
        src_text = read_text(src)
        bases = [skill_dir, src.parent]
        paths = set(re.findall(r"`(references/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+)`", src_text))
        for link in re.findall(r"\]\(([^)\s]+)\)", src_text):
            if re.match(r"^[a-z][a-z0-9+.-]*:", link, re.I) or link.startswith(("#", "/")):
                continue  # web, mailto, anchors, absolute paths
            paths.add(link)
        for p in sorted(paths):
            if any(ch in p for ch in "*<>{}"):
                continue  # placeholders and globs
            if not path_exists(p, bases):
                errors.append(f"{name}: {src.name} points to `{p}` which does not exist")
    lines = text.count("\n")
    if lines > 500:
        errors.append(f"{name}: SKILL.md has {lines} lines (keep under 500)")
    print(f"✓ {name}: description {len(desc)} chars, SKILL.md {lines} lines")

if errors:
    print("\n".join("✗ " + e for e in errors))
    sys.exit(1)
print("All skills valid.")
