import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "orchestrator" / "scripts" / "team_event.py"
sys.path.insert(0, str(ROOT / "scripts"))

import agent_contract as ac  # noqa: E402

_spec = importlib.util.spec_from_file_location("team_event", SCRIPT)
te = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(te)

QUESTIONS = [{"id": "q1", "question": "Email or link?", "why": "Changes the design"}]
OPTIONS = [{"id": "o1", "label": "sqlite", "recommended": True}, {"id": "o2", "label": "postgres"}]

# type -> (fields, agent or None)
EXAMPLES = {
    "run_started": ({"goal": "Add login", "size": "project"}, None),
    "run_finished": ({"status": "done", "summary": "All done"}, None),
    "handoff": ({"from": "orchestrator", "to": "architect", "task": "Plan it"}, None),
    "agent_result": (
        {"status": "done", "summary": "Planned", "response_file": ".team/runs/r/01-architect-response.json"},
        "architect",
    ),
    "question_asked": ({"id": "q-01", "questions": QUESTIONS}, "architect"),
    "blocked": ({"reason": "Python missing"}, "architect"),
    "blocker_cleared": ({}, "architect"),
    "approval_requested": (
        {"id": "a1", "kind": "decision", "title": "Storage", "why": "Hard to undo",
         "options": OPTIONS, "one_way_door": True, "asked_agent": "architect"},
        None,
    ),
    "approval_given": (
        {"id": "a1", "decision": "approved", "option": "o1", "by": "terminal",
         "answers": [{"id": "q1", "answer": "link"}]},
        None,
    ),
}


def make(etype):
    fields, agent = EXAMPLES[etype]
    return te.build_event(etype, "2026-10-23-login", dict(fields), agent=agent)


def run_cli(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8", cwd=cwd
    )


# ---------- drift: the embedded table versus the contract ----------

def test_examples_cover_every_writable_type():
    assert set(EXAMPLES) == set(te.EVENT_TABLE)
    assert set(te.EVENT_TABLE) | set(te.HOOK_TYPES) == set(ac.EVENT_TYPES)


@pytest.mark.parametrize("etype", sorted(EXAMPLES))
def test_every_example_passes_the_contract(etype):
    event = make(etype)
    assert ac.validate_event(event) == []
    assert te.validate_event_line(event) == []


@pytest.mark.parametrize("etype", sorted(EXAMPLES))
def test_minimal_examples_pass_the_contract(etype):
    fields, agent = EXAMPLES[etype]
    required = {k: v for k, v in fields.items() if k in te.EVENT_TABLE[etype]["required"]}
    event = te.build_event(etype, "r1", required, agent=agent)
    assert ac.validate_event(event) == []


def test_constants_match_contract():
    assert te.RESPONSE_STATUSES == ac.RESPONSE_STATUSES
    assert te.RUN_STATUSES == ac.RUN_FINISHED_STATUSES
    assert te.APPROVAL_KINDS == ac.APPROVAL_KINDS
    assert te.APPROVAL_DECISIONS == ac.APPROVAL_DECISIONS
    assert te.APPROVAL_SOURCES == ac.APPROVAL_SOURCES


def test_request_and_response_checks_agree_with_contract():
    good_req = {"goal": "g", "context_files": [], "constraints": [], "done_when": ["x"]}
    bad_reqs = [{}, {**good_req, "done_when": []}, {**good_req, "goal": " "}, {**good_req, "constraints": "x"}]
    for r in [good_req] + bad_reqs:
        assert bool(te.validate_request(r)) == bool(ac.validate_request(r))
    good_res = {"status": "done", "summary": "s", "files": [], "questions": [], "approvals": [],
                "assumptions": [], "evidence": ["ran tests"]}
    bad_res = [{}, {**good_res, "evidence": []}, {**good_res, "status": "needs_answers"},
               {**good_res, "status": "needs_approval"}, {**good_res, "status": "weird"}]
    for r in [good_res] + bad_res:
        assert bool(te.validate_response(r)) == bool(ac.validate_response(r))


# ---------- defaults, ts, refusals ----------

@pytest.mark.parametrize("etype", ["run_started", "run_finished", "handoff", "approval_requested", "approval_given"])
def test_boss_agent_default(etype):
    fields, _ = EXAMPLES[etype]
    assert te.build_event(etype, "r1", dict(fields))["agent"] == "orchestrator"


def test_agent_required_for_specialist_events():
    with pytest.raises(ValueError, match="agent"):
        te.build_event("blocked", "r1", {"reason": "x"})


def test_approval_given_by_defaults_to_terminal():
    ev = te.build_event("approval_given", "r1", {"id": "a1", "decision": "answered"})
    assert ev["by"] == "terminal"


def test_ts_is_real_utc_z_time():
    ev = make("run_started")
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", ev["ts"])
    now = te.datetime.now(te.timezone.utc)
    then = te.datetime.fromisoformat(ev["ts"].replace("Z", "+00:00"))
    assert abs((now - then).total_seconds()) < 5


@pytest.mark.parametrize("etype", ["agent_start", "agent_stop", "file_written"])
def test_hook_types_refused(etype):
    with pytest.raises(ValueError, match="hook"):
        te.build_event(etype, "r1", {}, agent="x")


def test_unknown_type_and_field_refused():
    with pytest.raises(ValueError):
        te.build_event("nope", "r1", {})
    with pytest.raises(ValueError, match="not a field"):
        te.build_event("run_started", "r1", {"goal": "g", "reason": "x"})


@pytest.mark.parametrize("etype", sorted(EXAMPLES))
def test_each_required_field_is_enforced(etype):
    fields, agent = EXAMPLES[etype]
    for name in te.EVENT_TABLE[etype]["required"]:
        partial = {k: v for k, v in fields.items() if k != name}
        with pytest.raises(ValueError, match=name):
            te.build_event(etype, "r1", partial, agent=agent)


def test_bad_values_refused():
    with pytest.raises(ValueError):
        te.build_event("run_finished", "r1", {"status": "ok", "summary": "s"})
    with pytest.raises(ValueError):
        te.build_event("question_asked", "r1", {"id": "q", "questions": [{"id": "q1"}]}, agent="a")
    with pytest.raises(ValueError):
        te.build_event("approval_requested", "r1", {**EXAMPLES["approval_requested"][0], "one_way_door": "yes"})


# ---------- CLI ----------

def test_cli_writes_one_line_and_creates_folder(tmp_path):
    r = run_cli("event", "run_started", "--run-id", "r1", "--goal", "Büro \u2713", "--size", "project",
                "--project", str(tmp_path))
    assert r.returncode == 0, r.stderr
    log = tmp_path / ".agents" / "events.jsonl"
    data = log.read_bytes()
    assert data.endswith(b"\n") and data.count(b"\n") == 1
    line = data.decode("utf-8").strip()
    assert r.stdout.strip() == line
    obj = json.loads(line)
    assert obj["goal"] == "Büro \u2713" and "\\u" not in line
    assert ac.validate_event(obj) == []


def test_cli_default_log_is_cwd_relative(tmp_path):
    r = run_cli("event", "handoff", "--run-id", "r1", "--from", "orchestrator", "--to", "architect",
                "--task", "t", cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / ".agents" / "events.jsonl").is_file()


def test_cli_appends_and_log_override(tmp_path):
    log = tmp_path / "x" / "my.jsonl"
    for goal in ("a", "b"):
        assert run_cli("event", "run_started", "--run-id", "r1", "--goal", goal, "--log", str(log)).returncode == 0
    assert len(log.read_text(encoding="utf-8").splitlines()) == 2


def test_cli_refusal_writes_nothing(tmp_path):
    r = run_cli("event", "run_started", "--run-id", "r1", "--project", str(tmp_path))
    assert r.returncode == 2
    assert "goal" in r.stderr and r.stdout == ""
    assert not (tmp_path / ".agents").exists()


def test_cli_hook_type_and_bad_json_refused(tmp_path):
    assert run_cli("event", "agent_start", "--run-id", "r1", "--agent", "a", "--project", str(tmp_path)).returncode == 2
    r = run_cli("event", "question_asked", "--run-id", "r1", "--agent", "a", "--id", "q-01",
                "--questions-json", "{oops", "--project", str(tmp_path))
    assert r.returncode == 2 and "questions-json" in r.stderr
    assert not (tmp_path / ".agents").exists()


def test_cli_documented_examples(tmp_path):
    log = str(tmp_path / "e.jsonl")
    cmds = [
        ["run_started", "--run-id", "r1", "--goal", "g", "--size", "project"],
        ["handoff", "--run-id", "r1", "--from", "orchestrator", "--to", "architect", "--task", "t"],
        ["agent_result", "--run-id", "r1", "--agent", "architect", "--status", "done", "--summary", "s",
         "--response-file", "p.json"],
        ["question_asked", "--run-id", "r1", "--agent", "architect", "--id", "q-01",
         "--questions-json", json.dumps(QUESTIONS)],
        ["approval_requested", "--run-id", "r1", "--id", "a1", "--kind", "decision", "--title", "t",
         "--why", "w", "--options-json", json.dumps(OPTIONS), "--one-way-door", "true",
         "--asked-agent", "architect"],
        ["approval_given", "--run-id", "r1", "--id", "a1", "--decision", "approved", "--option", "o1",
         "--by", "terminal"],
        ["blocked", "--run-id", "r1", "--agent", "architect", "--reason", "r"],
        ["blocker_cleared", "--run-id", "r1", "--agent", "architect"],
        ["run_finished", "--run-id", "r1", "--status", "done", "--summary", "s"],
    ]
    for c in cmds:
        r = run_cli("event", *c, "--log", log)
        assert r.returncode == 0, (c, r.stderr)
    for raw in Path(log).read_text(encoding="utf-8").splitlines():
        assert ac.validate_event(json.loads(raw)) == []


# ---------- check-run ----------

RUN_ID = "2026-10-23-login"
GOOD_REQ = {"goal": "Plan", "context_files": ["a.md"], "constraints": [], "done_when": ["plan exists"]}
GOOD_RES = {"status": "done", "summary": "ok", "files": [], "questions": [], "approvals": [],
            "assumptions": [], "evidence": ["read the files"]}


def build_run(tmp_path, closed=True):
    run = tmp_path / ".team" / "runs" / RUN_ID
    run.mkdir(parents=True)
    (run / "plan.md").write_text("plan\n", encoding="utf-8")
    (run / "01-architect-request.json").write_text(json.dumps(GOOD_REQ), encoding="utf-8")
    (run / "01-architect-response.json").write_text(json.dumps(GOOD_RES), encoding="utf-8")
    if closed:
        (run / "summary.md").write_text("done\n", encoding="utf-8")
    log = tmp_path / ".agents" / "events.jsonl"
    events = [
        te.build_event("run_started", RUN_ID, {"goal": "g", "size": "project"}),
        te.build_event("handoff", RUN_ID, {"from": "orchestrator", "to": "architect", "task": "t"}),
        te.build_event("handoff", RUN_ID, {"from": "architect", "to": "orchestrator", "task": "back"}),
        te.build_event("agent_result", RUN_ID, {"status": "done", "summary": "s"}, agent="architect"),
    ]
    if closed:
        events.append(te.build_event("run_finished", RUN_ID, {"status": "done", "summary": "s"}))
    log.parent.mkdir()
    return run, log, events


def put(log, events):
    log.write_text("".join(json.dumps(e) + "\n" for e in events), encoding="utf-8")


def problems_of(run, log=None):
    return te.check_run(run, log)[0]


def test_check_run_good_closed_folder(tmp_path):
    run, log, events = build_run(tmp_path)
    put(log, events)
    assert te.check_run(run) == ([], [])
    r = run_cli("check-run", str(run))
    assert r.returncode == 0 and r.stdout.startswith("OK")


def test_check_run_open_run_needs_no_summary(tmp_path):
    run, log, events = build_run(tmp_path, closed=False)
    put(log, events)
    problems, notes = te.check_run(run)
    assert problems == [] and any("open run" in n for n in notes)


def test_check_run_log_option(tmp_path):
    run, log, events = build_run(tmp_path)
    other = tmp_path / "elsewhere.jsonl"
    put(other, events)
    assert problems_of(run, other) == []


def test_check_run_cli_reports_problems(tmp_path):
    run, log, events = build_run(tmp_path)
    put(log, events)
    (run / "summary.md").unlink()
    r = run_cli("check-run", str(run))
    assert r.returncode == 1 and r.stdout.startswith("PROBLEMS") and "summary.md" in r.stdout


def test_check_run_missing_plan_and_summary(tmp_path):
    run, log, events = build_run(tmp_path)
    put(log, events)
    (run / "plan.md").unlink()
    (run / "summary.md").unlink()
    text = "\n".join(problems_of(run))
    assert "plan.md" in text and "summary.md" in text


def test_check_run_bad_request_and_response(tmp_path):
    run, log, events = build_run(tmp_path)
    put(log, events)
    (run / "01-architect-request.json").write_text(json.dumps({"goal": "x"}), encoding="utf-8")
    (run / "01-architect-response.json").write_text(json.dumps({**GOOD_RES, "evidence": []}), encoding="utf-8")
    text = "\n".join(problems_of(run))
    assert "request.json: context_files" in text and "done_when" in text
    assert "response.json: evidence" in text


def test_check_run_unreadable_json(tmp_path):
    run, log, events = build_run(tmp_path)
    put(log, events)
    (run / "01-architect-response.json").write_text("{nope", encoding="utf-8")
    assert any("cannot read JSON" in p for p in problems_of(run))


def test_check_run_missing_pair_member(tmp_path):
    run, log, events = build_run(tmp_path)
    put(log, events)
    (run / "01-architect-request.json").unlink()
    assert any("request.json is missing" in p for p in problems_of(run))
    (run / "01-architect-request.json").write_text(json.dumps(GOOD_REQ), encoding="utf-8")
    (run / "01-architect-response.json").unlink()
    assert any("response.json is missing" in p for p in problems_of(run))


def test_check_run_run_started_not_first(tmp_path):
    run, log, events = build_run(tmp_path)
    put(log, events[1:] + events[:1])
    text = "\n".join(problems_of(run))
    assert "not run_started" in text


def test_check_run_no_events_or_no_log(tmp_path):
    run, log, events = build_run(tmp_path)
    assert any("event log not found" in p for p in problems_of(run))
    put(log, [dict(e, run_id="other") for e in events])
    assert any("no events for run" in p for p in problems_of(run))


def test_check_run_missing_handoffs_and_result(tmp_path):
    run, log, events = build_run(tmp_path)
    put(log, [e for e in events if e["type"] in ("run_started", "run_finished")])
    text = "\n".join(problems_of(run))
    assert "handoff event(s) to it" in text
    assert "return handoff" in text
    assert "agent_result" in text


def test_check_run_run_finished_must_be_last(tmp_path):
    run, log, events = build_run(tmp_path)
    put(log, events[:-1] + [events[-1]] + [events[3]])
    assert any("not the last event" in p for p in problems_of(run))


def test_check_run_invalid_event_line(tmp_path):
    run, log, events = build_run(tmp_path)
    bad = dict(events[1])
    del bad["to"]
    put(log, [events[0], bad] + events[2:])
    log.write_text(log.read_text(encoding="utf-8") + "not json\n", encoding="utf-8")
    text = "\n".join(problems_of(run))
    assert "to: required text" in text and "not valid JSON" in text


def test_check_run_hand_written_wrong_format_is_caught(tmp_path):
    run, log, events = build_run(tmp_path)
    put(log, events)
    wrong = {"event": "run_started", "run": RUN_ID, "by": "orchestrator"}
    log.write_text(log.read_text(encoding="utf-8") + json.dumps(wrong) + "\n", encoding="utf-8")
    # no run_id on the wrong line, so it is not matched to this run; the right lines stay valid
    assert problems_of(run) == []


def test_check_run_pending_approval(tmp_path):
    run, log, events = build_run(tmp_path, closed=False)
    req = make("approval_requested")
    req["run_id"] = RUN_ID
    put(log, events + [req])
    problems, notes = te.check_run(run)
    assert problems == [] and "pending approval: a1" in notes
    given = make("approval_given")
    given["run_id"] = RUN_ID
    put(log, events + [req, given])
    assert not any("pending" in n for n in te.check_run(run)[1])
    # a given event that comes before the request does not clear it
    put(log, events + [given, req])
    assert "pending approval: a1" in te.check_run(run)[1]


def test_check_run_missing_folder(tmp_path):
    assert te.check_run(tmp_path / "nope")[0]
