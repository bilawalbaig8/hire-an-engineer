import subprocess
import sys
import zipfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import package_skill as ps  # noqa: E402


def agent_text(name: str, skill: str) -> str:
    return f"---\nname: {name}\ndescription: test\nmodel: sonnet\ntools: [Read]\nskill: {skill}\n---\n\n## Handoff\nhandoff-contract.md\n"


def make_repo(tmp_path: Path) -> Path:
    skill = tmp_path / "skills" / "alpha"
    (skill / "refs").mkdir(parents=True)
    (skill / "SKILL.md").write_text("# alpha\n", encoding="utf-8")
    (skill / "refs" / "a.md").write_text("a\n", encoding="utf-8")
    (skill / ".hidden").write_text("x\n", encoding="utf-8")
    return skill


def add_agents(tmp_path: Path) -> None:
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "builder.md").write_text(agent_text("builder", "alpha"), encoding="utf-8")
    (agents / "other.md").write_text(agent_text("other", "beta"), encoding="utf-8")


def run_packager(skill: Path, out: Path) -> None:
    subprocess.run(
        [sys.executable, str(SCRIPTS / "package_skill.py"), str(skill), str(out)],
        check=True, capture_output=True, text=True,
    )


def names(archive: Path) -> list:
    with zipfile.ZipFile(archive) as z:
        return sorted(z.namelist())


def test_agent_files_for_skill_matches_frontmatter(tmp_path):
    add_agents(tmp_path)
    (tmp_path / "agents" / "broken.md").write_text("no frontmatter\n", encoding="utf-8")
    found = ps.agent_files_for_skill("alpha", tmp_path / "agents")
    assert [p.name for p in found] == ["builder.md"]
    assert ps.agent_files_for_skill("beta", tmp_path / "agents")[0].name == "other.md"
    assert ps.agent_files_for_skill("alpha", tmp_path / "missing") == []


def test_package_contains_agent_file(tmp_path):
    skill = make_repo(tmp_path)
    add_agents(tmp_path)
    out = tmp_path / "dist"
    run_packager(skill, out)
    for ext in (".skill", ".zip"):
        listing = names(out / f"alpha{ext}")
        assert "agents/builder.md" in listing
        assert "agents/other.md" not in listing
        assert "alpha/SKILL.md" in listing


def test_package_without_agent_unchanged(tmp_path):
    skill = make_repo(tmp_path)
    out = tmp_path / "dist"
    run_packager(skill, out)
    expected = ["alpha/SKILL.md", "alpha/refs/a.md"]
    for ext in (".skill", ".zip"):
        assert names(out / f"alpha{ext}") == expected
    # agents folder present but none for this skill: still unchanged
    add_agents(tmp_path)
    (tmp_path / "agents" / "builder.md").unlink()
    run_packager(skill, out)
    assert names(out / "alpha.zip") == expected
