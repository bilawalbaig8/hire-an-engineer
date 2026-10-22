#!/usr/bin/env python3
"""Local server behind the virtual office window.

Serves the office UI from docs/agents/visual-office/ and streams the project's .agents/events.jsonl to it.
Binds 127.0.0.1 only.

  GET  /          the built UI (index.html) if present, else mock-v2.html; other static files by path
  GET  /events    Server-Sent Events: replays events.jsonl, then follows appended lines
  GET  /roster    JSON list of {name, skill, model, owns} from docs/agents/roster.md
  GET  /state     JSON {events: N, pending_approvals: [...]}
  POST /answer    JSON {id, answer, kind} -> one line appended to .team/inbox.jsonl

Usage: python scripts/office_server.py [--project DIR] [--port N] [--no-open]
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import threading
import time
import webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_roster import _rows  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
HOST = "127.0.0.1"
DEFAULT_PORT = 8765
MAX_BODY = 64 * 1024
POLL_SECONDS = 0.3
EVENTS_PATH = Path(".agents") / "events.jsonl"
INBOX_PATH = Path(".team") / "inbox.jsonl"
UI_DIR = Path("docs") / "agents" / "visual-office"
ROSTER_PATH = Path("docs") / "agents" / "roster.md"


def _parse_line(line: bytes) -> dict | list | None:
    """The JSON object or array on a line, or None when it is not valid JSON."""
    try:
        value = json.loads(line.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    return value if isinstance(value, (dict, list)) else None


class Tail:
    """Follow a JSON-lines file: complete lines only, survives a missing or truncated file."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.offset = 0
        self.pending = b""

    def read_new(self) -> list[bytes]:
        """New valid JSON lines (as raw bytes, no newline) since the last call."""
        try:
            size = self.path.stat().st_size
        except OSError:
            self.offset, self.pending = 0, b""
            return []
        if size < self.offset:  # truncated or replaced: start again
            self.offset, self.pending = 0, b""
        if size == self.offset and not self.pending:
            return []
        try:
            with open(self.path, "rb") as f:
                f.seek(self.offset)
                chunk = f.read(max(0, size - self.offset))
        except OSError:
            return []
        self.offset += len(chunk)
        data = self.pending + chunk
        *lines, rest = data.split(b"\n")
        # A last line without a newline counts only if it is already a complete object.
        if rest.strip() and _parse_line(rest) is not None and rest.lstrip().startswith((b"{", b"[")):
            lines.append(rest)
            rest = b""
        self.pending = rest
        return [ln.strip() for ln in lines if ln.strip() and _parse_line(ln) is not None]


def read_events(path: Path) -> list[dict]:
    """All valid event objects in the file."""
    try:
        data = path.read_bytes()
    except OSError:
        return []
    events = []
    for line in data.split(b"\n"):
        value = _parse_line(line.strip()) if line.strip() else None
        if isinstance(value, dict):
            events.append(value)
    return events


def pending_approvals(events: list[dict]) -> list[dict]:
    """approval_requested events with no later approval_given for the same approval_id."""
    pending: dict[object, dict] = {}
    for ev in events:
        aid = ev.get("approval_id")
        if aid is None:
            continue
        if ev.get("type") == "approval_requested":
            pending[aid] = ev
        elif ev.get("type") == "approval_given":
            pending.pop(aid, None)
    return list(pending.values())


def load_roster(path: Path) -> list[dict[str, str]]:
    try:
        rows = _rows(path.read_text(encoding="utf-8-sig"))
    except OSError:
        return []
    return [dict(zip(("name", "skill", "model", "owns"), r)) for r in rows or [] if len(r) == 4]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class OfficeServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address, handler, project: Path, repo_root: Path) -> None:
        super().__init__(address, handler)
        self.project = Path(project)
        self.repo_root = Path(repo_root)
        self.ui_dir = (self.repo_root / UI_DIR).resolve()
        self.stopping = threading.Event()

    def shutdown(self) -> None:
        self.stopping.set()
        super().shutdown()

    @property
    def port(self) -> int:
        return self.server_address[1]


class Handler(BaseHTTPRequestHandler):
    server: OfficeServer
    protocol_version = "HTTP/1.1"

    def log_message(self, format: str, *args) -> None:  # noqa: A002 - keep the console quiet
        pass

    # --- helpers
    def _send(self, status: int, body: bytes, ctype: str = "application/json", close: bool = False) -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if close:
            self.send_header("Connection", "close")
            self.close_connection = True
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, value) -> None:
        self._send(status, json.dumps(value).encode("utf-8"))

    def _drain(self) -> None:
        """Discard an unread request body (up to 1 MB) so the client gets our reply, not a reset."""
        try:
            left = min(int(self.headers.get("Content-Length", "0")), 1024 * 1024)
            while left > 0:
                chunk = self.rfile.read(min(left, 65536))
                if not chunk:
                    break
                left -= len(chunk)
        except (ValueError, OSError):
            pass

    def _allowed(self) -> bool:
        port = self.server.port
        allowed = {f"http://127.0.0.1:{port}", f"http://localhost:{port}"}
        origin = self.headers.get("Origin")
        if origin is not None and origin not in allowed:
            return False
        host = self.headers.get("Host")
        return host is None or host in {f"127.0.0.1:{port}", f"localhost:{port}"}

    # --- routes
    def do_GET(self) -> None:  # noqa: N802
        if not self._allowed():
            return self._json(403, {"error": "forbidden origin"})
        path = urlsplit(self.path).path
        if path == "/events":
            return self._events()
        if path == "/roster":
            return self._json(200, load_roster(self.server.repo_root / ROSTER_PATH))
        if path == "/state":
            events = read_events(self.server.project / EVENTS_PATH)
            return self._json(200, {"events": len(events), "pending_approvals": pending_approvals(events)})
        self._static(path)

    def _static(self, path: str) -> None:
        root = self.server.ui_dir
        rel = unquote(path)
        if "\x00" in rel or "\\" in rel:
            return self._json(403, {"error": "forbidden"})
        if rel in ("", "/"):
            target = root / "index.html"
            if not target.is_file():
                target = root / "mock-v2.html"
        else:
            target = (root / rel.lstrip("/")).resolve()
            if target != root and root not in target.parents:
                return self._json(403, {"error": "forbidden"})
        if not target.is_file():
            return self._json(404, {"error": "not found"})
        ctype = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript", "application/json"):
            ctype += "; charset=utf-8"
        self._send(200, target.read_bytes(), ctype)

    def _events(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True
        tail = Tail(self.server.project / EVENTS_PATH)
        idle = 0.0
        try:
            while not self.server.stopping.is_set():
                lines = tail.read_new()
                for line in lines:
                    self.wfile.write(b"data: " + line + b"\n\n")
                if lines:
                    idle = 0.0
                elif idle >= 15:  # keep-alive comment; also detects a closed client
                    self.wfile.write(b": keep-alive\n\n")
                    idle = 0.0
                self.wfile.flush()
                time.sleep(POLL_SECONDS)
                idle += POLL_SECONDS
        except (OSError, ValueError):
            pass  # client went away

    def do_POST(self) -> None:  # noqa: N802
        if not self._allowed():
            self._drain()
            return self._send(403, b'{"error": "forbidden origin"}', close=True)
        if urlsplit(self.path).path != "/answer":
            self._drain()
            return self._send(404, b'{"error": "not found"}', close=True)
        try:
            length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            return self._send(400, b'{"error": "content-length required"}', close=True)
        if length < 0 or length > MAX_BODY:
            self._drain()
            return self._send(400, b'{"error": "body too large"}', close=True)
        body = _parse_line(self.rfile.read(length))
        if not isinstance(body, dict):
            return self._send(400, b'{"error": "body must be a JSON object"}')
        ident, answer = body.get("id"), body.get("answer")
        if ident in (None, "") or answer is None or answer == "":
            return self._send(400, b'{"error": "id and answer are required"}')
        kind = body.get("kind", "question")
        if kind not in ("question", "approval"):
            return self._send(400, b'{"error": "kind must be question or approval"}')
        entry = {"ts": _now(), "id": ident, "answer": answer, "kind": kind, "source": "window"}
        inbox = self.server.project / INBOX_PATH
        try:
            inbox.parent.mkdir(parents=True, exist_ok=True)
            with open(inbox, "a", encoding="utf-8", newline="") as f:
                f.write(json.dumps(entry) + "\n")
        except OSError as e:
            return self._json(500, {"error": f"cannot write inbox: {e}"})
        self._json(200, {"ok": True})


def make_server(project: Path, host: str = HOST, port: int = DEFAULT_PORT,
                repo_root: Path | None = None) -> OfficeServer:
    if host != HOST:
        raise ValueError(f"the office server binds {HOST} only, not {host}")
    return OfficeServer((host, port), Handler, project, repo_root or REPO_ROOT)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve the virtual office window.")
    parser.add_argument("--project", default=".", help="project folder holding .agents/ and .team/ (default: .)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-open", action="store_true", help="do not open the browser")
    args = parser.parse_args(argv)
    try:
        server = make_server(Path(args.project).resolve(), port=args.port)
    except OSError as e:
        print(f"cannot start on {HOST}:{args.port}: {e}", file=sys.stderr)
        return 1
    url = f"http://{HOST}:{server.port}/"
    print(f"Virtual office at {url}  (project: {Path(args.project).resolve()}; Ctrl+C to stop)")
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stopping.set()
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
