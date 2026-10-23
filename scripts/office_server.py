#!/usr/bin/env python3
"""Local server behind the virtual office window.

Serves the office UI from docs/agents/visual-office/ and streams the project's .agents/events.jsonl to it.
Binds 127.0.0.1 only.

  GET  /          the built UI (index.html) if present, else mock-v2.html; other static files by path
  GET  /events    Server-Sent Events: replays events.jsonl, then follows appended lines
  GET  /roster    JSON list of {name, skill, model, owns} from docs/agents/roster.md
  GET  /state     JSON {events: N, pending_approvals: [...]}
  POST /answer    JSON {id, answer, kind} -> one line appended to .team/inbox.jsonl

Installed outside the repo (scripts/install_office.py puts it in <project>/.agents/office/): the UI is read from
ui/ next to this script, and the roster from --roster, else <project>/docs/agents/roster.md, else roster.md next
to this script, else built from the names in <project>/.claude/agents/*.md.

Usage: python scripts/office_server.py [--project DIR] [--port N] [--no-open] [--roster FILE]
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import re
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
ANSWER_EXTRA_KEYS = ("decision", "option", "answers", "text", "run_id")  # structured fields the window may add
UI_DIR = Path("docs") / "agents" / "visual-office"
ROSTER_PATH = Path("docs") / "agents" / "roster.md"
SCRIPT_DIR = Path(__file__).resolve().parent
AGENTS_DIR = Path(".claude") / "agents"


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
    """approval_requested events with no later approval_given for the same id (`id`, or the older `approval_id`)."""
    pending: dict[object, dict] = {}
    for ev in events:
        if ev.get("type") not in ("approval_requested", "approval_given"):
            continue
        aid = ev.get("id", ev.get("approval_id"))
        if aid is None:
            continue
        if ev.get("type") == "approval_requested":
            pending[aid] = ev
        elif ev.get("type") == "approval_given":
            pending.pop(aid, None)
    return list(pending.values())


TRUTH_LIMIT = 1000


def written_files_truth(project: Path, events: list[dict]) -> dict:
    """Which files the log says were written no longer exist on disk? Only project-relative paths are checked."""
    root = Path(project).resolve()
    seen: list[str] = []
    for ev in events:
        if ev.get("type") != "file_written":
            continue
        rel = ev.get("path")
        if not isinstance(rel, str) or not rel or rel.startswith(("/", "\\")) or (len(rel) > 1 and rel[1] == ":") or ".." in Path(rel).parts:
            continue
        if rel not in seen:
            seen.append(rel)
    seen = seen[-TRUTH_LIMIT:]
    missing = []
    for rel in seen:
        try:
            target = (root / rel).resolve()
            inside = root == target or root in target.parents
            if inside and not target.exists():
                missing.append(rel)
        except OSError:
            missing.append(rel)
    return {"checked": len(seen), "missing": missing, "events": len(events)}


def load_roster(path: Path) -> list[dict[str, str]]:
    try:
        rows = _rows(path.read_text(encoding="utf-8-sig"))
    except OSError:
        return []
    return [dict(zip(("name", "skill", "model", "owns"), r)) for r in rows or [] if len(r) == 4]


def roster_from_agents(agents_dir: Path) -> list[dict[str, str]]:
    """Fallback roster: one row per agent file's frontmatter (name, skill, model); the boss is left out."""
    rows = []
    for f in sorted(agents_dir.glob("*.md")) if agents_dir.is_dir() else []:
        try:
            text = f.read_text(encoding="utf-8-sig")
        except OSError:
            continue
        head = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
        if not head:
            continue
        fields = dict(re.findall(r"^(name|skill|model):\s*(.+?)\s*$", head.group(1), re.M))
        name = fields.get("name", "").strip("\"'")
        if name and name != "orchestrator":
            rows.append({"name": name, "skill": fields.get("skill", "").strip("\"'"),
                         "model": fields.get("model", "").strip("\"'"), "owns": ""})
    return rows


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class OfficeServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address, handler, project: Path, repo_root: Path,
                 ui_dir: Path | None = None, roster_path: Path | None = None,
                 answers_enabled: bool = False) -> None:
        super().__init__(address, handler)
        self.answers_enabled = answers_enabled
        self.project = Path(project)
        self.repo_root = Path(repo_root)
        if ui_dir is None:
            ui_dir = self.repo_root / UI_DIR
            if not ui_dir.is_dir() and (SCRIPT_DIR / "ui").is_dir():  # installed copy
                ui_dir = SCRIPT_DIR / "ui"
        self.ui_dir = Path(ui_dir).resolve()
        self.roster_path = Path(roster_path) if roster_path else None
        self.stopping = threading.Event()

    def roster(self) -> list[dict[str, str]]:
        for path in (self.roster_path, self.repo_root / ROSTER_PATH,
                     self.project / ROSTER_PATH, SCRIPT_DIR / "roster.md"):
            if path is not None and path.is_file():
                return load_roster(path)
        return roster_from_agents(self.project / AGENTS_DIR)

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
            return self._json(200, self.server.roster())
        if path == "/state":
            events = read_events(self.server.project / EVENTS_PATH)
            return self._json(200, {"events": len(events), "pending_approvals": pending_approvals(events)})
        if path == "/truth":
            return self._json(200, written_files_truth(self.server.project, read_events(self.server.project / EVENTS_PATH)))
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
        if not self.server.answers_enabled:
            self._drain()
            return self._send(404, b'{"error": "answers are switched off; start the server with --enable-answers"}', close=True)
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
        for key in ANSWER_EXTRA_KEYS:
            if key in body:
                entry[key] = body[key]
        inbox = self.server.project / INBOX_PATH
        try:
            inbox.parent.mkdir(parents=True, exist_ok=True)
            with open(inbox, "a", encoding="utf-8", newline="") as f:
                f.write(json.dumps(entry) + "\n")
        except OSError as e:
            return self._json(500, {"error": f"cannot write inbox: {e}"})
        self._json(200, {"ok": True})


def make_server(project: Path, host: str = HOST, port: int = DEFAULT_PORT,
                repo_root: Path | None = None, ui_dir: Path | None = None,
                roster_path: Path | None = None, answers_enabled: bool = False) -> OfficeServer:
    if host != HOST:
        raise ValueError(f"the office server binds {HOST} only, not {host}")
    return OfficeServer((host, port), Handler, project, repo_root or REPO_ROOT, ui_dir, roster_path, answers_enabled)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Serve the virtual office window.")
    parser.add_argument("--project", default=".", help="project folder holding .agents/ and .team/ (default: .)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--roster", default=None, help="roster.md to read (default: see above)")
    parser.add_argument("--no-open", action="store_true", help="do not open the browser")
    parser.add_argument("--enable-answers", action="store_true",
                        help="accept POST /answer from the window (off by default: the window is a viewer)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        server = make_server(Path(args.project).resolve(), port=args.port,
                             roster_path=Path(args.roster) if args.roster else None,
                             answers_enabled=args.enable_answers)
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
