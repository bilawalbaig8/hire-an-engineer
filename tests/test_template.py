import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import validate_agents as va  # noqa: E402

TEMPLATE = Path(__file__).resolve().parent.parent / "docs" / "agents" / "agent-template"


def fill(tmp_path, role="demo-role", skill="demo-skill"):
    agents = tmp_path / "agents"
    skills = tmp_path / "skills" / skill
    agents.mkdir()
    skills.mkdir(parents=True)
    text = (TEMPLATE / "agent.md").read_text(encoding="utf-8")
    filled = text.replace("<role-name>", role).replace("<skill-name>", skill)
    path = agents / f"{role}.md"
    path.write_text(filled, encoding="utf-8")
    return path, tmp_path / "skills"


def test_template_agent_passes_validator_after_fill(tmp_path):
    path, skills = fill(tmp_path)
    assert va.validate_agent_file(path, skills) == []


def test_unfilled_template_is_rejected(tmp_path):
    agents = tmp_path / "agents"
    agents.mkdir()
    (tmp_path / "skills").mkdir()
    path = agents / "agent.md"
    path.write_text((TEMPLATE / "agent.md").read_text(encoding="utf-8"), encoding="utf-8")
    assert va.validate_agent_file(path, tmp_path / "skills")


def test_template_agent_has_all_sections():
    text = (TEMPLATE / "agent.md").read_text(encoding="utf-8")
    for heading in ("## Role", "## When to use", "## Model and why", "## Tools",
                    "## Reads first", "## How it works", "## Handoff", "## Never"):
        assert re.search(rf"^{re.escape(heading)}\s*$", text, re.M), heading


def test_template_skill_folder_has_router_and_example():
    skill = TEMPLATE / "skill"
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\nname: <skill-name>\n")
    assert "references/example.md" in text
    assert (skill / "references" / "example.md").exists()


def test_readme_is_a_ten_step_checklist():
    text = (TEMPLATE / "README.md").read_text(encoding="utf-8")
    steps = re.findall(r"^(\d+)\. ", text, re.M)
    assert steps == [str(i) for i in range(1, 11)]
