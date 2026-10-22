import http.client
import json
import socket
import sys
import threading
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import office_server as os_  # noqa: E402

ROSTER = (
    "# Roster\n\n| Name | Skill | Model | Owns |\n|---|---|---|---|\n"
    "| architect | software-architect | opus | designs, ADRs |\n"
    "| code-reviewer | code-reviewer | opus | review reports |\n"
)


class Office:
    def __init__(self, root: Path):
        self.project = root / "project"
        self.project.mkdir()
        self.repo = root / "repo"
        (self.repo / "docs" / "agents" / "visual-office").mkdir(parents=True)
        (self.repo / "docs" / "agents" / "roster.md").write_text(ROSTER, encoding="utf-8")
        (self.repo / "docs" / "agents" / "visual-office" / "mock-v2.html").write_text(
            "<html>mock</html>", encoding="utf-8")
        (self.repo / "secret.txt").write_text("secret", encoding="utf-8")
        self.events = self.project / ".agents" / "events.jsonl"
        self.server = os_.make_server(self.project, port=0, repo_root=self.repo)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def conn(self, timeout: float = 5) -> http.client.HTTPConnection:
        return http.client.HTTPConnection("127.0.0.1", self.port, timeout=timeout)

    def get(self, path: str):
        c = self.conn()
        c.request("GET", path)
        r = c.getresponse()
        body = r.read()
        c.close()
        return r.status, body

    def post(self, body, headers=None):
        c = self.conn()
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        h = {"Content-Type": "application/json"}
        h.update(headers or {})
        c.request("POST", "/answer", body=data, headers=h)
        r = c.getresponse()
        out = r.read()
        c.close()
        return r.status, out

    def write_events(self, *lines: str, mode="w"):
        self.events.parent.mkdir(parents=True, exist_ok=True)
        with open(self.events, mode, encoding="utf-8", newline="") as f:
            f.write("".join(lines))

    def stream(self):
        c = self.conn(timeout=5)
        c.request("GET", "/events")
        r = c.getresponse()
        assert r.status == 200
        assert "text/event-stream" in r.getheader("Content-Type")
        return c, r

    def close(self):
        self.server.shutdown()
        self.server.server_close()


@pytest.fixture
def office(tmp_path):
    o = Office(tmp_path)
    yield o
    o.close()


def read_events(resp, n):
    """Read n `data:` events from an SSE response."""
    got = []
    while len(got) < n:
        line = resp.readline()
        assert line, "stream ended early"
        line = line.decode().rstrip("\r\n")
        if line.startswith("data: "):
            got.append(json.loads(line[6:]))
    return got


def test_binds_loopback_only(office):
    assert office.server.server_address[0] == "127.0.0.1"
    with pytest.raises(ValueError):
        os_.make_server(office.project, host="0.0.0.0", port=0, repo_root=office.repo)


def test_replays_existing_events(office):
    office.write_events('{"n": 1}\n', '{"n": 2}\n')
    c, r = office.stream()
    assert read_events(r, 2) == [{"n": 1}, {"n": 2}]
    c.close()


def test_follows_appended_events(office):
    office.write_events('{"n": 1}\n')
    c, r = office.stream()
    assert read_events(r, 1) == [{"n": 1}]
    office.write_events('{"n": 2}\n', mode="a")
    assert read_events(r, 1) == [{"n": 2}]
    c.close()


def test_missing_file_then_created(office):
    assert not office.events.exists()
    c, r = office.stream()
    time.sleep(0.5)
    office.write_events('{"n": 7}\n')
    assert read_events(r, 1) == [{"n": 7}]
    c.close()


def test_half_written_line_waits_for_newline(office):
    office.write_events('{"n": 1}\n{"n": ')
    c, r = office.stream()
    assert read_events(r, 1) == [{"n": 1}]
    time.sleep(0.8)
    office.write_events('2}\n', mode="a")
    assert read_events(r, 1) == [{"n": 2}]
    c.close()


def test_invalid_lines_skipped(office):
    office.write_events('not json\n', '\n', '{"n": 1}\n', '[1,\n', '{"n": 2}\n')
    c, r = office.stream()
    assert read_events(r, 2) == [{"n": 1}, {"n": 2}]
    c.close()


def test_truncation_restarts(office):
    office.write_events('{"n": 1}\n{"n": 2}\n')
    c, r = office.stream()
    assert read_events(r, 2) == [{"n": 1}, {"n": 2}]
    office.write_events('{"n": 3}\n')  # shorter than before
    assert read_events(r, 1) == [{"n": 3}]
    c.close()


def test_roster(office):
    status, body = office.get("/roster")
    assert status == 200
    assert json.loads(body) == [
        {"name": "architect", "skill": "software-architect", "model": "opus", "owns": "designs, ADRs"},
        {"name": "code-reviewer", "skill": "code-reviewer", "model": "opus", "owns": "review reports"},
    ]


def test_roster_missing_is_empty_list(office):
    (office.repo / "docs" / "agents" / "roster.md").unlink()
    status, body = office.get("/roster")
    assert status == 200 and json.loads(body) == []


def test_state_pending_logic(office):
    office.write_events(
        '{"type": "approval_requested", "approval_id": "a1"}\n',
        '{"type": "approval_requested", "approval_id": "a2"}\n',
        'garbage\n',
        '{"type": "approval_given", "approval_id": "a1"}\n',
    )
    status, body = office.get("/state")
    state = json.loads(body)
    assert status == 200
    assert state["events"] == 3
    assert [e["approval_id"] for e in state["pending_approvals"]] == ["a2"]


def test_state_without_file(office):
    status, body = office.get("/state")
    assert status == 200
    assert json.loads(body) == {"events": 0, "pending_approvals": []}


def test_answer_valid_appends_line(office):
    origin = f"http://127.0.0.1:{office.port}"
    status, _ = office.post({"id": "q1", "answer": "yes", "kind": "question"}, {"Origin": origin})
    assert status == 200
    status, _ = office.post({"id": "a1", "answer": "approved", "kind": "approval"})  # no Origin
    assert status == 200
    lines = (office.project / ".team" / "inbox.jsonl").read_text(encoding="utf-8").splitlines()
    first, second = json.loads(lines[0]), json.loads(lines[1])
    assert (first["id"], first["answer"], first["kind"], first["source"]) == ("q1", "yes", "question", "window")
    assert first["ts"].endswith("Z") and len(first["ts"]) == 20
    assert second["kind"] == "approval"


def test_answer_localhost_origin_ok(office):
    status, _ = office.post({"id": "q", "answer": "x"}, {"Origin": f"http://localhost:{office.port}"})
    assert status == 200


def test_answer_rejects_big_body(office):
    status, _ = office.post({"id": "q", "answer": "x" * 70000})
    assert status == 400
    assert not (office.project / ".team" / "inbox.jsonl").exists()


def test_answer_rejects_non_json(office):
    assert office.post(b"not json")[0] == 400


def test_answer_rejects_missing_fields(office):
    assert office.post({"answer": "x"})[0] == 400
    assert office.post({"id": "q"})[0] == 400
    assert office.post([1, 2])[0] == 400


def test_answer_rejects_foreign_origin(office):
    status, _ = office.post({"id": "q", "answer": "x"}, {"Origin": "http://evil.example"})
    assert status == 403
    status, _ = office.post({"id": "q", "answer": "x"}, {"Origin": f"http://127.0.0.1:{office.port + 1}"})
    assert status == 403
    assert not (office.project / ".team" / "inbox.jsonl").exists()


def test_index_serves_mock(office):
    status, body = office.get("/")
    assert status == 200 and b"mock" in body


def test_built_ui_preferred_as_index(office):
    (office.repo / "docs" / "agents" / "visual-office" / "index.html").write_text("built", encoding="utf-8")
    assert office.get("/") == (200, b"built")


def test_static_file_and_missing(office):
    assert office.get("/mock-v2.html")[0] == 200
    assert office.get("/nope.html")[0] == 404


@pytest.mark.parametrize("path", [
    "/../../secret.txt", "/%2e%2e/%2e%2e/secret.txt", "/..%5c..%5csecret.txt", "/%2e%2e%2f%2e%2e%2fsecret.txt",
])
def test_path_traversal_rejected(office, path):
    s = socket.create_connection(("127.0.0.1", office.port), timeout=5)
    s.sendall(f"GET {path} HTTP/1.1\r\nHost: 127.0.0.1:{office.port}\r\nConnection: close\r\n\r\n".encode())
    data = b""
    while chunk := s.recv(4096):
        data += chunk
    s.close()
    status = int(data.split(b" ", 2)[1])
    assert status in (400, 403, 404)
    assert b"secret" not in data.split(b"\r\n\r\n", 1)[1]


def test_state_pairs_approvals_on_id_of_the_new_contract(office):
    office.write_events(
        '{"type": "approval_requested", "id": "a1", "title": "Pick a database"}\n',
        '{"type": "approval_requested", "id": "a2"}\n',
        '{"type": "question_asked", "id": "a2"}\n',
        '{"type": "approval_given", "id": "a1", "decision": "approved"}\n',
    )
    _, body = office.get("/state")
    assert [e["id"] for e in json.loads(body)["pending_approvals"]] == ["a2"]


def test_state_old_approval_id_still_works(office):
    office.write_events(
        '{"type": "approval_requested", "approval_id": "x"}\n',
        '{"type": "approval_given", "id": "x"}\n',
    )
    _, body = office.get("/state")
    assert json.loads(body)["pending_approvals"] == []


def test_answer_keeps_structured_fields_and_drops_unknown_ones(office):
    status, _ = office.post({"id": "a1", "answer": "approved", "kind": "approval", "decision": "approved",
                             "option": "o1", "answers": [{"id": "q1", "answer": "x"}], "text": "ok",
                             "run_id": "r1", "evil": "dropped"})
    assert status == 200
    line = json.loads((office.project / ".team" / "inbox.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert line["decision"] == "approved" and line["option"] == "o1" and line["run_id"] == "r1"
    assert line["answers"] == [{"id": "q1", "answer": "x"}] and line["text"] == "ok"
    assert "evil" not in line
