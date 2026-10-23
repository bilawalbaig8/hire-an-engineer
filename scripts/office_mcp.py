#!/usr/bin/env python3
"""Local MCP server (stdio) that hands the boss the owner's answers from the office window.

The office window (scripts/office_server.py, POST /answer) appends one JSON line per answer
to <project>/.team/inbox.jsonl: {ts, id, answer, kind, source: "window", optional decision,
option, answers, text, run_id}. This server lets a running Claude Code session wait for such
a line with an MCP tool call:

  wait_for_owner_answer {id, timeout_seconds=600 (max 3500)}
      -> the newest unconsumed line with that id, or a "no_answer" result on timeout.
  pending_window_answers {}
      -> every unconsumed line (does not consume), for the next-turn fallback.

Returned lines are recorded in <project>/.team/inbox.consumed (JSON lines {id, ts, sha, at}),
so an answer is handed out once; a newer line with the same id is handed out again.

Transport: MCP stdio, JSON-RPC 2.0, one message per line, UTF-8. Python stdlib only.
stdout carries protocol messages only; diagnostics go to stderr (and OFFICE_MCP_LOG if set).

Project folder: --project, else $CLAUDE_PROJECT_DIR, else the current folder.
"""
import argparse
import hashlib
import json
import os
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

SERVER_NAME = "office"
SERVER_VERSION = "0.1.0"
SUPPORTED_VERSIONS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")  # newest first
INBOX_REL = Path(".team") / "inbox.jsonl"
CONSUMED_REL = Path(".team") / "inbox.consumed"
DEFAULT_TIMEOUT = 600
MAX_TIMEOUT = 3500
PROGRESS_EVERY = 20.0  # seconds between progress notifications, when the client asked for them
RESULT_KEYS = ("id", "answer", "kind", "decision", "option", "answers", "text", "source", "ts", "run_id")

PARSE_ERROR, INVALID_REQUEST, METHOD_NOT_FOUND, INVALID_PARAMS, INTERNAL_ERROR = (
    -32700, -32600, -32601, -32602, -32603)

WAIT_TOOL = {
    "name": "wait_for_owner_answer",
    "title": "Wait for the owner's answer in the office window",
    "description": (
        "Wait until the owner answers a question or approval in the office window, then return "
        "that answer. Use the same id you logged with question_asked or approval_requested. "
        "Returns JSON: status 'answered' with id, answer, kind, decision, option, answers, text, "
        "source; or status 'no_answer' when the time runs out (not an error). An answer typed in "
        "the chat interrupts this wait. timeout_seconds 0 only checks once."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "id": {"type": "string", "minLength": 1,
                   "description": "The question or approval id, e.g. q-01 or a-01."},
            "timeout_seconds": {"type": "number", "minimum": 0, "maximum": MAX_TIMEOUT,
                                "default": DEFAULT_TIMEOUT,
                                "description": "How long to wait, in seconds."},
        },
        "required": ["id"],
        "additionalProperties": False,
    },
}
PENDING_TOOL = {
    "name": "pending_window_answers",
    "title": "List unread office window answers",
    "description": (
        "List the answers the owner gave in the office window that have not been handed out yet. "
        "Does not mark them as read; call wait_for_owner_answer with the id and timeout_seconds 0 "
        "to take one."),
    "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
}
TOOLS = (WAIT_TOOL, PENDING_TOOL)


class RpcError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code, self.message = code, message


def log(msg: str) -> None:
    line = f"[office_mcp] {msg}"
    try:
        print(line, file=sys.stderr, flush=True)
    except (OSError, ValueError):
        pass
    path = os.environ.get("OFFICE_MCP_LOG")
    if path:
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"{_now()} {line}\n")
        except OSError:
            pass


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def negotiate(requested) -> str:
    """The client's version if supported, otherwise the newest this server speaks."""
    return requested if requested in SUPPORTED_VERSIONS else SUPPORTED_VERSIONS[0]


def parse_timeout(value) -> float:
    if value is None:
        return float(DEFAULT_TIMEOUT)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value != value or value < 0:
        raise RpcError(INVALID_PARAMS, "timeout_seconds must be a number >= 0")
    return float(min(value, MAX_TIMEOUT))


# --- inbox ---------------------------------------------------------------------------

def read_inbox(project: Path) -> list:
    """Complete, valid answer lines in file order: [(sha, entry)]. A last line without a
    newline is still being written and is skipped."""
    try:
        data = (project / INBOX_REL).read_bytes()
    except OSError:
        return []
    out = []
    for raw in data.split(b"\n")[:-1]:
        raw = raw.strip()
        if not raw:
            continue
        try:
            entry = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            continue
        if not isinstance(entry, dict):
            continue
        ident, answer = entry.get("id"), entry.get("answer")
        if not isinstance(ident, str) or not ident or answer is None or answer == "":
            continue
        out.append((hashlib.sha256(raw).hexdigest(), entry))
    return out


def read_consumed(project: Path) -> tuple:
    """(set of consumed line hashes, {id: newest consumed ts})."""
    shas, newest = set(), {}
    try:
        data = (project / CONSUMED_REL).read_bytes()
    except OSError:
        return shas, newest
    for raw in data.split(b"\n"):
        try:
            rec = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            continue
        if not isinstance(rec, dict):
            continue
        if isinstance(rec.get("sha"), str):
            shas.add(rec["sha"])
        ident, ts = rec.get("id"), rec.get("ts")
        if isinstance(ident, str) and isinstance(ts, str) and ts > newest.get(ident, ""):
            newest[ident] = ts
    return shas, newest


def pending(project: Path) -> list:
    """Unconsumed lines: not handed out before and not older than one already handed out."""
    shas, newest = read_consumed(project)
    out = []
    for sha, entry in read_inbox(project):
        ts = entry.get("ts") if isinstance(entry.get("ts"), str) else ""
        if sha in shas or ts < newest.get(entry["id"], ""):
            continue
        out.append((sha, entry))
    return out


_inbox_lock = threading.Lock()


def take(project: Path, ident: str):
    """The newest unconsumed line for ident, marking it and any older pending ones consumed."""
    with _inbox_lock:
        mine = [(sha, e) for sha, e in pending(project) if e["id"] == ident]
        if not mine:
            return None
        path = project / CONSUMED_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        at = _now()
        with open(path, "a", encoding="utf-8", newline="") as f:
            for sha, e in mine:
                ts = e.get("ts") if isinstance(e.get("ts"), str) else ""
                f.write(json.dumps({"id": ident, "ts": ts, "sha": sha, "at": at}) + "\n")
        return mine[-1][1]


def shape(entry: dict, status: str = "answered") -> dict:
    out = {"status": status}
    for key in RESULT_KEYS:
        if key != "run_id" or key in entry:
            out[key] = entry.get(key)
    return out


def text_result(payload: dict) -> dict:
    return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
            "isError": False}


# --- server --------------------------------------------------------------------------

class Server:
    def __init__(self, project: Path, out=None, poll: float = 0.5):
        self.project = project
        self.out = out or sys.stdout.buffer
        self.poll = poll
        self.write_lock = threading.Lock()
        self.active = {}  # json(request id) -> threading.Event (set = cancelled)
        self.active_lock = threading.Lock()

    def send(self, msg: dict) -> None:
        data = json.dumps(msg, ensure_ascii=True).encode("ascii") + b"\n"
        with self.write_lock:
            try:
                self.out.write(data)
                self.out.flush()
            except (OSError, ValueError):
                pass

    def reply(self, msg_id, result=None, error: RpcError | None = None) -> None:
        msg = {"jsonrpc": "2.0", "id": msg_id}
        if error is not None:
            msg["error"] = {"code": error.code, "message": error.message}
        else:
            msg["result"] = result
        self.send(msg)

    # one incoming line
    def handle_line(self, raw: bytes) -> None:
        text = raw.decode("utf-8", errors="replace").strip()
        if not text:
            return
        try:
            msg = json.loads(text)
        except ValueError:
            return self.reply(None, error=RpcError(PARSE_ERROR, "parse error"))
        if not isinstance(msg, dict):
            return self.reply(None, error=RpcError(INVALID_REQUEST, "a message must be one JSON object"))
        has_id = "id" in msg
        msg_id = msg.get("id")
        if has_id and (isinstance(msg_id, bool) or not isinstance(msg_id, (str, int))):
            return self.reply(None, error=RpcError(INVALID_REQUEST, "id must be a string or integer"))
        method = msg.get("method")
        if method is None and ("result" in msg or "error" in msg):
            return  # a response to a request we never send; ignore
        if msg.get("jsonrpc") != "2.0" or not isinstance(method, str):
            if has_id:
                self.reply(msg_id, error=RpcError(INVALID_REQUEST, "jsonrpc must be 2.0 and method a string"))
            return
        params = msg.get("params")
        if not has_id:
            return self.notification(method, params)
        try:
            self.request(msg_id, method, params)
        except RpcError as e:
            self.reply(msg_id, error=e)
        except Exception as e:  # never die on one bad request
            log(f"internal error in {method}: {e!r}")
            self.reply(msg_id, error=RpcError(INTERNAL_ERROR, "internal error"))

    def notification(self, method: str, params) -> None:
        if method == "notifications/cancelled" and isinstance(params, dict):
            key = json.dumps(params.get("requestId"))
            with self.active_lock:
                ev = self.active.get(key)
            if ev is not None:
                ev.set()
                log(f"cancelled request {key}")
        # notifications/initialized and anything else: nothing to do

    def request(self, msg_id, method: str, params) -> None:
        if method == "initialize":
            requested = params.get("protocolVersion") if isinstance(params, dict) else None
            version = negotiate(requested)
            log(f"initialize: client asked {requested!r}, using {version}; project {self.project}")
            return self.reply(msg_id, {
                "protocolVersion": version,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "instructions": "Hands the boss the owner's answers from the office window "
                                "(.team/inbox.jsonl).",
            })
        if method == "ping":
            return self.reply(msg_id, {})
        if method == "tools/list":
            return self.reply(msg_id, {"tools": list(TOOLS)})
        if method == "tools/call":
            return self.tools_call(msg_id, params)
        raise RpcError(METHOD_NOT_FOUND, f"method not found: {method}")

    def tools_call(self, msg_id, params) -> None:
        if not isinstance(params, dict):
            raise RpcError(INVALID_PARAMS, "params must be an object")
        name, args = params.get("name"), params.get("arguments", {})
        if args is None:
            args = {}
        if not isinstance(args, dict):
            raise RpcError(INVALID_PARAMS, "arguments must be an object")
        if name == PENDING_TOOL["name"]:
            items = [shape(e, "pending") for _, e in pending(self.project)]
            return self.reply(msg_id, text_result({"pending": items, "count": len(items)}))
        if name != WAIT_TOOL["name"]:
            raise RpcError(INVALID_PARAMS, f"unknown tool: {name!r}")
        ident = args.get("id")
        if not isinstance(ident, str) or not ident.strip():
            raise RpcError(INVALID_PARAMS, "id must be a non-empty string")
        timeout = parse_timeout(args.get("timeout_seconds"))
        meta = params.get("_meta")
        token = meta.get("progressToken") if isinstance(meta, dict) else None
        key = json.dumps(msg_id)
        cancel = threading.Event()
        with self.active_lock:
            self.active[key] = cancel
        threading.Thread(target=self._wait, args=(msg_id, key, ident.strip(), timeout, token, cancel),
                         daemon=True).start()

    def _wait(self, msg_id, key, ident, timeout, token, cancel) -> None:
        try:
            start = time.monotonic()
            next_progress = start + PROGRESS_EVERY
            while not cancel.is_set():
                try:
                    entry = take(self.project, ident)
                except OSError as e:
                    log(f"cannot read or mark inbox: {e}")
                    entry = None
                if cancel.is_set():
                    return
                if entry is not None:
                    return self.reply(msg_id, text_result(shape(entry)))
                now = time.monotonic()
                if now - start >= timeout:
                    waited = round(now - start)
                    return self.reply(msg_id, text_result({
                        "status": "no_answer", "id": ident, "waited_seconds": waited,
                        "message": f"No answer in the office window for {ident} after {waited} s. "
                                   "The owner may still answer in the chat or the window; ask again "
                                   "or call this tool again."}))
                if token is not None and now >= next_progress:
                    next_progress = now + PROGRESS_EVERY
                    self.send({"jsonrpc": "2.0", "method": "notifications/progress",
                               "params": {"progressToken": token, "progress": round(now - start),
                                          "total": timeout, "message": "waiting for the owner"}})
                cancel.wait(min(self.poll, max(0.0, timeout - (now - start))))
        except Exception as e:
            log(f"wait for {ident} failed: {e!r}")
            if not cancel.is_set():
                self.reply(msg_id, error=RpcError(INTERNAL_ERROR, "internal error while waiting"))
        finally:
            with self.active_lock:
                self.active.pop(key, None)

    def serve(self, inp=None) -> int:
        inp = inp or sys.stdin.buffer
        while True:
            try:
                raw = inp.readline()
            except (OSError, ValueError):
                break
            if not raw:
                break
            self.handle_line(raw)
        with self.active_lock:
            for ev in self.active.values():
                ev.set()
        log("stdin closed, exiting")
        return 0


def pick_project(flag: str | None) -> Path:
    if flag:
        return Path(flag).resolve()
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()
    return Path.cwd().resolve()


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description="MCP stdio server: owner answers from the office window.")
    parser.add_argument("--project", help="project folder (default: $CLAUDE_PROJECT_DIR or the current folder)")
    args = parser.parse_args(argv)
    try:
        poll = float(os.environ.get("OFFICE_MCP_POLL_SECONDS", "0.5"))
    except ValueError:
        poll = 0.5
    server = Server(pick_project(args.project), poll=max(0.01, poll))
    log(f"started, project {server.project}")
    return server.serve()


if __name__ == "__main__":
    sys.exit(main())
