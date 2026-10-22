import io
import json
import socket
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import office_launch as ol  # noqa: E402


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    opened = []
    monkeypatch.setattr(ol.webbrowser, "open", lambda url, *a, **k: opened.append(url) or True)
    project = tmp_path / "proj"
    project.mkdir()
    state = {"project": project, "opened": opened, "base": free_port()}
    yield state
    try:
        ol.main(["--stop", "--project", str(project)])
    except SystemExit:
        pass


def run(env, capsys, *args, payload=None, monkeypatch=None):
    argv = ["--project", str(env["project"]), "--port", str(env["base"]), *args]
    rc = ol.main(argv, stdin=io.StringIO(json.dumps(payload) if payload is not None else ""))
    return rc, capsys.readouterr()


def office_json(env):
    return json.loads((env["project"] / ".agents" / "office.json").read_text(encoding="utf-8"))


def test_start_once_and_reuse(env, capsys):
    rc, out = run(env, capsys, payload={"session_id": "s1"})
    assert rc == 0 and out.out == ""
    first = office_json(env)
    assert ol.server_alive(first["port"]) and ol.pid_alive(first["pid"])
    rc, out = run(env, capsys, payload={"session_id": "s1"})
    assert rc == 0 and out.out == ""
    assert office_json(env)["pid"] == first["pid"]


def test_stale_office_json_replaced(env, capsys):
    agents = env["project"] / ".agents"
    agents.mkdir()
    (agents / "office.json").write_text(
        json.dumps({"pid": 999999, "port": free_port(), "started": "x", "opened": []}), encoding="utf-8")
    rc, out = run(env, capsys, "--no-browser")
    assert rc == 0
    info = office_json(env)
    assert info["pid"] != 999999 and ol.server_alive(info["port"])


def test_corrupt_office_json_replaced(env, capsys):
    agents = env["project"] / ".agents"
    agents.mkdir()
    (agents / "office.json").write_text("{not json", encoding="utf-8")
    rc, out = run(env, capsys, "--no-browser")
    assert rc == 0 and ol.server_alive(office_json(env)["port"])


def test_browser_opens_once_per_session(env, capsys):
    run(env, capsys, payload={"session_id": "a"})
    run(env, capsys, payload={"session_id": "a"})
    assert len(env["opened"]) == 1
    assert env["opened"][0].startswith("http://127.0.0.1:")
    run(env, capsys, payload={"session_id": "b"})
    assert len(env["opened"]) == 2
    assert office_json(env)["opened"] == ["a", "b"]


def test_no_browser(env, capsys):
    run(env, capsys, "--no-browser", payload={"session_id": "a"})
    assert env["opened"] == []


def test_project_dir_env_wins_over_cwd(env, capsys, monkeypatch, tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(env["project"]))
    rc = ol.main(["--port", str(env["base"]), "--no-browser"],
                 stdin=io.StringIO(json.dumps({"cwd": str(other), "session_id": "z"})))
    assert rc == 0
    assert (env["project"] / ".agents" / "office.json").is_file()
    assert not (other / ".agents").exists()


def test_cwd_from_payload(env, capsys):
    rc = ol.main(["--port", str(env["base"]), "--no-browser"],
                 stdin=io.StringIO(json.dumps({"cwd": str(env["project"])})))
    assert rc == 0 and (env["project"] / ".agents" / "office.json").is_file()


def test_stop_kills_and_cleans(env, capsys):
    run(env, capsys, "--no-browser")
    info = office_json(env)
    rc, out = run(env, capsys, "--stop")
    assert rc == 0
    assert not (env["project"] / ".agents" / "office.json").exists()
    import time
    for _ in range(50):
        if not ol.server_alive(info["port"]):
            break
        time.sleep(0.1)
    assert not ol.server_alive(info["port"])


def test_stop_when_nothing_running(env, capsys):
    rc, out = run(env, capsys, "--stop")
    assert rc == 0 and out.out.strip()


def test_status(env, capsys):
    rc, out = run(env, capsys, "--status")
    assert rc == 0 and "not running" in out.out
    run(env, capsys, "--no-browser")
    rc, out = run(env, capsys, "--status")
    info = office_json(env)
    assert rc == 0 and "running" in out.out and str(info["port"]) in out.out and "not running" not in out.out


def test_no_stdout_noise_on_start(env, capsys):
    rc, out = run(env, capsys, payload={"session_id": "q"})
    assert rc == 0 and out.out == ""


def test_bad_stdin_and_errors_exit_zero(env, capsys, monkeypatch):
    rc = ol.main(["--project", str(env["project"]), "--no-browser", "--port", str(env["base"])],
                 stdin=io.StringIO("not json at all"))
    assert rc == 0
    capsys.readouterr()
    # server script missing -> error to stderr, still exit 0, nothing on stdout
    monkeypatch.setattr(ol, "SERVER_SCRIPT", env["project"] / "nope.py")
    ol.main(["--stop", "--project", str(env["project"])])
    capsys.readouterr()
    rc = ol.main(["--project", str(env["project"]), "--no-browser", "--port", str(env["base"])],
                 stdin=io.StringIO(""))
    cap = capsys.readouterr()
    assert rc == 0 and cap.out == "" and cap.err.strip()


def test_unwritable_project_exits_zero(env, capsys, tmp_path):
    f = tmp_path / "afile"
    f.write_text("x")
    rc = ol.main(["--project", str(f), "--no-browser"], stdin=io.StringIO(""))
    cap = capsys.readouterr()
    assert rc == 0 and cap.out == ""


def test_find_free_port_skips_taken(env):
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        taken = s.getsockname()[1]
        s.listen(1)
        assert ol.find_free_port(taken) != taken
