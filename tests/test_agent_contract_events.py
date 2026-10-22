"""Boss-written events (run_started ... blocker_cleared) and extended approval/handoff fields."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import agent_contract as ac  # noqa: E402


def ev(type_, **over):
    e = {"ts": "2026-10-23T10:00:00Z", "type": type_, "agent": "orchestrator", "run_id": "run-1"}
    e.update(over)
    return e


def bad(event, key):
    errs = ac.validate_event(event)
    assert any(key in x for x in errs), errs


# Old events stay valid
@pytest.mark.parametrize("e", [
    ev("agent_start", agent="architect"),
    ev("agent_stop", agent="architect"),
    ev("file_written", agent="architect", path="a.md"),
    ev("handoff", **{"from": "orchestrator", "to": "architect"}),
    ev("approval_requested"),
    ev("approval_given"),
])
def test_old_events_still_valid(e):
    assert ac.validate_event(e) == []


def test_new_types_registered():
    for t in ("run_started", "run_finished", "agent_result", "question_asked", "blocked", "blocker_cleared"):
        assert t in ac.EVENT_TYPES


def test_run_started():
    assert ac.validate_event(ev("run_started", goal="Add login")) == []
    assert ac.validate_event(ev("run_started", goal="Add login", size="project")) == []
    bad(ev("run_started"), "goal")
    bad(ev("run_started", goal=" "), "goal")
    bad(ev("run_started", goal="x", size=3), "size")


def test_run_finished():
    for s in ("done", "stopped", "failed"):
        assert ac.validate_event(ev("run_finished", status=s, summary="ok")) == []
    bad(ev("run_finished", status="weird", summary="ok"), "status")
    bad(ev("run_finished", summary="ok"), "status")
    bad(ev("run_finished", status="done"), "summary")


def test_agent_result():
    for s in ac.RESPONSE_STATUSES:
        assert ac.validate_event(ev("agent_result", agent="architect", status=s, summary="x")) == []
    assert ac.validate_event(ev("agent_result", agent="architect", status="done", summary="x",
                                response_file=".team/runs/r/01-architect-response.json")) == []
    bad(ev("agent_result", agent="architect", status="finished", summary="x"), "status")
    bad(ev("agent_result", agent="architect", summary="x"), "status")
    bad(ev("agent_result", agent="architect", status="done"), "summary")
    bad(ev("agent_result", agent="architect", status="done", summary="x", response_file=""), "response_file")


def test_question_asked():
    q = [{"id": "q1", "question": "Email or link?", "why": "Changes design"}]
    assert ac.validate_event(ev("question_asked", id="q-01", agent="architect", questions=q)) == []
    bad(ev("question_asked", agent="architect", questions=q), "id")
    bad(ev("question_asked", id="q-01", agent="architect"), "questions")
    bad(ev("question_asked", id="q-01", agent="architect", questions=[]), "questions")
    bad(ev("question_asked", id="q-01", agent="architect", questions=[{"id": "q1"}]), "questions[0]")
    bad(ev("question_asked", id="q-01", agent="architect", questions="why"), "questions")


def test_blocked_and_cleared():
    assert ac.validate_event(ev("blocked", agent="architect", reason="Tests cannot run")) == []
    bad(ev("blocked", agent="architect"), "reason")
    bad(ev("blocked", agent="architect", reason=""), "reason")
    assert ac.validate_event(ev("blocker_cleared", agent="architect")) == []


def test_approval_requested_extended():
    full = ev("approval_requested", id="a1", kind="decision", title="Database", why="One-way",
              options=[{"id": "o1", "label": "sqlite", "note": "simple", "recommended": True}],
              one_way_door=True, asked_agent="architect")
    assert ac.validate_event(full) == []
    assert ac.validate_event(ev("approval_requested", id="a1", kind="questions")) == []
    bad(ev("approval_requested", kind="decision"), "id")
    bad(ev("approval_requested", id="a1", kind="other"), "kind")
    bad(ev("approval_requested", id="a1", kind="decision", one_way_door="yes"), "one_way_door")
    bad(ev("approval_requested", id="a1", kind="decision", options=[{"label": "x"}]), "options[0]")
    bad(ev("approval_requested", id="a1", kind="decision", options="sqlite"), "options")
    bad(ev("approval_requested", id="a1", kind="decision", asked_agent=""), "asked_agent")


def test_approval_given_extended():
    assert ac.validate_event(ev("approval_given", id="a1", decision="approved", option="o1", by="terminal")) == []
    assert ac.validate_event(ev("approval_given", id="q-01", decision="answered", by="window",
                                answers=[{"id": "q1", "answer": "Email"}])) == []
    assert ac.validate_event(ev("approval_given", id="a1", decision="rejected")) == []
    bad(ev("approval_given", decision="approved"), "id")
    bad(ev("approval_given", id="a1", decision="maybe"), "decision")
    bad(ev("approval_given", id="a1", decision="approved", by="phone"), "by")
    bad(ev("approval_given", id="a1", decision="answered", answers=[{"id": "q1"}]), "answers[0]")


def test_handoff_task_optional():
    h = {"from": "orchestrator", "to": "architect"}
    assert ac.validate_event(ev("handoff", task="Plan the login page", **h)) == []
    bad(ev("handoff", task="", **h), "task")
    bad(ev("handoff", task=5, **h), "task")


def test_append_event_accepts_new_event(tmp_path):
    p = tmp_path / "events.jsonl"
    ac.append_event(p, ev("run_started", goal="Add login"))
    assert p.read_text(encoding="utf-8").count("\n") == 1
    with pytest.raises(ValueError):
        ac.append_event(p, ev("run_started"))
