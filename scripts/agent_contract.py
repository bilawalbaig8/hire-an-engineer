#!/usr/bin/env python3
"""Handoff contract between the boss agent and a specialist agent.

Hand-written checks only (no dependencies). Each validate_* function returns
a list of error strings; an empty list means valid.

CLI: python scripts/agent_contract.py check-request|check-response|check-event FILE
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

RESPONSE_STATUSES = ("done", "needs_answers", "needs_approval", "blocked")
EVENT_TYPES = (
    "agent_start",
    "agent_stop",
    "handoff",
    "file_written",
    "approval_requested",
    "approval_given",
)


def _is_str(v):
    return isinstance(v, str) and v.strip() != ""


def _str_list(obj, key, errors, required=True, non_empty=False):
    if key not in obj:
        if required:
            errors.append(f"{key}: missing (list of text)")
        return
    v = obj[key]
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        errors.append(f"{key}: must be a list of text")
    elif non_empty and not v:
        errors.append(f"{key}: must not be empty")


def _list_of_dicts(obj, key, fields, errors, required=False):
    if key not in obj:
        if required:
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
                not isinstance(val, list) or not val or not all(isinstance(x, str) for x in val)
            ):
                errors.append(f"{key}[{i}].{name}: must be a non-empty list of text")


def validate_request(obj: dict) -> list[str]:
    if not isinstance(obj, dict):
        return ["request: must be a JSON object"]
    errors = []
    if not _is_str(obj.get("goal")):
        errors.append("goal: required text")
    _str_list(obj, "context_files", errors)
    _str_list(obj, "constraints", errors)
    _str_list(obj, "done_when", errors, non_empty=True)
    if "mode" in obj and not _is_str(obj["mode"]):
        errors.append("mode: must be text")
    if "answers" in obj:
        _list_of_dicts(obj, "answers", {"id": "str", "answer": "str"}, errors)
    return errors


def validate_response(obj: dict) -> list[str]:
    if not isinstance(obj, dict):
        return ["response: must be a JSON object"]
    errors = []
    status = obj.get("status")
    if status not in RESPONSE_STATUSES:
        errors.append(f"status: must be one of {', '.join(RESPONSE_STATUSES)}")
    if not _is_str(obj.get("summary")):
        errors.append("summary: required text")
    for key in ("files", "assumptions", "evidence"):
        _str_list(obj, key, errors)
    _list_of_dicts(obj, "questions", {"id": "str", "question": "str", "why": "str"}, errors, required=True)
    _list_of_dicts(
        obj,
        "approvals",
        {
            "id": "str",
            "decision": "str",
            "options": "strlist",
            "recommended": "str",
            "one_way_door": "bool",
        },
        errors,
        required=True,
    )
    if status == "done" and not obj.get("evidence"):
        errors.append("evidence: status done needs at least one piece of evidence")
    if status == "needs_answers" and not obj.get("questions"):
        errors.append("questions: status needs_answers needs at least one question")
    if status == "needs_approval" and not obj.get("approvals"):
        errors.append("approvals: status needs_approval needs at least one approval")
    return errors


def _valid_ts(ts):
    if not isinstance(ts, str) or not re.search(r"(Z|[+-]00:?00)$", ts):
        return False
    try:
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def validate_event(obj: dict) -> list[str]:
    if not isinstance(obj, dict):
        return ["event: must be a JSON object"]
    errors = []
    if not _valid_ts(obj.get("ts")):
        errors.append("ts: must be an ISO 8601 UTC time, e.g. 2026-10-22T10:00:00Z")
    etype = obj.get("type")
    if etype not in EVENT_TYPES:
        errors.append(f"type: must be one of {', '.join(EVENT_TYPES)}")
    for key in ("agent", "run_id"):
        if not _is_str(obj.get(key)):
            errors.append(f"{key}: required text")
    if etype == "file_written" and not _is_str(obj.get("path")):
        errors.append("path: required for file_written")
    if etype == "handoff":
        for key in ("from", "to"):
            if not _is_str(obj.get(key)):
                errors.append(f"{key}: required for handoff")
    return errors


def append_event(path: Path, event: dict) -> None:
    errors = validate_event(event)
    if errors:
        raise ValueError("invalid event: " + "; ".join(errors))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


_CHECKS = {
    "check-request": validate_request,
    "check-response": validate_response,
    "check-event": validate_event,
}


def main(argv):
    if len(argv) != 3 or argv[1] not in _CHECKS:
        print("usage: agent_contract.py check-request|check-response|check-event FILE")
        return 2
    try:
        obj = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"cannot read JSON from {argv[2]}: {e}")
        return 1
    errors = _CHECKS[argv[1]](obj)
    for e in errors:
        print(e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
