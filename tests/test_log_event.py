import json
import subprocess
import sys
from pathlib import Path

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


def test_write_tool_maps_to_file_written_with_relative_path():
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


def test_cli_never_raises_on_garbage_stdin(tmp_path):
    for data in ("not json", "[1,2]", "", '{"hook_event_name": "SubagentStart"}'):
        r = subprocess.run([sys.executable, str(SCRIPT)], input=data, text=True,
                           capture_output=True, cwd=tmp_path)
        assert r.returncode == 0
    assert not (tmp_path / ".agents" / "events.jsonl").exists()


def test_cli_appends_one_valid_line(tmp_path):
    payload = base("SubagentStart", cwd=str(tmp_path), agent_id="a", agent_type="architect")
    r = subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(payload), text=True,
                       capture_output=True, cwd=tmp_path)
    assert r.returncode == 0
    lines = (tmp_path / ".agents" / "events.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1 and ac.validate_event(json.loads(lines[0])) == []
