import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import install_agents as ia  # noqa: E402


@pytest.fixture
def src(tmp_path):
    root = tmp_path / "src"
    (root / "skills" / "demo" / "references").mkdir(parents=True)
    (root / "skills" / "demo" / "SKILL.md").write_text("skill", encoding="utf-8")
    (root / "skills" / "demo" / "references" / "a.md").write_text("ref", encoding="utf-8")
    (root / "skills" / "demo" / "__pycache__").mkdir()
    (root / "skills" / "demo" / "__pycache__" / "x.pyc").write_bytes(b"x")
    (root / "skills" / "demo" / ".hidden").write_text("h", encoding="utf-8")
    (root / "agents").mkdir()
    (root / "agents" / "architect.md").write_text("agent", encoding="utf-8")
    (root / "agents" / "notes.txt").write_text("no", encoding="utf-8")
    return root


@pytest.fixture
def dest(tmp_path):
    return tmp_path / "dest"


def test_new_files_are_copied(src, dest):
    assert ia.install(src, dest) == 3
    assert (dest / "skills" / "demo" / "SKILL.md").read_text(encoding="utf-8") == "skill"
    assert (dest / "skills" / "demo" / "references" / "a.md").exists()
    assert (dest / "agents" / "architect.md").exists()
    assert not (dest / "agents" / "notes.txt").exists()
    assert not (dest / "skills" / "demo" / ".hidden").exists()
    assert not (dest / "skills" / "demo" / "__pycache__").exists()


def test_identical_files_are_skipped(src, dest):
    ia.install(src, dest)
    kinds = {a.kind for a in ia.plan_install(src, dest)}
    assert kinds == {"same"}


def test_modified_destination_raises_without_force(src, dest):
    ia.install(src, dest)
    (dest / "agents" / "architect.md").write_text("changed", encoding="utf-8")
    (dest / "skills" / "demo" / "SKILL.md").write_text("changed", encoding="utf-8")
    (src / "agents" / "second.md").write_text("new", encoding="utf-8")
    with pytest.raises(FileExistsError) as exc:
        ia.install(src, dest)
    msg = str(exc.value)
    assert str(dest / "agents" / "architect.md") in msg
    assert str(dest / "skills" / "demo" / "SKILL.md") in msg
    assert (dest / "agents" / "architect.md").read_text(encoding="utf-8") == "changed"
    assert not (dest / "agents" / "second.md").exists()


def test_force_overwrites(src, dest):
    ia.install(src, dest)
    (dest / "agents" / "architect.md").write_text("changed", encoding="utf-8")
    assert ia.install(src, dest, force=True) == 1
    assert (dest / "agents" / "architect.md").read_text(encoding="utf-8") == "agent"


def test_dry_run_writes_nothing(src, dest, capsys):
    assert ia.install(src, dest, dry_run=True) == 0
    assert not dest.exists()
    assert "new " in capsys.readouterr().out


def test_dry_run_does_not_raise_on_differs(src, dest, capsys):
    ia.install(src, dest)
    (dest / "agents" / "architect.md").write_text("changed", encoding="utf-8")
    assert ia.install(src, dest, dry_run=True) == 0
    out = capsys.readouterr().out
    assert "differs" in out
    assert (dest / "agents" / "architect.md").read_text(encoding="utf-8") == "changed"


def test_second_run_writes_zero(src, dest):
    assert ia.install(src, dest) == 3
    assert ia.install(src, dest) == 0


def test_missing_agents_folder_plans_only_skills(src, dest):
    import shutil
    shutil.rmtree(src / "agents")
    assert ia.install(src, dest) == 2
    assert not (dest / "agents").exists()


def test_summary_and_verbose(src, dest, capsys):
    ia.install(src, dest)
    capsys.readouterr()
    ia.install(src, dest, dry_run=True)
    out = capsys.readouterr().out
    assert "0 new, 3 same, 0 differ" in out
    assert "same " not in out.replace("3 same", "")
    ia.install(src, dest, dry_run=True, verbose=True)
    assert "same " in capsys.readouterr().out


def test_cli_exit_1_on_differs(src, dest, monkeypatch):
    monkeypatch.setattr(ia, "REPO_ROOT", src)
    assert ia.main(["--dest", str(dest)]) == 0
    (dest / "agents" / "architect.md").write_text("changed", encoding="utf-8")
    assert ia.main(["--dest", str(dest)]) == 1
    assert ia.main(["--dest", str(dest), "--force"]) == 0


def test_scripts_subfolder_is_copied(src, dest):
    scripts = src / "skills" / "demo" / "scripts"
    (scripts / "__pycache__").mkdir(parents=True)
    (scripts / "tool.py").write_text("print(1)", encoding="utf-8")
    (scripts / "__pycache__" / "tool.pyc").write_bytes(b"x")
    ia.install(src, dest)
    assert (dest / "skills" / "demo" / "scripts" / "tool.py").read_text(encoding="utf-8") == "print(1)"
    assert not (dest / "skills" / "demo" / "scripts" / "__pycache__").exists()
