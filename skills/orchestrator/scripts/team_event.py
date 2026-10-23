#!/usr/bin/env python3
"""Write run events for the boss and check a run folder. Standard library only.

The boss never writes event JSON by hand: it runs this script.

  python team_event.py event TYPE --run-id ID [fields...] [--log PATH | --project DIR]
  python team_event.py check-run RUN_DIR [--log PATH]

`event` validates against the table below, refuses (exit 2, nothing written) when
a field is missing or wrong, appends exactly one line to the log
(default ./.agents/events.jsonl) and prints that line.
`check-run` prints OK or PROBLEMS (one per line) and exits 0 or 1.

This file is self-contained on purpose (it is installed without the repo). The
table mirrors scripts/agent_contract.py; tests/test_team_event.py checks that
they cannot drift apart.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RESPONSE_STATUSES = ("done", "needs_answers", "needs_approval", "blocked")
RUN_STATUSES = ("done", "stopped", "failed")
APPROVAL_KINDS = ("decision", "questions")
APPROVAL_DECISIONS = ("answered", "approved", "rejected")
APPROVAL_SOURCES = ("terminal", "window")
BOSS = "orchestrator"
DEFAULT_LOG = Path(".agents") / "events.jsonl"

# Field kinds: str, bool, questions, options, answers, or a tuple of allowed values.
# "required" and "optional" are the fields beyond ts/type/agent/run_id.
# "agent": default value of `agent` (None = the caller must pass --agent).
EVENT_TABLE = {
    "run_started": {"agent": BOSS, "required": {"goal": "str"}, "optional": {"size": "str"}},
    "run_finished": {
        "agent": BOSS,
        "required": {"status": RUN_STATUSES, "summary": "str"},
        "optional": {},
    },
    "handoff": {
        "agent": BOSS,
        "required": {"from": "str", "to": "str"},
        "optional": {"task": "str"},
    },
    "agent_result": {
        "agent": None,
        "required": {"status": RESPONSE_STATUSES, "summary": "str"},
        "optional": {"response_file": "str"},
    },
    "question_asked": {"agent": None, "required": {"id": "str", "questions": "questions"}, "optional": {}},
    "blocked": {"agent": None, "required": {"reason": "str"}, "optional": {}},
    "blocker_cleared": {"agent": None, "required": {}, "optional": {}},
    "approval_requested": {
        "agent": BOSS,
        "required": {
            "id": "str",
            "kind": APPROVAL_KINDS,
            "title": "str",
            "why": "str",
            "options": "options",
            "one_way_door": "bool",
            "asked_agent": "str",
        },
        "optional": {},
    },
    "approval_given": {
        "agent": BOSS,
        "required": {"id": "str", "decision": APPROVAL_DECISIONS},
        "optional": {"option": "str", "by": APPROVAL_SOURCES, "answers": "answers"},
    },
}
# Written by the hook, never by this script; still known so check-run can read them.
HOOK_TYPES = {"agent_start": {}, "agent_stop": {}, "file_written": {"path": "str"}}
ALL_TYPES = tuple(EVENT_TABLE) + tuple(HOOK_TYPES)


def _is_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _valid_ts(ts) -> bool:
    if not isinstance(ts, str) or not re.search(r"(Z|[+-]00:?00)$", ts):
        return False
    try:
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _check_kind(name: str, kind, value) -> list[str]:
    if isinstance(kind, tuple):
        return [] if value in kind else [f"{name}: must be one of {', '.join(kind)}"]
    if kind == "str":
        return [] if _is_str(value) else [f"{name}: required text"]
    if kind == "bool":
        return [] if isinstance(value, bool) else [f"{name}: must be true or false"]
    specs = {
        "questions": {"id": "str", "question": "str", "why": "str"},
        "options": {"id": "str", "label": "str"},
        "answers": {"id": "str", "answer": "str"},
    }
    errors: list[str] = []
    if not isinstance(value, list) or (kind != "answers" and not value):
        return [f"{name}: must be a non-empty list"]
    for i, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{name}[{i}]: must be an object")
            continue
        for key, sub in specs[kind].items():
            errors += _check_kind(f"{name}[{i}].{key}", sub, item.get(key))
    return errors


def validate_event_line(event) -> list[str]:
    """Errors for one event object (empty list = valid)."""
    if not isinstance(event, dict):
        return ["event: must be a JSON object"]
    errors: list[str] = []
    if not _valid_ts(event.get("ts")):
        errors.append("ts: must be an ISO 8601 UTC time, e.g. 2026-10-22T10:00:00Z")
    etype = event.get("type")
    if etype not in ALL_TYPES:
        errors.append(f"type: must be one of {', '.join(ALL_TYPES)}")
        etype = None
    for key in ("agent", "run_id"):
        if not _is_str(event.get(key)):
            errors.append(f"{key}: required text")
    if etype in EVENT_TABLE:
        spec = EVENT_TABLE[etype]
        for name, kind in spec["required"].items():
            errors += _check_kind(name, kind, event.get(name))
        for name, kind in spec["optional"].items():
            if name in event:
                errors += _check_kind(name, kind, event[name])
    elif etype in HOOK_TYPES:
        for name, kind in HOOK_TYPES[etype].items():
            errors += _check_kind(name, kind, event.get(name))
    return errors


def build_event(etype: str, run_id: str, fields: dict, agent: str | None = None, ts: str | None = None) -> dict:
    """Make an event dict (ts, type, agent, run_id, then the fields). Raises ValueError when invalid."""
    if etype in HOOK_TYPES:
        raise ValueError(f"type: {etype} is written by the hook, not by this script")
    if etype not in EVENT_TABLE:
        raise ValueError(f"type: must be one of {', '.join(EVENT_TABLE)}")
    spec = EVENT_TABLE[etype]
    who = agent or spec["agent"]
    event = {
        "ts": ts or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": etype,
        "agent": who,
        "run_id": run_id,
    }
    if etype == "approval_given" and "by" not in fields:
        fields = {**fields, "by": "terminal"}
    allowed = set(spec["required"]) | set(spec["optional"])
    for name, value in fields.items():
        if value is None:
            continue
        if name not in allowed:
            raise ValueError(f"{name}: not a field of {etype}")
        event[name] = value
    errors = validate_event_line(event)
    if errors:
        raise ValueError("; ".join(errors))
    return event


def write_event(log: Path, event: dict) -> str:
    line = json.dumps(event, ensure_ascii=False)
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    return line


# ---------- request / response checks (mirror scripts/agent_contract.py) ----------

def _str_list(obj, key, errors, non_empty=False):
    if key not in obj:
        errors.append(f"{key}: missing (list of text)")
        return
    v = obj[key]
    if not isinstance(v, list) or not all(_is_str(x) for x in v):
        errors.append(f"{key}: must be a list of non-blank text")
    elif non_empty and not v:
        errors.append(f"{key}: must not be empty")


def _dict_list(obj, key, fields, errors):
    if key not in obj:
        errors.append(f"{key}: missing (list)")
        return
    v = obj[key]
    if not isinstance(v, list):
        errors.append(f"{key}: must be a list")
        return
    for i, item in enumerate(v):
        if not isinstance(item, dict):
            errors.append(f"{key}[{i}]: must be an object")
            continue
        for name, kind in fields.items():
            val = item.get(name)
            if kind == "str" and not _is_str(val):
                errors.append(f"{key}[{i}].{name}: required text")
            elif kind == "bool" and not isinstance(val, bool):
                errors.append(f"{key}[{i}].{name}: must be true or false")
            elif kind == "strlist" and (
                not isinstance(val, list) or not val or not all(_is_str(x) for x in val)
            ):
                errors.append(f"{key}[{i}].{name}: must be a non-empty list of text")


def validate_request(obj) -> list[str]:
    if not isinstance(obj, dict):
        return ["request: must be a JSON object"]
    errors: list[str] = []
    if not _is_str(obj.get("goal")):
        errors.append("goal: required text")
    _str_list(obj, "context_files", errors)
    _str_list(obj, "constraints", errors)
    _str_list(obj, "done_when", errors, non_empty=True)
    return errors


def validate_response(obj) -> list[str]:
    if not isinstance(obj, dict):
        return ["response: must be a JSON object"]
    errors: list[str] = []
    status = obj.get("status")
    if status not in RESPONSE_STATUSES:
        errors.append(f"status: must be one of {', '.join(RESPONSE_STATUSES)}")
    if not _is_str(obj.get("summary")):
        errors.append("summary: required text")
    for key in ("files", "assumptions", "evidence"):
        _str_list(obj, key, errors)
    _dict_list(obj, "questions", {"id": "str", "question": "str", "why": "str"}, errors)
    _dict_list(
        obj,
        "approvals",
        {"id": "str", "decision": "str", "options": "strlist", "recommended": "str", "one_way_door": "bool"},
        errors,
    )
    if status == "done" and not obj.get("evidence"):
        errors.append("evidence: status done needs at least one piece of evidence")
    if status == "needs_answers" and not obj.get("questions"):
        errors.append("questions: status needs_answers needs at least one question")
    if status == "needs_approval" and not obj.get("approvals"):
        errors.append("approvals: status needs_approval needs at least one approval")
    return errors


# ---------- check-run ----------

_FILE_RE = re.compile(r"^(\d{2})-(.+)-(request|response)\.json$")


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig")), None
    except (OSError, ValueError) as e:
        return None, f"cannot read JSON ({e})"


def check_run(run_dir: Path, log: Path | None = None) -> tuple[list[str], list[str]]:
    """Return (problems, notes). notes: 'open run', pending approvals."""
    run_dir = Path(run_dir).resolve()
    run_id = run_dir.name
    problems: list[str] = []
    notes: list[str] = []
    if not run_dir.is_dir():
        return [f"run folder not found: {run_dir}"], notes
    if log is None:
        derived = run_dir.parent.parent.parent / DEFAULT_LOG
        log = derived if derived.is_file() or not DEFAULT_LOG.is_file() else DEFAULT_LOG
    log = Path(log)

    # events of this run
    events: list[dict] = []
    if not log.is_file():
        problems.append(f"event log not found: {log}")
    else:
        for n, raw in enumerate(log.read_text(encoding="utf-8-sig").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                ev = json.loads(raw)
            except ValueError:
                problems.append(f"event log line {n}: not valid JSON")
                continue
            if not isinstance(ev, dict) or ev.get("run_id") != run_id:
                if not isinstance(ev, dict):
                    problems.append(f"event log line {n}: not a JSON object")
                continue
            errs = validate_event_line(ev)
            for e in errs:
                problems.append(f"event log line {n} ({ev.get('type')}): {e}")
            events.append(ev)

    closed = any(e.get("type") == "run_finished" for e in events)

    if not (run_dir / "plan.md").is_file():
        problems.append("plan.md is missing")
    if closed:
        if not (run_dir / "summary.md").is_file():
            problems.append("summary.md is missing (the run has a run_finished event)")
    else:
        notes.append("open run (no run_finished event yet)")

    # request / response pairs
    files: dict[tuple[str, str], dict[str, Path]] = {}
    for f in sorted(run_dir.iterdir()):
        m = _FILE_RE.match(f.name)
        if m:
            files.setdefault((m.group(1), m.group(2)), {})[m.group(3)] = f
    responses_per_role: dict[str, int] = {}
    for (nn, role), pair in sorted(files.items()):
        req, res = pair.get("request"), pair.get("response")
        if req is None:
            problems.append(f"{nn}-{role}-request.json is missing (a response exists)")
        else:
            obj, err = _read_json(req)
            for e in [err] if err else validate_request(obj):
                problems.append(f"{req.name}: {e}")
        if res is None:
            if closed:
                problems.append(f"{nn}-{role}-response.json is missing (the run is closed)")
            else:
                notes.append(f"{nn}-{role}: waiting for the response")
        else:
            responses_per_role[role] = responses_per_role.get(role, 0) + 1
            obj, err = _read_json(res)
            for e in [err] if err else validate_response(obj):
                problems.append(f"{res.name}: {e}")

    # event log vs run folder
    if events:
        if events[0].get("type") != "run_started":
            problems.append("the first event of this run is not run_started")
    elif log.is_file():
        problems.append(f"the event log has no events for run {run_id}")
    if closed and events and events[-1].get("type") != "run_finished":
        problems.append("run_finished is not the last event of the run")
    for role, count in sorted(responses_per_role.items()):
        out = sum(1 for e in events if e.get("type") == "handoff" and e.get("to") == role)
        back = sum(1 for e in events if e.get("type") == "handoff" and e.get("from") == role)
        res = sum(1 for e in events if e.get("type") == "agent_result" and e.get("agent") == role)
        if out < count:
            problems.append(f"{role}: {count} response(s) but only {out} handoff event(s) to it")
        if back < count:
            problems.append(f"{role}: {count} response(s) but only {back} return handoff event(s) from it")
        if res < count:
            problems.append(f"{role}: {count} response(s) but only {res} agent_result event(s)")

    # approvals
    for i, ev in enumerate(events):
        if ev.get("type") == "approval_requested" and ev.get("id"):
            later = any(
                e.get("type") == "approval_given" and e.get("id") == ev["id"] for e in events[i + 1 :]
            )
            if not later:
                notes.append(f"pending approval: {ev['id']}")
    return problems, notes


# ---------- CLI ----------

def _json_arg(text: str, name: str):
    try:
        return json.loads(text)
    except ValueError as e:
        raise ValueError(f"{name}: not valid JSON ({e})")


def _bool_arg(text: str, name: str) -> bool:
    low = text.strip().lower()
    if low in ("true", "yes", "1"):
        return True
    if low in ("false", "no", "0"):
        return False
    raise ValueError(f"{name}: must be true or false")


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="team_event.py", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("event", help="validate and append one event line")
    e.add_argument("type")
    e.add_argument("--run-id", required=True)
    e.add_argument("--agent")
    e.add_argument("--log")
    e.add_argument("--project")
    for flag in (
        "goal", "size", "from", "to", "task", "status", "summary", "response-file", "id",
        "kind", "title", "why", "asked-agent", "decision", "option", "by", "reason",
    ):
        e.add_argument(f"--{flag}")
    for flag in ("questions-json", "options-json", "answers-json", "one-way-door"):
        e.add_argument(f"--{flag}")
    c = sub.add_parser("check-run", help="check a run folder and its event log")
    c.add_argument("run_dir")
    c.add_argument("--log")
    return p


def cmd_event(a) -> int:
    try:
        fields = {
            "goal": a.goal, "size": a.size, "from": a.from_, "to": a.to, "task": a.task,
            "status": a.status, "summary": a.summary, "response_file": a.response_file,
            "id": a.id, "kind": a.kind, "title": a.title, "why": a.why,
            "asked_agent": a.asked_agent, "decision": a.decision, "option": a.option,
            "by": a.by, "reason": a.reason,
        }
        if a.questions_json is not None:
            fields["questions"] = _json_arg(a.questions_json, "--questions-json")
        if a.options_json is not None:
            fields["options"] = _json_arg(a.options_json, "--options-json")
        if a.answers_json is not None:
            fields["answers"] = _json_arg(a.answers_json, "--answers-json")
        if a.one_way_door is not None:
            fields["one_way_door"] = _bool_arg(a.one_way_door, "--one-way-door")
        event = build_event(a.type, a.run_id, fields, agent=a.agent)
    except ValueError as e:
        print(f"refused, nothing written: {e}", file=sys.stderr)
        return 2
    if a.log:
        log = Path(a.log)
    else:
        log = Path(a.project or ".") / DEFAULT_LOG
    print(write_event(log, event))
    return 0


def cmd_check(a) -> int:
    problems, notes = check_run(Path(a.run_dir), Path(a.log) if a.log else None)
    print("PROBLEMS" if problems else "OK")
    for line in problems:
        print(f"- {line}")
    for line in notes:
        print(f"note: {line}")
    return 1 if problems else 0


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    args = _parser().parse_args(argv)
    if args.cmd == "event":
        # argparse turns --from into attribute `from`; expose it as from_
        args.from_ = getattr(args, "from")
        return cmd_event(args)
    return cmd_check(args)


if __name__ == "__main__":
    sys.exit(main())
