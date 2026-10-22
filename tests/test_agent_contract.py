import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import agent_contract as ac  # noqa: E402


def good_response(**over):
    r = {
        "status": "done",
        "summary": "Built the login page.",
        "files": ["src/login.py"],
        "questions": [],
        "approvals": [],
        "assumptions": ["Email login only"],
        "evidence": ["pytest: 4 passed"],
    }
    r.update(over)
    return r


def test_valid_response_done_has_no_errors():
    assert ac.validate_response(good_response()) == []


def test_done_without_evidence_is_error():
    errs = ac.validate_response(good_response(evidence=[]))
    assert any("evidence" in e for e in errs)


def test_needs_answers_requires_questions():
    errs = ac.validate_response(good_response(status="needs_answers", evidence=[]))
    assert any("questions" in e for e in errs)
    ok = good_response(
        status="needs_answers",
        evidence=[],
        questions=[{"id": "q1", "question": "Which login?", "why": "Changes design"}],
    )
    assert ac.validate_response(ok) == []


def test_needs_approval_requires_approvals():
    errs = ac.validate_response(good_response(status="needs_approval", evidence=[]))
    assert any("approvals" in e for e in errs)
    ok = good_response(
        status="needs_approval",
        evidence=[],
        approvals=[
            {
                "id": "a1",
                "decision": "Pick a database",
                "options": ["sqlite", "postgres"],
                "recommended": "sqlite",
                "one_way_door": False,
            }
        ],
    )
    assert ac.validate_response(ok) == []


def test_unknown_status_is_error():
    errs = ac.validate_response(good_response(status="maybe"))
    assert any("status" in e for e in errs)


def test_request_requires_goal_and_done_when():
    errs = ac.validate_request({"context_files": [], "constraints": []})
    assert any("goal" in e for e in errs)
    assert any("done_when" in e for e in errs)
    ok = {
        "goal": "Add login",
        "context_files": ["README.md"],
        "constraints": ["No new dependencies"],
        "done_when": ["Tests pass"],
    }
    assert ac.validate_request(ok) == []


def good_event(**over):
    e = {
        "ts": "2026-10-22T10:00:00Z",
        "type": "agent_start",
        "agent": "architect",
        "run_id": "run-1",
    }
    e.update(over)
    return e


def test_event_file_written_requires_path():
    errs = ac.validate_event(good_event(type="file_written"))
    assert any("path" in e for e in errs)
    assert ac.validate_event(good_event(type="file_written", path="a.md")) == []


def test_handoff_requires_from_and_to():
    errs = ac.validate_event(good_event(type="handoff"))
    assert any("from" in e for e in errs)
    assert any("to" in e for e in errs)
    assert ac.validate_event(good_event(type="handoff", **{"from": "boss", "to": "architect"})) == []


def test_append_event_writes_one_line_and_rejects_invalid(tmp_path):
    p = tmp_path / "sub" / "events.jsonl"
    ac.append_event(p, good_event())
    lines = p.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["type"] == "agent_start"
    before = p.read_text(encoding="utf-8")
    with pytest.raises(ValueError):
        ac.append_event(p, good_event(type="nope"))
    assert p.read_text(encoding="utf-8") == before


def test_response_missing_questions_is_error():
    r = good_response()
    del r["questions"]
    assert any("questions" in e and "missing" in e for e in ac.validate_response(r))


def test_response_missing_approvals_is_error():
    r = good_response()
    del r["approvals"]
    assert any("approvals" in e and "missing" in e for e in ac.validate_response(r))
