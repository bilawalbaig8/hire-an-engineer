import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import install_agents as ia  # noqa: E402


def agent_text(skill=None):
    front = "---\nname: x\ndescription: d\n"
    if skill:
        front += f"skill: {skill}\n"
    return front + "---\n# body\n"


@pytest.fixture
def src(tmp_path):
    root = tmp_path / "src"
    for name in ("alpha", "beta", "gamma"):
        (root / "skills" / name / "references").mkdir(parents=True)
        (root / "skills" / name / "SKILL.md").write_text(f"{name} skill", encoding="utf-8")
        (root / "skills" / name / "references" / "r.md").write_text(f"{name} ref", encoding="utf-8")
    (root / "agents").mkdir()
    (root / "agents" / "alpha-agent.md").write_text(agent_text("alpha"), encoding="utf-8")
    (root / "agents" / "beta-agent.md").write_text(agent_text("beta"), encoding="utf-8")
    (root / "agents" / "loose.md").write_text(agent_text(), encoding="utf-8")
    return root


@pytest.fixture
def dest(tmp_path):
    return tmp_path / "dest"


def test_only_plans_just_that_skill_and_its_agent(src, dest):
    plan = ia.plan_install(src, dest, only=["alpha"])
    assert {a.dst for a in plan} == {
        dest / "skills" / "alpha" / "SKILL.md",
        dest / "skills" / "alpha" / "references" / "r.md",
        dest / "agents" / "alpha-agent.md",
    }


def test_only_install_writes_nothing_else(src, dest):
    assert ia.install(src, dest, only=["alpha"]) == 3
    assert not (dest / "skills" / "beta").exists()
    assert not (dest / "agents" / "beta-agent.md").exists()
    assert not (dest / "agents" / "loose.md").exists()


def test_only_ignores_differing_files_of_other_skills(src, dest):
    ia.install(src, dest)
    (dest / "skills" / "beta" / "SKILL.md").write_text("owner changed this", encoding="utf-8")
    (src / "skills" / "alpha" / "SKILL.md").write_text("alpha v2", encoding="utf-8")
    (dest / "skills" / "alpha" / "SKILL.md").unlink()
    ia.install(src, dest, only=["alpha"])
    assert (dest / "skills" / "beta" / "SKILL.md").read_text(encoding="utf-8") == "owner changed this"
    assert (dest / "skills" / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "alpha v2"


def test_only_still_refuses_to_overwrite_its_own_differing_files(src, dest):
    ia.install(src, dest, only=["alpha"])
    (dest / "skills" / "alpha" / "SKILL.md").write_text("owner changed this", encoding="utf-8")
    with pytest.raises(FileExistsError):
        ia.install(src, dest, only=["alpha"])
    assert (dest / "skills" / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "owner changed this"


def test_only_accepts_several_names(src, dest):
    ia.install(src, dest, only=["alpha", "beta"])
    assert (dest / "skills" / "alpha" / "SKILL.md").exists()
    assert (dest / "skills" / "beta" / "SKILL.md").exists()
    assert not (dest / "skills" / "gamma").exists()
    assert (dest / "agents" / "beta-agent.md").exists()


def test_only_unknown_name_is_an_error_listing_the_skills(src, dest):
    with pytest.raises(ValueError) as exc:
        ia.plan_install(src, dest, only=["nope"])
    msg = str(exc.value)
    assert "nope" in msg and "alpha" in msg and "beta" in msg and "gamma" in msg
    assert not dest.exists()


def test_agent_without_skill_key_is_never_installed_with_only(src, dest):
    plan = ia.plan_install(src, dest, only=["alpha", "beta", "gamma"])
    assert dest / "agents" / "loose.md" not in {a.dst for a in plan}


def test_without_only_everything_is_planned(src, dest):
    plan = ia.plan_install(src, dest)
    assert dest / "agents" / "loose.md" in {a.dst for a in plan}
    assert dest / "skills" / "gamma" / "SKILL.md" in {a.dst for a in plan}


def test_cli_only_flag(src, dest, monkeypatch, capsys):
    monkeypatch.setattr(ia, "REPO_ROOT", src)
    assert ia.main(["--dest", str(dest), "--only", "alpha"]) == 0
    assert (dest / "skills" / "alpha" / "SKILL.md").exists()
    assert not (dest / "skills" / "beta").exists()


def test_cli_only_unknown_name_exits_2_and_writes_nothing(src, dest, monkeypatch, capsys):
    monkeypatch.setattr(ia, "REPO_ROOT", src)
    assert ia.main(["--dest", str(dest), "--only", "nope"]) == 2
    assert "nope" in capsys.readouterr().err
    assert not dest.exists()


def test_cli_only_flag_can_repeat(src, dest, monkeypatch):
    monkeypatch.setattr(ia, "REPO_ROOT", src)
    assert ia.main(["--dest", str(dest), "--only", "alpha", "--only", "gamma"]) == 0
    assert (dest / "skills" / "gamma" / "SKILL.md").exists()
    assert not (dest / "skills" / "beta").exists()
