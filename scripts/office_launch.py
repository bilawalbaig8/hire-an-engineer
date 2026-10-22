"""Claude Code hook: start the local office window server once per project.

Usage (as a hook, payload JSON on stdin):
    python scripts/office_launch.py [--no-browser] [--port N] [--project DIR]
Other modes:
    python scripts/office_launch.py --status   # print whether the server runs
    python scripts/office_launch.py --stop     # stop it and remove .agents/office.json

Project folder: CLAUDE_PROJECT_DIR, else payload "cwd", else --project, else cwd.
State file <project>/.agents/office.json: {pid, port, started, opened}. A server
counts as running only if its pid is alive AND 127.0.0.1:port answers GET /state;
otherwise the file is stale and replaced. The browser opens once per session id.

Never fails the host: prints nothing to stdout when used as a hook, errors go to
stderr, exit code is always 0. Stdlib only.
"""
from __future__ import annotations

import argparse
import http.client
import json
import os
import socket
import subprocess
import sys
import time
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

SERVER_SCRIPT = Path(__file__).resolve().parent / "office_server.py"
HOST = "127.0.0.1"
DEFAULT_PORT = 8765
STATE_REL = Path(".agents") / "office.json"
WAIT_SECONDS = 3.0


def _err(msg: str) -> None:
    print(f"office_launch: {msg}", file=sys.stderr)


def read_payload(stdin) -> dict:
    try:
        if stdin is None or stdin.isatty():
            return {}
        data = json.loads(stdin.read() or "{}")
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def pick_project(payload: dict, override: str | None) -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR", "").strip()
    cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else ""
    return Path(env or cwd or override or os.getcwd()).resolve()


def pid_alive(pid) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    if os.name == "nt":
        import ctypes
        k32 = ctypes.windll.kernel32
        h = k32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        try:
            code = ctypes.c_ulong()
            return bool(k32.GetExitCodeProcess(h, ctypes.byref(code))) and code.value == 259  # STILL_ACTIVE
        finally:
            k32.CloseHandle(h)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def server_alive(port) -> bool:
    if not isinstance(port, int) or not 0 < port < 65536:
        return False
    try:
        conn = http.client.HTTPConnection(HOST, port, timeout=1)
        conn.request("GET", "/state")
        ok = conn.getresponse().status == 200
        conn.close()
        return ok
    except Exception:
        return False


def find_free_port(start: int) -> int:
    for port in range(start, start + 50):
        with socket.socket() as s:
            try:
                s.bind((HOST, port))
                return port
            except OSError:
                continue
    with socket.socket() as s:
        s.bind((HOST, 0))
        return s.getsockname()[1]


def load_state(project: Path) -> dict:
    try:
        data = json.loads((project / STATE_REL).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_state(project: Path, state: dict) -> None:
    path = project / STATE_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def is_running(state: dict) -> bool:
    return pid_alive(state.get("pid")) and server_alive(state.get("port"))


def kill_pid(pid: int) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    else:
        import signal
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass


def spawn_server(project: Path, port: int) -> subprocess.Popen:
    cmd = [sys.executable, str(SERVER_SCRIPT), "--project", str(project), "--port", str(port), "--no-open"]
    kwargs: dict = dict(stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, cwd=str(project), close_fds=True)
    if os.name == "nt":
        kwargs["creationflags"] = (subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
                                   | getattr(subprocess, "CREATE_NO_WINDOW", 0))
    else:
        kwargs["start_new_session"] = True
    return subprocess.Popen(cmd, **kwargs)


def start_server(project: Path, start_port: int) -> dict | None:
    if not SERVER_SCRIPT.is_file():
        _err(f"server script not found: {SERVER_SCRIPT}")
        return None
    port = find_free_port(start_port)
    proc = spawn_server(project, port)
    deadline = time.monotonic() + WAIT_SECONDS
    while time.monotonic() < deadline:
        if server_alive(port):
            return {"pid": proc.pid, "port": port,
                    "started": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "opened": []}
        if proc.poll() is not None:
            break
        time.sleep(0.1)
    _err(f"server did not answer on {HOST}:{port} within {WAIT_SECONDS:.0f}s")
    if proc.poll() is None:
        kill_pid(proc.pid)
    return None


def do_status(project: Path) -> None:
    state = load_state(project)
    if state and is_running(state):
        print(f"running pid={state['pid']} port={state['port']} url=http://{HOST}:{state['port']}/")
    else:
        print("not running")


def do_stop(project: Path) -> None:
    state = load_state(project)
    if state and is_running(state):
        kill_pid(state["pid"])
        print(f"stopped pid={state['pid']}")
    else:
        print("not running")
    try:
        (project / STATE_REL).unlink()
    except FileNotFoundError:
        pass


def do_launch(project: Path, payload: dict, start_port: int, browser: bool) -> None:
    state = load_state(project)
    if not (state and is_running(state)):
        state = start_server(project, start_port)
        if state is None:
            return
        save_state(project, state)
    if browser:
        sid = payload.get("session_id") if isinstance(payload.get("session_id"), str) else ""
        opened = [s for s in state.get("opened", []) if isinstance(s, str)]
        if sid not in opened:
            try:
                webbrowser.open(f"http://{HOST}:{state['port']}/")
            except Exception as e:
                _err(f"cannot open browser: {e}")
            opened.append(sid)
            state["opened"] = opened
            save_state(project, state)


def main(argv: list[str] | None = None, stdin=None) -> int:
    try:
        parser = argparse.ArgumentParser(description="Start the office window server once per project.")
        parser.add_argument("--project", default=None, help="project folder (CLAUDE_PROJECT_DIR and payload cwd win)")
        parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="first port to try (default 8765)")
        parser.add_argument("--no-browser", action="store_true")
        parser.add_argument("--stop", action="store_true")
        parser.add_argument("--status", action="store_true")
        args = parser.parse_args(argv)
        payload = {} if (args.stop or args.status) else read_payload(sys.stdin if stdin is None else stdin)
        project = pick_project(payload, args.project)
        if args.status:
            do_status(project)
        elif args.stop:
            do_stop(project)
        else:
            do_launch(project, payload, args.port, not args.no_browser)
    except SystemExit:
        pass
    except BaseException as e:  # never fail the host
        _err(f"{type(e).__name__}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
