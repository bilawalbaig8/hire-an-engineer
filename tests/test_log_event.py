import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import agent_contract as ac  # noqa: E402
import log_event as le  # noqa: E402

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "log_event.py"


def base(event, **over):
    p = {"session_id": "abc123", "transcript_path": "/t.jsonl",
         "cwd": "/proj", "hook_event_name": event}
    p.update(over)
    return p


def test_subagent_start_maps_to_agent_start():
    e = le.event_from_hook(base("SubagentStart", agent_id="agent-1", agent_type="architect"))
    assert e["type"] == "agent_start" and e["agent"] == "architect" and e["run_id"] == "abc123"
    assert ac.validate_event(e) == []


def test_subagent_stop_maps_to_agent_stop():
    e = le.event_from_hook(base("SubagentStop", agent_id="a", agent_type="architect",
                                last_assistant_message="done", stop_hook_active=False))
    assert e["type"] == "agent_stop" and e["agent"] == "architect"
    assert ac.validate_event(e) == []


def test_write_tool_maps_to_file_written_with_relative_path(monkeypatch):
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    proj = Path.cwd().resolve()
    for tool in ("Write", "Edit"):
        p = base("PostToolUse", cwd=str(proj), tool_name=tool,
                 tool_input={"file_path": str(proj / "docs" / "plan.md")},
                 tool_response={"filePath": "x"})
        e = le.event_from_hook(p)
        assert e["type"] == "file_written" and e["path"] == "docs/plan.md"
        assert e["agent"] == "main"
        assert ac.validate_event(e) == []


def test_other_events_return_none():
    assert le.event_from_hook(base("PostToolUse", tool_name="Bash", tool_input={"command": "ls"})) is None
    assert le.event_from_hook(base("PreToolUse", tool_name="Write")) is None
    assert le.event_from_hook(base("PostToolUse", tool_name="Write", tool_input={})) is None
    assert le.event_from_hook({}) is None


def clean_env():
    env = dict(os.environ)
    env.pop("CLAUDE_PROJECT_DIR", None)
    return env


def run_cli(script, data, cwd, raw=False):
    return subprocess.run([sys.executable, str(script)],
                          input=data if raw else data.encode("utf-8"),
                          capture_output=True, cwd=cwd, env=clean_env())


def test_cli_never_raises_on_garbage_stdin(tmp_path):
    for data in ("not json", "[1,2]", "", '{"hook_event_name": "SubagentStart"}'):
        r = run_cli(SCRIPT, data, tmp_path)
        assert r.returncode == 0
    assert not (tmp_path / ".agents" / "events.jsonl").exists()


def test_cli_appends_one_valid_line(tmp_path):
    payload = base("SubagentStart", cwd=str(tmp_path), agent_id="a", agent_type="architect")
    r = run_cli(SCRIPT, json.dumps(payload), tmp_path)
    assert r.returncode == 0
    lines = (tmp_path / ".agents" / "events.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1 and ac.validate_event(json.loads(lines[0])) == []


def test_cli_exits_0_when_contract_module_is_missing(tmp_path):
    alone = tmp_path / "alone"
    alone.mkdir()
    shutil.copy(SCRIPT, alone / "log_event.py")
    r = run_cli(alone / "log_event.py", "{}", alone)
    assert r.returncode == 0
    assert b"log_event:" in r.stderr


def _symlink_or_skip(link, target):
    try:
        link.symlink_to(target, target_is_directory=target.is_dir())
    except (OSError, NotImplementedError):
        pytest.skip("cannot create symlinks here")


def test_cli_refuses_symlinked_agents_folder(tmp_path):
    proj, outside = tmp_path / "proj", tmp_path / "outside"
    proj.mkdir()
    outside.mkdir()
    _symlink_or_skip(proj / ".agents", outside)
    payload = base("SubagentStart", cwd=str(proj), agent_id="a", agent_type="architect")
    r = run_cli(SCRIPT, json.dumps(payload), proj)
    assert r.returncode == 0 and b"symlink" in r.stderr
    assert list(outside.iterdir()) == []


def test_cli_refuses_symlinked_events_file(tmp_path):
    proj, outside = tmp_path / "proj", tmp_path / "outside"
    (proj / ".agents").mkdir(parents=True)
    outside.mkdir()
    target = outside / "target.jsonl"
    target.write_text("", encoding="utf-8")
    _symlink_or_skip(proj / ".agents" / "events.jsonl", target)
    payload = base("SubagentStart", cwd=str(proj), agent_id="a", agent_type="architect")
    r = run_cli(SCRIPT, json.dumps(payload), proj)
    assert r.returncode == 0 and b"symlink" in r.stderr
    assert target.read_text(encoding="utf-8") == ""


def test_cli_reads_stdin_as_utf8(tmp_path):
    proj = tmp_path / "projé"
    proj.mkdir()
    payload = base("PostToolUse", cwd=str(proj), tool_name="Write",
                   tool_input={"file_path": str(proj / "docs" / "café.md")})
    r = run_cli(SCRIPT, json.dumps(payload, ensure_ascii=False), proj)
    assert r.returncode == 0
    line = (proj / ".agents" / "events.jsonl").read_text(encoding="utf-8").splitlines()[0]
    assert json.loads(line)["path"] == "docs/café.md"


# ---------- current_run: the boss's run id replaces the session id ----------

def _hook_payload(proj):
    return base("SubagentStart", cwd=str(proj), agent_type="architect")


def _set_current_run(proj, text, age_hours=0):
    f = proj / ".agents" / "current_run"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(text.encode("utf-8") if isinstance(text, str) else text)
    if age_hours:
        import time
        t = time.time() - age_hours * 3600
        os.utime(f, (t, t))


def test_current_run_switches_run_id_and_adds_session_id(tmp_path, monkeypatch):
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    _set_current_run(tmp_path, "2026-10-23-shop-recover\n")
    e = le.event_from_hook(_hook_payload(tmp_path))
    assert e["run_id"] == "2026-10-23-shop-recover" and e["session_id"] == "abc123"
    assert ac.validate_event(e) == []


def test_current_run_applies_to_file_written(tmp_path, monkeypatch):
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    _set_current_run(tmp_path, "run-7")
    p = base("PostToolUse", cwd=str(tmp_path), tool_name="Write",
             tool_input={"file_path": str(tmp_path / "a.md")})
    e = le.event_from_hook(p)
    assert e["run_id"] == "run-7" and e["session_id"] == "abc123" and e["path"] == "a.md"


def test_no_current_run_behaves_as_before(tmp_path, monkeypatch):
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    e = le.event_from_hook(_hook_payload(tmp_path))
    assert e["run_id"] == "abc123" and "session_id" not in e


def test_current_run_uses_claude_project_dir(tmp_path, monkeypatch):
    other = tmp_path / "other"
    other.mkdir()
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    _set_current_run(tmp_path, "run-env")
    e = le.event_from_hook(_hook_payload(other))
    assert e["run_id"] == "run-env"


def test_stale_current_run_ignored(tmp_path, monkeypatch):
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    _set_current_run(tmp_path, "old-run", age_hours=13)
    e = le.event_from_hook(_hook_payload(tmp_path))
    assert e["run_id"] == "abc123" and "session_id" not in e
    _set_current_run(tmp_path, "fresh-run", age_hours=11)
    assert le.event_from_hook(_hook_payload(tmp_path))["run_id"] == "fresh-run"


@pytest.mark.parametrize("content", ["", "   \n", b"\xff\xfe\x00bad", "a\x00b", "x" * 500])
def test_garbled_current_run_ignored(tmp_path, monkeypatch, content):
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    _set_current_run(tmp_path, content)
    e = le.event_from_hook(_hook_payload(tmp_path))
    assert e["run_id"] == "abc123" and "session_id" not in e


def test_current_run_is_a_directory_no_crash(tmp_path, monkeypatch):
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    (tmp_path / ".agents" / "current_run").mkdir(parents=True)
    assert le.event_from_hook(_hook_payload(tmp_path))["run_id"] == "abc123"


def test_cli_writes_boss_run_id_with_session_id(tmp_path):
    _set_current_run(tmp_path, "2026-10-23-shop-recover")
    data = json.dumps(_hook_payload(tmp_path))
    assert run_cli(SCRIPT, data, tmp_path).returncode == 0
    line = json.loads((tmp_path / ".agents" / "events.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert line["run_id"] == "2026-10-23-shop-recover" and line["session_id"] == "abc123"


def test_contract_session_id_optional_and_validated():
    ev = {"ts": "2026-10-23T10:00:00Z", "type": "agent_start", "agent": "a", "run_id": "r"}
    assert ac.validate_event(ev) == []
    assert ac.validate_event({**ev, "session_id": "s1"}) == []
    assert any("session_id" in e for e in ac.validate_event({**ev, "session_id": ""}))
    assert any("session_id" in e for e in ac.validate_event({**ev, "session_id": 5}))
