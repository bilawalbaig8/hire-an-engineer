# Opening the office window automatically

A `SessionStart` hook runs `scripts/office_launch.py`. It starts the local office server for the project once (detached, no console window), opens the browser once per session, and prints nothing. The exit code is always 0, so it cannot break a session.

## Enable

1. Make sure the project has `scripts/office_launch.py` and `scripts/office_server.py` side by side (the launcher finds the server next to itself).
2. Copy the `hooks` block from `hooks-snippet-office.json` into the project's `.claude/settings.json` (merge it with any existing `hooks` key). Do not edit `~/.claude`.
3. Start a new Claude Code session in the project. The window opens at `http://127.0.0.1:8765/` (the next free port if 8765 is taken).

`async: true` and `matcher: "startup"` are documented hook fields (research-channel.md). With `async` the first response is not held back; without it Claude waits for the hook.

## Use by hand

```
python scripts/office_launch.py --status      # running pid/port/url, or "not running"
python scripts/office_launch.py --stop        # stop the server, delete .agents/office.json
python scripts/office_launch.py --no-browser  # start without opening a tab
python scripts/office_launch.py --port 9000   # first port to try
```

State lives in `<project>/.agents/office.json`: `{pid, port, started, opened}`. A server counts as running only if the pid is alive and `GET /state` answers on 127.0.0.1; otherwise the file is stale and replaced. `opened` lists the session ids that already got a browser tab.

## Windows notes

- Hooks run under Git Bash (or PowerShell if `"shell": "powershell"` is set); `python` must be on PATH.
- The server is started with `DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW`, with all stdio closed, so no console window appears and it outlives the hook.
- `--stop` uses `taskkill /T /F`.
- The server binds 127.0.0.1 only.

## Not verified

- Hooks inside the Claude Desktop app (docs say it reads the same settings files; hook execution and browser opening there were not tested).
- That the detached server survives the end of the Claude session on every Windows setup (tested only with the unit tests, which use a real subprocess).
- Whether a `SessionStart` hook may print `hookSpecificOutput`: not needed, so the script prints nothing.
