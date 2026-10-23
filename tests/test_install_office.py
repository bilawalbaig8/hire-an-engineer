import http.client
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

PRE = {
    "hooks": {"PostToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo mine"}]}]},
    "permissions": {"deny": ["Read(.env)"], "allow": ["Bash(ls)"]},
    "model": "opus",
}


def run(project, *extra):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "install_office.py"), "--project", str(project), *extra],
                          capture_output=True, text=True)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_dry_run_changes_nothing(tmp_path):
    r = run(tmp_path, "--dry-run")
    assert r.returncode == 0 and "new" in r.stdout
    assert list(tmp_path.iterdir()) == []


def test_install_creates_everything(tmp_path):
    r = run(tmp_path)
    assert r.returncode == 0, r.stderr
    off = tmp_path / ".agents" / "office"
    for n in ("office_server.py", "office_launch.py", "office_mcp.py", "log_event.py", "agent_contract.py",
              "check_roster.py", "roster.md", "ui/index.html"):
        assert (off / n).is_file(), n
    s = read(tmp_path / ".claude" / "settings.json")
    assert set(s["hooks"]) == {"SubagentStart", "SubagentStop", "PostToolUse", "SessionStart"}
    assert "Write(/.agents/**)" in s["permissions"]["deny"]
    assert "allow" not in s["permissions"] and "ask" not in s["permissions"]
    assert s["agent"] == "orchestrator"  # plain `claude` in this project starts as the boss
    assert s["hooks"]["SessionStart"][0]["hooks"][0]["async"] is True
    assert "${CLAUDE_PROJECT_DIR}/.agents/office/log_event.py" in s["hooks"]["SubagentStart"][0]["hooks"][0]["command"]
    assert not (tmp_path / ".mcp.json").exists()  # window answers are off: no MCP server by default
    assert "office_launch.py --stop" in r.stdout and "--allowedTools" in r.stdout and "claude --agent orchestrator" in r.stdout


def test_with_mcp_adds_the_office_server(tmp_path):
    r = run(tmp_path, "--with-mcp")
    assert r.returncode == 0, r.stderr
    m = read(tmp_path / ".mcp.json")
    assert m["mcpServers"]["office"]["args"][0].endswith(".agents/office/office_mcp.py")


def test_idempotent(tmp_path):
    run(tmp_path)
    before = (tmp_path / ".claude" / "settings.json").read_bytes()
    r = run(tmp_path)
    assert r.returncode == 0 and "all same" in r.stdout
    assert "0 new, 10 same, 0 differs, 0 merged, 0 conflict" in r.stdout
    assert (tmp_path / ".claude" / "settings.json").read_bytes() == before


def test_merge_keeps_existing(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps(PRE), encoding="utf-8")
    (tmp_path / ".mcp.json").write_text(json.dumps({"mcpServers": {"other": {"command": "x"}}, "keep": 1}), encoding="utf-8")
    r = run(tmp_path, "--with-mcp")
    assert r.returncode == 0 and "merged" in r.stdout
    s = read(tmp_path / ".claude" / "settings.json")
    assert s["model"] == "opus" and s["permissions"]["allow"] == ["Bash(ls)"]
    assert s["permissions"]["deny"][0] == "Read(.env)" and "Edit(/.agents/**)" in s["permissions"]["deny"]
    assert s["hooks"]["PostToolUse"][0]["hooks"][0]["command"] == "echo mine"
    assert len(s["hooks"]["PostToolUse"]) == 2
    m = read(tmp_path / ".mcp.json")
    assert m["keep"] == 1 and "other" in m["mcpServers"] and "office" in m["mcpServers"]
    assert "all same" in run(tmp_path, "--with-mcp").stdout


def test_conflicting_office_entry_is_left(tmp_path):
    mine = {"mcpServers": {"office": {"command": "mine"}}}
    (tmp_path / ".mcp.json").write_text(json.dumps(mine), encoding="utf-8")
    r = run(tmp_path, "--with-mcp")
    assert r.returncode == 0 and "conflict" in r.stdout
    assert read(tmp_path / ".mcp.json") == mine


def test_differing_file_refused_then_forced(tmp_path):
    run(tmp_path)
    f = tmp_path / ".agents" / "office" / "office_server.py"
    f.write_text("# edited", encoding="utf-8")
    r = run(tmp_path)
    assert r.returncode == 1 and "differ" in r.stderr and "office_server.py" in r.stderr
    assert f.read_text(encoding="utf-8") == "# edited"
    assert run(tmp_path, "--force").returncode == 0
    assert f.read_text(encoding="utf-8") != "# edited"


def test_invalid_settings_json_changes_nothing(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text("{nope", encoding="utf-8")
    r = run(tmp_path)
    assert r.returncode == 2 and "not valid JSON" in r.stderr
    assert not (tmp_path / ".agents").exists()


def test_missing_project_folder(tmp_path):
    assert run(tmp_path / "nope").returncode == 2


def test_nothing_outside_project(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    (tmp_path / "sibling.txt").write_text("x", encoding="utf-8")
    run(proj)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["proj", "sibling.txt"]


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _get(port, path):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    c.request("GET", path)
    r = c.getresponse()
    return r.status, r.read()


@pytest.fixture
def installed_server(tmp_path):
    run(tmp_path)
    port = _free_port()
    proc = subprocess.Popen([sys.executable, str(tmp_path / ".agents" / "office" / "office_server.py"),
                             "--project", str(tmp_path), "--port", str(port), "--no-open"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(tmp_path))
    try:
        for _ in range(50):
            try:
                _get(port, "/state")
                break
            except OSError:
                time.sleep(0.1)
        yield tmp_path, port
    finally:
        proc.kill()
        proc.wait()


def test_installed_server_serves_live_ui_and_roster(installed_server):
    proj, port = installed_server
    status, body = _get(port, "/state")
    assert status == 200 and json.loads(body)["events"] == 0
    status, body = _get(port, "/")
    assert status == 200 and body == (ROOT / "docs/agents/visual-office/index.html").read_bytes()
    status, body = _get(port, "/roster")
    assert status == 200 and [r["name"] for r in json.loads(body)] == ["architect", "code-reviewer"]
    assert _get(port, "/office_server.py")[0] == 404  # scripts are not served


def test_installed_roster_prefers_project_roster(installed_server):
    proj, port = installed_server
    (proj / "docs" / "agents").mkdir(parents=True)
    (proj / "docs" / "agents" / "roster.md").write_text(
        "| Name | Skill | Model | Owns |\n|---|---|---|---|\n| dev | s | sonnet | code |\n", encoding="utf-8")
    assert [r["name"] for r in json.loads(_get(port, "/roster")[1])] == ["dev"]


def test_log_event_hook_works_from_installed_copy(tmp_path):
    run(tmp_path)
    payload = json.dumps({"hook_event_name": "SubagentStart", "agent_type": "architect", "session_id": "s", "cwd": str(tmp_path)})
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(tmp_path)}
    r = subprocess.run([sys.executable, str(tmp_path / ".agents" / "office" / "log_event.py")], input=payload,
                       capture_output=True, text=True, env=env, cwd=str(tmp_path))
    assert r.returncode == 0, r.stderr
    assert (tmp_path / ".agents" / "events.jsonl").is_file()


def test_no_default_agent_flag_leaves_the_agent_setting_out(tmp_path):
    r = run(tmp_path, "--no-default-agent")
    assert r.returncode == 0, r.stderr
    assert "agent" not in read(tmp_path / ".claude" / "settings.json")


def test_an_existing_different_agent_setting_is_kept_and_reported(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps({"agent": "my-agent"}), encoding="utf-8")
    r = run(tmp_path)
    assert r.returncode == 0, r.stderr
    assert read(tmp_path / ".claude" / "settings.json")["agent"] == "my-agent"
    assert "my-agent" in r.stdout and "orchestrator" in r.stdout


def test_default_agent_is_idempotent(tmp_path):
    run(tmp_path)
    assert "all same" in run(tmp_path).stdout
