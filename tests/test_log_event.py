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
