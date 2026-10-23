"""scripts/setup_team.py: one command that puts the whole team and the office into a project."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "setup_team.py"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")


def test_sets_up_agents_skills_office_and_the_default_agent(tmp_path):
    r = run("--project", str(tmp_path))
    assert r.returncode == 0, r.stderr
    for name in ("orchestrator", "architect", "code-reviewer"):
        assert (tmp_path / ".claude" / "agents" / f"{name}.md").is_file(), name
    for skill in ("orchestrator", "software-architect", "code-reviewer"):
        assert (tmp_path / ".claude" / "skills" / skill / "SKILL.md").is_file(), skill
    assert (tmp_path / ".agents" / "office" / "office_server.py").is_file()
    s = json.loads((tmp_path / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert s["agent"] == "orchestrator" and "SessionStart" in s["hooks"]
    assert "claude" in r.stdout and "office_launch.py --status" in r.stdout


def test_second_run_changes_nothing(tmp_path):
    run("--project", str(tmp_path))
    before = (tmp_path / ".claude" / "settings.json").read_bytes()
    r = run("--project", str(tmp_path))
    assert r.returncode == 0, r.stderr
    assert "0 new" in r.stdout
    assert (tmp_path / ".claude" / "settings.json").read_bytes() == before


def test_dry_run_writes_nothing(tmp_path):
    r = run("--project", str(tmp_path), "--dry-run")
    assert r.returncode == 0, r.stderr
    assert not (tmp_path / ".claude").exists() and not (tmp_path / ".agents").exists()


def test_missing_project_folder_is_a_clean_error(tmp_path):
    r = run("--project", str(tmp_path / "nope"))
    assert r.returncode == 2 and "nope" in r.stderr


def test_changed_installed_file_is_not_overwritten_without_force(tmp_path):
    run("--project", str(tmp_path))
    f = tmp_path / ".claude" / "agents" / "orchestrator.md"
    f.write_text("my own edit", encoding="utf-8")
    r = run("--project", str(tmp_path))
    assert r.returncode == 1 and "orchestrator.md" in r.stderr
    assert f.read_text(encoding="utf-8") == "my own edit"
    assert run("--project", str(tmp_path), "--force").returncode == 0
    assert f.read_text(encoding="utf-8") != "my own edit"


def test_no_default_agent_is_passed_through(tmp_path):
    assert run("--project", str(tmp_path), "--no-default-agent").returncode == 0
    assert "agent" not in json.loads((tmp_path / ".claude" / "settings.json").read_text(encoding="utf-8"))
