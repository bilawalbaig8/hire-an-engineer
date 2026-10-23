"""Drive scripts/office_mcp.py as a real subprocess over stdio with JSON-RPC 2.0 lines."""
import json
import os
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "office_mcp.py"
sys.path.insert(0, str(SCRIPT.parent))

import office_mcp  # noqa: E402

WAIT = "wait_for_owner_answer"
PENDING = "pending_window_answers"


class Server:
    """One office_mcp.py process; every stdout line must be a JSON-RPC message."""

    def __init__(self, project: Path | None, env_project: Path | None = None, extra_args=()):
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
        env["OFFICE_MCP_POLL_SECONDS"] = "0.05"
        env["PYTHONIOENCODING"] = "utf-8"
        if env_project is not None:
            env["CLAUDE_PROJECT_DIR"] = str(env_project)
        args = [sys.executable, str(SCRIPT), *extra_args]
        if project is not None:
            args += ["--project", str(project)]
        self.proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, env=env)
        self.msgs: queue.Queue = queue.Queue()
        self.bad_stdout: list = []
        self.next_id = 0
        threading.Thread(target=self._read, daemon=True).start()
        threading.Thread(target=self._drain_err, daemon=True).start()

    def _read(self):
        for raw in self.proc.stdout:
            line = raw.decode("utf-8")
            if not line.endswith("\n") or line.endswith("\r\n"):
                self.bad_stdout.append(line)
            try:
                msg = json.loads(line)
            except ValueError:
                self.bad_stdout.append(line)
                continue
            if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
                self.bad_stdout.append(line)
            self.msgs.put(msg)

    def _drain_err(self):
        for _ in self.proc.stderr:
            pass

    def send_raw(self, text: str):
        self.proc.stdin.write(text.encode("utf-8") + b"\n")
        self.proc.stdin.flush()

    def send(self, method, params=None, msg_id=None, notify=False):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        if not notify:
            if msg_id is None:
                self.next_id += 1
                msg_id = self.next_id
            msg["id"] = msg_id
        self.send_raw(json.dumps(msg))
        return msg_id

    def recv(self, timeout=10.0):
        return self.msgs.get(timeout=timeout)

    def request(self, method, params=None, timeout=10.0):
        msg_id = self.send(method, params)
        msg = self.recv(timeout)
        assert msg.get("id") == msg_id, msg
        return msg

    def initialize(self, version="2025-06-18"):
        r = self.request("initialize", {"protocolVersion": version, "capabilities": {},
                                        "clientInfo": {"name": "pytest", "version": "0"}})
        self.send("notifications/initialized", notify=True)
        return r

    def call(self, name, arguments=None, timeout=10.0):
        params = {"name": name}
        if arguments is not None:
            params["arguments"] = arguments
        return self.request("tools/call", params, timeout=timeout)

    def close(self):
        try:
            self.proc.stdin.close()
        except OSError:
            pass
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()
        assert not self.bad_stdout, f"non-protocol output on stdout: {self.bad_stdout!r}"


@pytest.fixture
def project(tmp_path):
    p = tmp_path / "project"
    p.mkdir()
    return p


@pytest.fixture
def server(project):
    s = Server(project)
    s.initialize()
    yield s
    s.close()


def inbox(project: Path) -> Path:
    return project / ".team" / "inbox.jsonl"


def append(project: Path, text: str):
    path = inbox(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="") as f:
        f.write(text)


def answer_line(ident, answer, ts="2026-10-23T10:00:00Z", **extra):
    entry = {"ts": ts, "id": ident, "answer": answer, "kind": extra.pop("kind", "question"),
             "source": extra.pop("source", "window"), **extra}
    return json.dumps(entry) + "\n"


def result_json(resp):
    assert "result" in resp, resp
    res = resp["result"]
    assert res.get("isError") is False, res
    content = res["content"]
    assert content and content[0]["type"] == "text"
    return json.loads(content[0]["text"])


# --- handshake -----------------------------------------------------------------------

def test_initialize_echoes_supported_version(project):
    s = Server(project)
    try:
        r = s.initialize("2025-06-18")["result"]
        assert r["protocolVersion"] == "2025-06-18"
        assert r["capabilities"]["tools"] == {}
        assert r["serverInfo"]["name"] == "office"
    finally:
        s.close()


def test_initialize_unknown_version_gets_server_latest(project):
    s = Server(project)
    try:
        r = s.initialize("1999-01-01")["result"]
        assert r["protocolVersion"] in office_mcp.SUPPORTED_VERSIONS
        assert r["protocolVersion"] == office_mcp.SUPPORTED_VERSIONS[0]
    finally:
        s.close()


def test_initialized_notification_gets_no_reply_and_ping_works(server):
    server.send("notifications/initialized", notify=True)
    r = server.request("ping")
    assert r["result"] == {}


def test_tools_list(server):
    tools = {t["name"]: t for t in server.request("tools/list")["result"]["tools"]}
    assert set(tools) == {WAIT, PENDING}
    schema = tools[WAIT]["inputSchema"]
    assert schema["type"] == "object"
    assert schema["required"] == ["id"]
    assert schema["properties"]["timeout_seconds"]["maximum"] == office_mcp.MAX_TIMEOUT
    assert tools[PENDING]["inputSchema"]["type"] == "object"
    assert tools[WAIT]["description"] and tools[PENDING]["description"]


# --- waiting -------------------------------------------------------------------------

def test_wait_returns_when_line_appended_mid_wait(server, project):
    msg_id = server.send("tools/call", {"name": WAIT, "arguments": {"id": "q-01", "timeout_seconds": 20}})
    time.sleep(0.5)
    assert server.msgs.empty()  # still waiting
    append(project, answer_line("q-02", "other id"))
    append(project, answer_line("a-01", "Option B", kind="approval", decision="approved",
                                option="o2", run_id="r1"))
    append(project, answer_line("q-01", "use postgres", answers={"1": "ok"}, text="ok"))
    start = time.time()
    resp = server.recv(timeout=10)
    assert resp["id"] == msg_id
    assert time.time() - start < 5
    got = result_json(resp)
    assert got["status"] == "answered"
    assert got["id"] == "q-01" and got["answer"] == "use postgres"
    assert got["source"] == "window" and got["kind"] == "question"
    assert got["answers"] == {"1": "ok"} and got["text"] == "ok"
    for key in ("decision", "option"):
        assert key in got


def test_wait_returns_approval_fields(server, project):
    append(project, answer_line("a-01", "Option B", kind="approval", decision="approved", option="o2"))
    got = result_json(server.call(WAIT, {"id": "a-01", "timeout_seconds": 5}))
    assert (got["kind"], got["decision"], got["option"]) == ("approval", "approved", "o2")


def test_timeout_is_a_result_not_an_error(server):
    start = time.time()
    got = result_json(server.call(WAIT, {"id": "q-none", "timeout_seconds": 1}))
    assert 0.9 <= time.time() - start < 5
    assert got["status"] == "no_answer"
    assert got["id"] == "q-none"
    assert "no answer" in got["message"].lower()


def test_missing_inbox_file_times_out_cleanly(server, project):
    got = result_json(server.call(WAIT, {"id": "q-01", "timeout_seconds": 0}))
    assert got["status"] == "no_answer"
    assert result_json(server.call(PENDING))["pending"] == []
    assert not (project / ".team").exists()


def test_default_timeout_used_when_omitted(server, project):
    append(project, answer_line("q-01", "yes"))
    got = result_json(server.call(WAIT, {"id": "q-01"}))
    assert got["answer"] == "yes"


def test_already_present_line_returned_once_then_consumed(server, project):
    append(project, answer_line("q-01", "first"))
    assert result_json(server.call(WAIT, {"id": "q-01", "timeout_seconds": 2}))["answer"] == "first"
    assert (project / ".team" / "inbox.consumed").is_file()
    assert result_json(server.call(WAIT, {"id": "q-01", "timeout_seconds": 1}))["status"] == "no_answer"
    append(project, answer_line("q-01", "second", ts="2026-10-23T10:05:00Z"))
    assert result_json(server.call(WAIT, {"id": "q-01", "timeout_seconds": 2}))["answer"] == "second"


def test_consumed_survives_restart(project):
    append(project, answer_line("q-01", "first"))
    s = Server(project)
    try:
        s.initialize()
        assert result_json(s.call(WAIT, {"id": "q-01", "timeout_seconds": 2}))["answer"] == "first"
    finally:
        s.close()
    s = Server(project)
    try:
        s.initialize()
        assert result_json(s.call(WAIT, {"id": "q-01", "timeout_seconds": 0}))["status"] == "no_answer"
    finally:
        s.close()


def test_newest_unconsumed_line_wins_and_older_are_consumed(server, project):
    append(project, answer_line("q-01", "old", ts="2026-10-23T10:00:00Z"))
    append(project, answer_line("q-01", "new", ts="2026-10-23T10:01:00Z"))
    assert result_json(server.call(WAIT, {"id": "q-01", "timeout_seconds": 2}))["answer"] == "new"
    assert result_json(server.call(WAIT, {"id": "q-01", "timeout_seconds": 0}))["status"] == "no_answer"


def test_older_line_than_returned_one_is_not_returned(server, project):
    append(project, answer_line("q-01", "new", ts="2026-10-23T10:05:00Z"))
    assert result_json(server.call(WAIT, {"id": "q-01", "timeout_seconds": 2}))["answer"] == "new"
    append(project, answer_line("q-01", "late but older", ts="2026-10-23T10:00:00Z"))
    assert result_json(server.call(WAIT, {"id": "q-01", "timeout_seconds": 0}))["status"] == "no_answer"


def test_invalid_and_half_written_lines_are_skipped(server, project):
    append(project, "not json\n")
    append(project, "[1, 2]\n")
    append(project, json.dumps({"id": "q-01"}) + "\n")  # no answer
    append(project, json.dumps({"answer": "x"}) + "\n")  # no id
    append(project, "\n")
    half = answer_line("q-01", "complete me").rstrip("\n")
    append(project, half[:20])
    got = result_json(server.call(WAIT, {"id": "q-01", "timeout_seconds": 0}))
    assert got["status"] == "no_answer"
    msg_id = server.send("tools/call", {"name": WAIT, "arguments": {"id": "q-01", "timeout_seconds": 10}})
    time.sleep(0.3)
    append(project, half[20:] + "\n")
    resp = server.recv(timeout=8)
    assert resp["id"] == msg_id
    assert result_json(resp)["answer"] == "complete me"


def test_many_ids(server, project):
    for i in range(200):
        append(project, answer_line(f"q-{i:03d}", f"answer {i}"))
    assert result_json(server.call(WAIT, {"id": "q-137", "timeout_seconds": 2}))["answer"] == "answer 137"
    pending = result_json(server.call(PENDING))["pending"]
    assert len(pending) == 199
    assert "q-137" not in {p["id"] for p in pending}


def test_pending_lists_unconsumed_without_consuming(server, project):
    append(project, answer_line("q-01", "a"))
    append(project, answer_line("a-01", "b", kind="approval", decision="rejected"))
    first = result_json(server.call(PENDING))["pending"]
    assert [p["id"] for p in first] == ["q-01", "a-01"]
    assert first[1]["decision"] == "rejected" and first[0]["source"] == "window"
    assert result_json(server.call(PENDING))["pending"] == first
    result_json(server.call(WAIT, {"id": "q-01", "timeout_seconds": 0}))
    assert [p["id"] for p in result_json(server.call(PENDING))["pending"]] == ["a-01"]


def test_ping_answered_during_a_wait(server, project):
    wait_id = server.send("tools/call", {"name": WAIT, "arguments": {"id": "q-01", "timeout_seconds": 20}})
    time.sleep(0.2)
    r = server.request("ping", timeout=3)
    assert r["result"] == {}
    append(project, answer_line("q-01", "done"))
    resp = server.recv(timeout=8)
    assert resp["id"] == wait_id


def test_cancelled_wait_sends_no_reply_and_consumes_nothing(server, project):
    wait_id = server.send("tools/call", {"name": WAIT, "arguments": {"id": "q-01", "timeout_seconds": 20}})
    time.sleep(0.2)
    server.send("notifications/cancelled", {"requestId": wait_id, "reason": "user"}, notify=True)
    time.sleep(0.4)
    append(project, answer_line("q-01", "after cancel"))
    time.sleep(0.4)
    r = server.request("ping", timeout=3)
    assert r["result"] == {}
    assert server.msgs.empty()
    assert [p["id"] for p in result_json(server.call(PENDING))["pending"]] == ["q-01"]


def test_project_from_env(tmp_path):
    proj = tmp_path / "envproj"
    proj.mkdir()
    append(proj, answer_line("q-env", "from env"))
    s = Server(None, env_project=proj)
    try:
        s.initialize()
        assert result_json(s.call(WAIT, {"id": "q-env", "timeout_seconds": 1}))["answer"] == "from env"
    finally:
        s.close()


def test_project_flag_beats_env(tmp_path):
    flag, env = tmp_path / "flag", tmp_path / "env"
    flag.mkdir()
    env.mkdir()
    append(flag, answer_line("q-1", "flag"))
    append(env, answer_line("q-1", "env"))
    s = Server(flag, env_project=env)
    try:
        s.initialize()
        assert result_json(s.call(WAIT, {"id": "q-1", "timeout_seconds": 1}))["answer"] == "flag"
    finally:
        s.close()


def test_exits_on_stdin_eof(project):
    s = Server(project)
    s.initialize()
    s.send("tools/call", {"name": WAIT, "arguments": {"id": "q-01", "timeout_seconds": 60}})
    time.sleep(0.2)
    s.proc.stdin.close()
    assert s.proc.wait(timeout=5) == 0


def test_unicode_answer_round_trip(server, project):
    append(project, answer_line("q-u", "haan, theek hai ✓ منظور"))
    assert result_json(server.call(WAIT, {"id": "q-u", "timeout_seconds": 1}))["answer"].endswith(
        "منظور")


# --- errors --------------------------------------------------------------------------

def test_parse_error(server):
    server.send_raw("{not json")
    r = server.recv()
    assert r["id"] is None and r["error"]["code"] == -32700


@pytest.mark.parametrize("raw", ['[]', '"x"', '{"jsonrpc": "2.0", "id": 5}',
                                 '{"jsonrpc": "1.0", "id": 6, "method": "ping"}',
                                 '{"jsonrpc": "2.0", "id": 7, "method": 3}'])
def test_invalid_request(server, raw):
    server.send_raw(raw)
    r = server.recv()
    assert r["error"]["code"] == -32600


def test_unknown_method(server):
    r = server.request("resources/list")
    assert r["error"]["code"] == -32601


def test_unknown_notification_is_ignored(server):
    server.send("notifications/whatever", {}, notify=True)
    assert server.request("ping")["result"] == {}


@pytest.mark.parametrize("params", [
    {"name": "no_such_tool", "arguments": {}},
    {"arguments": {"id": "q-01"}},
    {"name": WAIT, "arguments": {}},
    {"name": WAIT, "arguments": {"id": ""}},
    {"name": WAIT, "arguments": {"id": 5}},
    {"name": WAIT, "arguments": {"id": "q", "timeout_seconds": "ten"}},
    {"name": WAIT, "arguments": {"id": "q", "timeout_seconds": -1}},
    {"name": WAIT, "arguments": {"id": "q", "timeout_seconds": True}},
    {"name": WAIT, "arguments": "id=q"},
])
def test_invalid_params(server, params):
    r = server.request("tools/call", params)
    assert r["error"]["code"] == -32602, r


def test_blank_lines_on_stdin_are_ignored(server):
    server.send_raw("")
    server.send_raw("   ")
    assert server.request("ping")["result"] == {}


# --- unit: helpers -------------------------------------------------------------------

def test_timeout_is_clamped():
    assert office_mcp.parse_timeout(None) == office_mcp.DEFAULT_TIMEOUT == 600
    assert office_mcp.parse_timeout(99999) == office_mcp.MAX_TIMEOUT == 3500
    assert office_mcp.parse_timeout(2.5) == 2.5


def test_negotiate_version():
    assert office_mcp.negotiate("2024-11-05") == "2024-11-05"
    assert office_mcp.negotiate(None) == office_mcp.SUPPORTED_VERSIONS[0]
