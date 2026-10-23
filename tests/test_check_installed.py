import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import backup_evals  # noqa: E402
import check_installed  # noqa: E402


def _repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "skills" / "demo" / "references").mkdir(parents=True)
    (repo / "skills" / "hire-an-engineer").mkdir(parents=True)
    (repo / "agents").mkdir()
    (repo / "skills" / "demo" / "SKILL.md").write_text("a\nb\n", encoding="utf-8")
    (repo / "skills" / "demo" / "references" / "x.md").write_text("x\n", encoding="utf-8")
    (repo / "skills" / "hire-an-engineer" / "SKILL.md").write_text("own\n", encoding="utf-8")
    (repo / "agents" / "demo.md").write_text("agent\n", encoding="utf-8")
    return repo


def test_reports_missing_then_same_ignoring_line_endings(tmp_path):
    repo, dest = _repo(tmp_path), tmp_path / "home"
    assert len(check_installed.compare(repo, dest)) == 3
    (dest / "skills" / "demo" / "references").mkdir(parents=True)
    (dest / "agents").mkdir()
    (dest / "skills" / "demo" / "SKILL.md").write_bytes(b"a\r\nb\r\n")
    (dest / "skills" / "demo" / "references" / "x.md").write_bytes(b"x\n")
    (dest / "agents" / "demo.md").write_bytes(b"agent\n")
    assert check_installed.compare(repo, dest) == []


def test_reports_difference_and_skips_own_skill(tmp_path):
    repo, dest = _repo(tmp_path), tmp_path / "home"
    (dest / "skills" / "demo" / "references").mkdir(parents=True)
    (dest / "agents").mkdir()
    (dest / "skills" / "demo" / "SKILL.md").write_text("changed\n", encoding="utf-8")
    (dest / "skills" / "demo" / "references" / "x.md").write_text("x\n", encoding="utf-8")
    (dest / "agents" / "demo.md").write_text("agent\n", encoding="utf-8")
    problems = check_installed.compare(repo, dest)
    assert len(problems) == 1 and problems[0].startswith("differs") and "hire-an-engineer" not in problems[0]


def test_backup_evals_zips_and_keeps_newest(tmp_path):
    repo = tmp_path / "repo"
    (repo / "evals" / "demo").mkdir(parents=True)
    (repo / "evals" / "demo" / "evals.json").write_text("[]", encoding="utf-8")
    dest = tmp_path / "bk"
    dest.mkdir()
    for n in ("2020-01-01_000001", "2020-01-01_000002"):
        (dest / f"evals-{n}.zip").write_bytes(b"old")
    target = backup_evals.backup(repo, dest, keep=2)
    assert target is not None and target.exists()
    names = sorted(p.name for p in dest.glob("evals-*.zip"))
    assert len(names) == 2 and target.name in names
    assert backup_evals.backup(tmp_path / "nothing", dest) is None
