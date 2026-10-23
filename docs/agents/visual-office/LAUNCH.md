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

## Answering in the window (MCP server `office`)

The owner can answer the boss's questions and approvals in the chat or in the office window; the first answer wins. The window's answer button appends a line to `<project>/.team/inbox.jsonl`; `scripts/office_mcp.py` (a local MCP server over stdio, Python stdlib only) gives the boss two tools:

- `mcp__office__wait_for_owner_answer` `{id, timeout_seconds}` (default 600, max 3500): waits for the window's answer to that question or approval id and returns it as JSON (`status` `answered`, `id`, `answer`, `kind`, `decision`, `option`, `answers`, `text`, `source`), or `status` `no_answer` when the time runs out. An answer typed in the chat interrupts the wait.
- `mcp__office__pending_window_answers`: lists window answers not handed out yet (does not mark them read).

Handed-out answers are recorded in `.team/inbox.consumed`, so each is returned once; a newer answer with the same id is returned again.

Enable, per project:
1. Put `scripts/office_mcp.py` next to `office_launch.py` and `office_server.py`.
2. Copy `mcp-config.example.json` to the project root as `.mcp.json` (merge into `mcpServers` if the file exists). The server name must stay `office`: tool names are `mcp__<server>__<tool>`. `timeout` is milliseconds per tool call; `${CLAUDE_PROJECT_DIR:-.}` needs the `:-.` default in a project `.mcp.json` (Claude Code sets `CLAUDE_PROJECT_DIR` in the server's environment, not in its own).
3. The first interactive session asks once to approve the new project MCP server. To skip the per-call prompt, add an allow rule to the project's `.claude/settings.json`: `"permissions": {"allow": ["mcp__office__wait_for_owner_answer", "mcp__office__pending_window_answers"]}`.
4. The boss's agent file already lists both tools; when the server is not set up they are simply missing and the boss asks in the chat.

Headless (`claude -p`): pass the rule as `--allowedTools "mcp__office__wait_for_owner_answer"`; without it the call is denied (tested). A project `.mcp.json` was loaded in `-p` mode without an approval prompt (tested); `--mcp-config <file>` also works, and `--strict-mcp-config` ignores every other MCP server.

Tested on 2026-10-23 with Claude Code 2.1.308 on Windows, headless, in a throwaway project: answer already in the inbox (returned at once), no answer (`no_answer` after 20 s, not an error), answer appended 12 s into a 60 s wait (returned when written), the call without the allow rule (denied), and `claude -p --agent orchestrator` with the agent file's tools line (the tool resolved and returned the answer). The client asked for protocol `2025-11-25`.

Not verified: an interactive session (the approval dialog, Esc or typing during a wait, the 2-minute move to the background), the Claude Desktop app, and the boss following the skill's window steps in a full team run.

## Starting the boss and installing the team
- Start the boss in the project folder with `claude --agent orchestrator`.
- Install per project for headless runs, evals and automation: `python scripts/install_agents.py --dest <project>/.claude --only orchestrator --only software-architect --only code-reviewer`. Global install (`--only NAME`, copies to `~/.claude`) is for interactive sessions.
- Headless runs (`claude -p ...`) refuse to read `~/.claude/skills/`, so a global install is not enough there (see PERMISSIONS.md).
- After installing, run again with `--dry-run` and expect `0 new, N same, 0 differ`. Never use `--force` on hire-an-engineer files.

## How to open the office window (every time)
1. Start the team in the project folder: just `claude` (the installer sets the project's default agent to the boss; without that setting use `claude --agent orchestrator`). The SessionStart hook starts the local server by itself and opens the window in your default browser (once per session). The boss also tells you the address in its first message.
2. If the window did not open, or you closed it: run `python .agents/office/office_launch.py --status`. It prints the address, normally `http://127.0.0.1:8765/`. Paste it into Chrome.
3. If it says `not running`: start it with `python .agents/office/office_launch.py` (add `--no-browser` to only start the server), then open the address.
4. Stop it with `python .agents/office/office_launch.py --stop`.
The window only reads this project's `.agents/events.jsonl`; reload the page if it ever looks cropped.

## Answering: terminal only for now (owner decision, 2026-10-23)
The window is a viewer. Questions and approvals show in its Inbox as a read-only list ("Answer in your Claude session"); you answer in the terminal. The window answer buttons, the office MCP tools and the window chat are switched off: the code is kept (`scripts/office_server.py` POST /answer, `scripts/office_mcp.py`, the Inbox form with `?answers=1` or the demo), the boss does not use it. The chat work in progress is saved as a patch outside the repo; bring it back only when the owner asks.

## New project, nothing installed yet
Run once from the repo: `python scripts/setup_team.py --project <project folder>` (team, office, hooks, default agent). Then `claude` in that folder starts the boss. Before that a project is just normal Claude Code.
