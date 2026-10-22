import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_roster as cr  # noqa: E402

HEADER = "| Name | Skill | Model | Owns |\n|---|---|---|---|\n"


def agent(root, name, skill, model="opus"):
    (root / "agents").mkdir(exist_ok=True)
    (root / "agents" / f"{name}.md").write_text(
        f"---\nname: {name}\ndescription: d\nmodel: {model}\nskill: {skill}\n---\n# {name}\n",
        encoding="utf-8",
    )


def roster(root, rows):
    path = root / "roster.md"
    path.write_text("# Roster\n\n" + HEADER + "".join(rows), encoding="utf-8")
    return path


@pytest.fixture
def repo(tmp_path):
    agent(tmp_path, "architect", "software-architect")
    agent(tmp_path, "code-reviewer", "code-reviewer")
    return tmp_path


GOOD = [
    "| architect | software-architect | opus | architecture, ADRs |\n",
    "| code-reviewer | code-reviewer | opus | review reports |\n",
]


def test_matching_roster_has_no_errors(repo):
    assert cr.check_roster(roster(repo, GOOD), repo / "agents") == []


def test_roster_row_without_agent_file_is_an_error(repo):
    rows = GOOD + ["| ghost | ghost-skill | opus | nothing |\n"]
    errors = cr.check_roster(roster(repo, rows), repo / "agents")
    assert any("ghost" in e and "no agent file" in e for e in errors)


def test_agent_file_missing_from_roster_is_an_error(repo):
    errors = cr.check_roster(roster(repo, GOOD[:1]), repo / "agents")
    assert any("code-reviewer" in e and "not in the roster" in e for e in errors)


def test_model_mismatch_is_an_error(repo):
    rows = ["| architect | software-architect | sonnet | x |\n", GOOD[1]]
    errors = cr.check_roster(roster(repo, rows), repo / "agents")
    assert any("architect" in e and "model" in e for e in errors)


def test_skill_mismatch_is_an_error(repo):
    rows = ["| architect | other-skill | opus | x |\n", GOOD[1]]
    errors = cr.check_roster(roster(repo, rows), repo / "agents")
    assert any("architect" in e and "skill" in e for e in errors)


def test_duplicate_row_is_an_error(repo):
    errors = cr.check_roster(roster(repo, GOOD + GOOD[:1]), repo / "agents")
    assert any("duplicate" in e and "architect" in e for e in errors)


def test_the_boss_agent_is_not_required_in_the_roster(repo):
    agent(repo, "orchestrator", "orchestrator")
    assert cr.check_roster(roster(repo, GOOD), repo / "agents") == []


def test_empty_owns_cell_is_an_error(repo):
    rows = ["| architect | software-architect | opus |  |\n", GOOD[1]]
    errors = cr.check_roster(roster(repo, rows), repo / "agents")
    assert any("architect" in e and "owns" in e for e in errors)


def test_roster_without_table_is_an_error(repo):
    path = repo / "roster.md"
    path.write_text("# Roster\n\nnothing here\n", encoding="utf-8")
    errors = cr.check_roster(path, repo / "agents")
    assert errors and "table" in errors[0]


def test_missing_roster_file_is_an_error(repo):
    errors = cr.check_roster(repo / "nope.md", repo / "agents")
    assert errors and "cannot read" in errors[0]


def test_cli_exit_codes(repo, capsys):
    ok = roster(repo, GOOD)
    assert cr.main([str(ok), "--agents", str(repo / "agents")]) == 0
    bad = roster(repo, GOOD[:1])
    assert cr.main([str(bad), "--agents", str(repo / "agents")]) == 1
    assert "code-reviewer" in capsys.readouterr().err
