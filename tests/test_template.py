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


def _read(name):
    return (TEMPLATE / name).read_text(encoding="utf-8")


def test_contract_says_who_writes_the_event_log():
    text = _read("handoff-contract.md")
    assert "The hook" in text and "writes `agent_start`, `agent_stop`" in text
    assert "The boss writes `handoff`, `approval_requested` and `approval_given`" in text
    assert "A specialist writes nothing" in text
    assert "must be present" in text and "should be present" not in text


def test_readme_follows_definition_of_done():
    text = _read("README.md")
    steps = dict(re.findall(r"^(\d+)\. (.*)$", text, re.M))
    assert "evals" in steps["4"].lower() and "BEFORE" in steps["4"]
    assert "knowledge" in steps["5"].lower()
    assert "check_evals.py" in steps["7"]
    assert "diff -rq" in steps["9"] and "stale" in steps["9"]
    assert "hooks-snippet.json" in text and "scripts/log_event.py" in text


def test_agent_template_never_list_and_inline_handoff():
    text = _read("agent.md")
    assert "Overwrite, renumber or reformat existing project records" in text
    handoff = text.split("## Handoff")[1].split("## Never")[0]
    for field in ("status", "summary", "files", "questions", "approvals", "assumptions", "evidence", "one_way_door"):
        assert f'"{field}"' in handoff, field
    assert "handoff-contract.md" in handoff
    assert "not evidence" in handoff


def test_agent_template_tools_and_skills_keys():
    text = _read("agent.md")
    assert re.search(r"^tools: Read, Grep", text, re.M)
    assert re.search(r"^skills:\n  - <skill-name>\nskill: <skill-name>$", text, re.M)


def test_skill_template_has_no_issue_link_and_uses_claim_labels():
    text = _read("skill/SKILL.md")
    assert "issue link" not in text
    assert "verified in code" in text
    assert "verified in code" in _read("agent.md")


def test_install_doc_and_workflows():
    root = TEMPLATE.parent.parent.parent
    install = (root / "docs" / "INSTALL.md").read_text(encoding="utf-8")
    assert "--verbose` to list `same`" in install and "never removes stale files" in install
    validate = (root / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
    assert "skills/*/" in validate and "software-architect" not in validate
    release = (root / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    assert "validate_agents.py" in release and "pytest -q" in release
