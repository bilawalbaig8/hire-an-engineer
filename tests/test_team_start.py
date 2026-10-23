"""The global team-start skill: runtime copy stays in sync with the sources, enable_team turns the team on for a folder."""
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "team-start"
ENABLE = SKILL / "scripts" / "enable_team.py"
RUNTIME = SKILL / "runtime"
SYNC = ROOT / "scripts" / "sync_team_start.py"

PAIRS = [
    ("scripts/office_server.py", "office_server.py"),
    ("scripts/office_launch.py", "office_launch.py"),
    ("scripts/log_event.py", "log_event.py"),
    ("scripts/agent_contract.py", "agent_contract.py"),
    ("scripts/check_roster.py", "check_roster.py"),
    ("docs/agents/roster.md", "roster.md"),
    ("docs/agents/visual-office/index.html", "ui/index.html"),
    ("docs/agents/visual-office/mock-v2.html", "ui/mock-v2.html"),
]


def env():
    e = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
    e["PYTHONIOENCODING"] = "utf-8"
    return e


def run(script, *args):
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, encoding="utf-8", env=env())


def read_bytes(p):
    return p.read_bytes().replace(b"\r\n", b"\n")


@pytest.mark.parametrize("src,dst", PAIRS)
def test_runtime_copy_matches_the_source(src, dst):
    assert read_bytes(RUNTIME / dst) == read_bytes(ROOT / src), f"{dst} is out of date: run python scripts/sync_team_start.py"


def test_sync_check_passes_when_in_sync():
    r = run(SYNC, "--check")
    assert r.returncode == 0, r.stdout + r.stderr


def stop(project):
    run(RUNTIME / "office_launch.py", "--project", str(project), "--stop")


def test_enable_turns_the_team_on_and_starts_the_office(tmp_path):
    try:
        r = run(ENABLE, "--project", str(tmp_path), "--no-browser")
        assert r.returncode == 0, r.stderr
        assert (tmp_path / ".agents" / "enabled").is_file()
        info = json.loads((tmp_path / ".agents" / "office.json").read_text(encoding="utf-8"))
        url = f"http://127.0.0.1:{info['port']}/"
        assert url in r.stdout
        assert b"events" in urllib.request.urlopen(url + "state", timeout=10).read()
        again = run(ENABLE, "--project", str(tmp_path), "--no-browser")
        assert again.returncode == 0 and url in again.stdout
    finally:
        stop(tmp_path)


def test_solo_writes_a_marker_and_starts_nothing(tmp_path):
    r = run(ENABLE, "--project", str(tmp_path), "--solo")
    assert r.returncode == 0, r.stderr
    assert (tmp_path / ".agents" / "solo").is_file()
    assert not (tmp_path / ".agents" / "enabled").exists() and not (tmp_path / ".agents" / "office.json").exists()


def test_enable_after_solo_switches_to_team(tmp_path):
    try:
        run(ENABLE, "--project", str(tmp_path), "--solo")
        assert run(ENABLE, "--project", str(tmp_path), "--no-browser").returncode == 0
        assert (tmp_path / ".agents" / "enabled").is_file() and not (tmp_path / ".agents" / "solo").exists()
    finally:
        stop(tmp_path)


def test_missing_folder_is_a_clean_error(tmp_path):
    r = run(ENABLE, "--project", str(tmp_path / "nope"))
    assert r.returncode == 2 and "nope" in r.stderr


def test_skill_md_is_short_and_has_a_description():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---") and "name: team-start" in text and "description:" in text
    assert len(text.splitlines()) <= 70
