import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import validate_agents as va  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "agents"
SKILLS = FIX / "good" / "skills"


def check(path):
    return va.validate_agent_file(path, SKILLS)


def test_good_agent_passes():
    assert check(FIX / "good" / "agents" / "demo.md") == []


def test_name_must_match_filename():
    errs = check(FIX / "bad" / "agents" / "wrong-name.md")
    assert any("name" in e and "wrong-name" in e for e in errs)


def test_description_too_long():
    errs = check(FIX / "bad" / "agents" / "long-desc.md")
    assert any("1024" in e for e in errs)


def test_bad_model():
    errs = check(FIX / "bad" / "agents" / "bad-model.md")
    assert any("model" in e for e in errs)


def test_missing_skill_folder():
    errs = check(FIX / "bad" / "agents" / "no-skill.md")
    assert any("missing-skill" in e for e in errs)


def test_missing_handoff_section():
    errs = check(FIX / "bad" / "agents" / "no-handoff.md")
    assert any("Handoff" in e for e in errs)


def test_missing_frontmatter():
    errs = check(FIX / "bad" / "agents" / "no-frontmatter.md")
    assert any("frontmatter" in e for e in errs)


def test_tools_missing_is_rejected(tmp_path):
    p = tmp_path / "t.md"
    p.write_text(
        "---\nname: t\ndescription: d\nmodel: opus\nskill: demo\n---\n"
        "## Handoff\n\nhandoff-contract.md\n",
        encoding="utf-8",
    )
    assert any("tools" in e for e in va.validate_agent_file(p, SKILLS))


def _agent_with_tools(tmp_path, tools_line):
    p = tmp_path / "t.md"
    p.write_text(
        f"---\nname: t\ndescription: d\nmodel: opus\n{tools_line}\nskill: demo\n---\n"
        "## Handoff\n\nhandoff-contract.md\n",
        encoding="utf-8",
    )
    return p


def test_tools_comma_string_is_accepted(tmp_path):
    p = _agent_with_tools(tmp_path, "tools: Read, Grep, Bash(git status)")
    assert va.validate_agent_file(p, SKILLS) == []


def test_tools_yaml_list_is_accepted(tmp_path):
    p = _agent_with_tools(tmp_path, "tools:\n  - Read\n  - Grep")
    assert va.validate_agent_file(p, SKILLS) == []


def test_tools_string_with_empty_item_is_rejected(tmp_path):
    p = _agent_with_tools(tmp_path, "tools: Read, , Grep")
    assert any("tools" in e for e in va.validate_agent_file(p, SKILLS))


def test_tools_empty_string_or_list_is_rejected(tmp_path):
    for line in ('tools: ""', "tools: []", "tools: 5", 'tools: [Read, ""]'):
        p = _agent_with_tools(tmp_path, line)
        assert any("tools" in e for e in va.validate_agent_file(p, SKILLS)), line


def test_cli_works_without_utf8_env():
    import os
    import subprocess
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONUTF8", "PYTHONIOENCODING")}
    r = subprocess.run([sys.executable, str(Path(va.__file__)), str(FIX / "good")], capture_output=True, env=env)
    assert r.returncode == 0, r.stderr
    assert b"demo" in r.stdout
