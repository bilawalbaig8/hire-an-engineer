import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "install_global_hooks.py"
EVENTS = ("SubagentStart", "SubagentStop", "PostToolUse")


def run(settings, *args):
    return subprocess.run([sys.executable, str(SCRIPT), "--settings", str(settings), *args],
                          capture_output=True, text=True, encoding="utf-8")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def commands(settings, event):
    return [h["command"] for g in load(settings)["hooks"][event] for h in g["hooks"]]


def test_installs_the_three_hooks_with_the_guard_flag(tmp_path):
    s = tmp_path / ".claude" / "settings.json"
    r = run(s)
    assert r.returncode == 0, r.stderr
    for ev in EVENTS:
        cmds = commands(s, ev)
        assert len(cmds) == 1 and "--only-if-enabled" in cmds[0] and "team-start" in cmds[0] and "log_event.py" in cmds[0]
    post = load(s)["hooks"]["PostToolUse"][0]
    assert post["matcher"] == "Write|Edit"


def test_idempotent(tmp_path):
    s = tmp_path / "settings.json"
    run(s)
    before = s.read_bytes()
    r = run(s)
    assert r.returncode == 0 and "already installed" in r.stdout
    assert s.read_bytes() == before


def test_existing_settings_and_hooks_are_kept_and_a_backup_is_made(tmp_path):
    s = tmp_path / "settings.json"
    mine = {"model": "opus", "hooks": {"PostToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo mine"}]}]}}
    s.write_text(json.dumps(mine), encoding="utf-8")
    assert run(s).returncode == 0
    data = load(s)
    assert data["model"] == "opus"
    assert "echo mine" in commands(s, "PostToolUse") and len(commands(s, "PostToolUse")) == 2
    assert load(tmp_path / "settings.json.before-team-start") == mine


def test_dry_run_writes_nothing(tmp_path):
    s = tmp_path / "settings.json"
    r = run(s, "--dry-run")
    assert r.returncode == 0 and "would" in r.stdout.lower()
    assert not s.exists()


def test_remove_takes_out_only_our_hooks(tmp_path):
    s = tmp_path / "settings.json"
    mine = {"hooks": {"PostToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo mine"}]}]}}
    s.write_text(json.dumps(mine), encoding="utf-8")
    run(s)
    assert run(s, "--remove").returncode == 0
    data = load(s)
    assert commands(s, "PostToolUse") == ["echo mine"]
    assert "SubagentStart" not in data.get("hooks", {})


def test_invalid_json_is_refused_and_left_alone(tmp_path):
    s = tmp_path / "settings.json"
    s.write_text("{nope", encoding="utf-8")
    r = run(s)
    assert r.returncode == 2 and s.read_text(encoding="utf-8") == "{nope"


def test_hooks_that_is_not_an_object_is_refused(tmp_path):
    s = tmp_path / "settings.json"
    s.write_text(json.dumps({"hooks": []}), encoding="utf-8")
    assert run(s).returncode == 2
