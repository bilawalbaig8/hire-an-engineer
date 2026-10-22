"""Claude Code hook: turn a hook payload (JSON on stdin) into one event line.

Appends to .agents/events.jsonl inside the project folder. Never fails the
host: exit code is always 0 and problems go to stderr only.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agent_contract  # noqa: E402

LOG_PATH = Path(".agents") / "events.jsonl"


def _text(value) -> str:
    return value if isinstance(value, str) and value.strip() else ""


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _relative_path(file_path: str, project_dir: str) -> str:
    """Path relative to the project, or "" when the file is outside it."""
    try:
        rel = Path(file_path).resolve().relative_to(Path(project_dir).resolve())
    except (ValueError, OSError):
        return ""
    return rel.as_posix()


def event_from_hook(payload: dict) -> dict | None:
    if not isinstance(payload, dict):
        return None
    run_id = _text(payload.get("session_id"))
    name = payload.get("hook_event_name")
    if not run_id:
        return None
    event = {"ts": _now(), "run_id": run_id}
    if name in ("SubagentStart", "SubagentStop"):
        agent = _text(payload.get("agent_type"))
        if not agent:
            return None
        event["type"] = "agent_start" if name == "SubagentStart" else "agent_stop"
        event["agent"] = agent
        return event
    if name == "PostToolUse" and payload.get("tool_name") in ("Write", "Edit"):
        tool_input = payload.get("tool_input")
        file_path = _text(tool_input.get("file_path")) if isinstance(tool_input, dict) else ""
        if not file_path:
            return None
        project_dir = (_text(os.environ.get("CLAUDE_PROJECT_DIR"))
                       or _text(payload.get("cwd")) or os.getcwd())
        rel = _relative_path(file_path, project_dir)
        if not rel:
            return None
        event.update(type="file_written", agent=_text(payload.get("agent_type")) or "main", path=rel)
        return event
    return None


def project_dir_for(payload: dict) -> Path:
    return Path(_text(os.environ.get("CLAUDE_PROJECT_DIR"))
                or _text(payload.get("cwd")) or os.getcwd())


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read())
        event = event_from_hook(payload)
        if event is not None:
            agent_contract.append_event(project_dir_for(payload) / LOG_PATH, event)
    except Exception as exc:  # never break the host session
        print(f"log_event: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
