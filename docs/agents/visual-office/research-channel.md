# Research: window <-> running Claude Code session channel

Date 2026-10-23. Source: official docs only, fetched this session. Base: https://code.claude.com/docs/en/
Every claim carries its page. Anything not on a page is marked **unverified**. Nothing was run; no experiment touched ~/.claude or settings.

Short names: HOOKS = hooks.md, CH = channels.md, CHR = channels-reference.md, MCP = mcp.md, XS = cross-session-messaging.md, DESK = desktop.md.

## 1. What the docs confirm (facts used below)

Hooks (HOOKS)
- SessionStart fires on new/resumed session; only `command` and `mcp_tool` hook types. In interactive sessions it runs in the background, but "Claude's first response still waits for the hooks to finish"; a prompt typed meanwhile waits too.
- SessionStart can return `hookSpecificOutput.additionalContext` (also `initialUserMessage`, `sessionTitle`, `watchPaths`, `reloadSkills`). Plain stdout on exit 0 is added as context.
- UserPromptSubmit fires before Claude processes a prompt (also on turns Claude Code starts itself). It can block (exit 2, or `decision:"block"` + `reason`) or add `additionalContext`; it cannot replace the prompt. Default timeout 30 s; on timeout output is discarded.
- Cap: `additionalContext`, `systemMessage`, `initialUserMessage` and plain stdout are capped at 10,000 characters; overflow goes to a file with a 2,000-char preview. Not raisable.
- Exit 1 is a non-blocking error; only exit 2 blocks.
- `async: true` runs a command hook in the background without blocking; timeout not enforced on it. `asyncRewake: true` wakes Claude on exit code 2 and shows stderr (or stdout) as a system reminder.
- A hook may start a background process; redirect its output (`>/dev/null 2>&1 &`) or the call can be blocked ("refusing to honor the suspect capture"). Doc example is for PreToolUse-style allow output; applicability to SessionStart is **unverified**.
- Windows: command hooks default to `bash` (Git Bash), fall back to PowerShell; `"shell": "powershell"` selectable. Exec form needs a real .exe. Nothing on detaching a process on Windows (**unverified**).
- PreToolUse on `AskUserQuestion`: a hook may return `permissionDecision:"allow"` plus `updatedInput` containing `answers` to answer the question without the dialog. PermissionRequest hook can return `decision.behavior` allow/deny. Both HOOKS.
- Stop hook can `decision:"block"` with a reason to keep Claude working; capped at 8 consecutive continuations (HOOKS).
- Hook types `http` (POST of the input JSON to a URL) and `mcp_tool` exist (HOOKS).
- Desktop: "The desktop app reads the same settings files as the CLI" (DESK). Plugins can add hooks and MCP servers (DESK). Hooks and `--channels` in Desktop are not documented in the parts read (**unverified**; about 1/3 of the Desktop and hooks pages was not read).

Channels (CH, CHR)
- A channel is an MCP server that pushes events into a running session; can be two-way (reply tool). Claude Code spawns it as a stdio subprocess (CHR "Overview").
- Research preview. Needs claude.ai login or Console API key; not on Bedrock/Vertex/Foundry. Team/Enterprise orgs must enable `channelsEnabled`; Pro/Max without org skip checks (CH).
- `--channels` accepts only allowlisted plugins; custom ones need `--dangerously-load-development-channels server:<name>`, which shows a confirmation dialog, and is ignored with `-p` / Agent SDK (CHR "Test during the research preview").
- Neither flag appears in `claude --help`; "being in .mcp.json isn't enough" (CH).
- Contract: capability `experimental['claude/channel']`, emit `notifications/claude/channel` with `content` and `meta`. Arrives as `<channel source="..." ...>` in context. If Claude is busy, events queue and are delivered together next turn (CHR). Idle session: delivered as a new turn (**inferred** from CH quickstart "message arrives in your session"; not stated in these words).
- Permission relay: `experimental['claude/channel/permission']`; terminal dialog and remote prompt both stay live; whichever answers first wins and the other closes. Covers tool approvals (Bash/Write/Edit); project-trust and MCP-consent dialogs do not relay (CHR "Relay permission prompts"). Needs v2.1.234+.
- In `-p` mode, multiple-choice questions and plan-mode approval are disabled (CH quickstart).
- Fakechat (official demo): browser UI on http://localhost:8787, two-way, Bun required (CH quickstart).
- Channel servers negotiating MCP protocol 2026-07-28 are not registered; `MCP_PROTOCOL_NEGOTIATION=legacy` keeps the old handshake (MCP "Channels").

MCP (MCP)
- Tool call timeout: per-server `timeout` ms in .mcp.json (hard, progress does not extend); unset `MCP_TOOL_TIMEOUT` default about 28 h. Idle timeout 30 min for stdio servers, 5 min for HTTP/SSE (`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`, 0 disables). Progress notifications reset idle.
- A tool call running over 2 min in the main conversation moves to a background task and Claude keeps working (`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`, 0 disables). Not applied to subagent calls or non-interactive runs.
- A tool call waiting on an open elicitation dialog is not backgrounded (MCP). Elicitation body not read (**unverified**).
- Project .mcp.json servers need interactive approval once ("New MCP server found in this project").
- Windows stdio: stdin closed, process tree killed after 300 ms if still alive (v2.1.296+).

Cross-session messaging (XS)
- Needs v2.1.224+ (v2.1.234+ native Windows). Claude calls `ListAgents`/`SendMessage`; local delivery over a per-session socket (named pipe on Windows).
- Exported to hooks and Bash: `CLAUDE_CODE_MESSAGING_SOCKET` and `CLAUDE_CODE_MESSAGING_TOKEN`. "a script or hook [can] post into a session": send `{"type":"auth","token":...}` first (required on Windows), then a line; connection closes after 30 s without a complete line.
- Hard limits: a peer message "can't approve anything" and never counts as the owner's consent; it arrives as plain text; permission prompts still fire. Own-child messages are delivered when no `crossSessionInbound` value applies. On native Windows, only the token verifies own-child.
- In the Desktop app and VS Code a held message cannot show the approval dialog; kept until `dialogExpiry` (default 5 min) (XS).
- Wire format of the socket line beyond auth is not documented in the page read (**unverified**).

## 2. Options

### A. Hook starts local server and opens the browser
- Fits: SessionStart (source=startup) or UserPromptSubmit on the first prompt. Hook = `command`; script starts server detached, opens `http://127.0.0.1:PORT`, prints at most a short line.
- Confirmed: output cap 10,000 chars; SessionStart/UserPromptSubmit may return `additionalContext`; `async: true` avoids blocking Claude's first response; background processes allowed if output is redirected.
- Caveats: SessionStart blocks the first response unless `async`; UserPromptSubmit default 30 s timeout. Detached process surviving hook exit and session end on Windows: **unverified** (use `Start-Process -WindowStyle Hidden` or `pythonw`; test it). Opening the browser: ordinary OS call (`start`), nothing in docs forbids it; **unverified** under Desktop.
- Idempotency (pid/port file, one server per project) is the script's job.
- Verdict: **works with caveat** (open + serve). A hook cannot itself take the answer back; see B/D/E.

### B. Inbox file polled by the boss with a blocking Bash wait
- Boss asks the question in plain text, then runs `python scripts/wait_answer.py <question_id>` which blocks until `.agents/inbox/<id>.json` appears or timeout. Window writes the file.
- Terminal answer vs window answer: the terminal answer cannot unblock a running Bash call; the owner must interrupt (Esc) the wait or the boss must poll in slices (e.g. 20 s loops) and check for a new user turn. A typed terminal message while a tool runs is queued for the next turn (**unverified**; not read in these pages). So "first wins" is only half-true: window wins instantly; terminal wins after the wait ends or is interrupted.
- Bash tool timeout default/max: not read from the Bash tool page (**unverified**; CLAUDE.md of this repo says nothing). Slice the wait to be safe. Long waits still burn no tokens while blocked.
- Verdict: **works with caveat**. Simplest, no preview features, works in CLI and (likely) Desktop. Terminal-vs-window race is imperfect.

### C. Channel / push-event feature
- Exists (CH, CHR), and is the documented way to push window text into a running session; two-way; permission relay gives exactly "answer in terminal or window, first wins" for tool approvals.
- Cons: research preview; flags unlisted in `--help` and may change; custom channel needs `--dangerously-load-development-channels` plus a confirmation dialog on every start (CHR); ignored in `-p`/SDK; needs claude.ai or Console auth; org policy on Team/Enterprise; Bun or Node MCP SDK; `claude --agent orchestrator --dangerously-load-development-channels server:office` combination not shown in docs (**unverified**). Desktop support **unverified** (not mentioned in DESK parts read). Permission relay does not cover the boss's free-text questions, only tool approvals.
- Owner types in the terminal: also works, it is just a normal prompt. So for free-text questions the "either place" requirement is met natively.
- Verdict: **works with caveat** (best fit for CLI; preview risk; Desktop unknown).

### D. Local MCP server with `wait_for_owner_answer`
- Plain MCP stdio server in .mcp.json; boss (needs the tool in its `tools:` list; orchestrator.md currently lists Agent, Read, Grep, Glob, Bash, Write) calls it; server serves the window and returns the answer as the tool result.
- Confirmed: long tool calls allowed (per-server `timeout`, idle 30 min for stdio, progress notifications reset idle); calls over 2 min become background tasks in the main conversation, so Claude keeps working and is told when done (MCP). Elicitation dialog not backgrounded.
- Terminal answer: same limitation as B (cannot unblock the call); owner interrupts. Behaviour of an interrupted MCP call (does the server see a cancel?): **unverified**.
- Not a preview feature; also the same server can be the channel (C) later (same process, add the capability).
- Cons: first-use approval dialog for project .mcp.json; Windows process-tree kill on exit is fine. Needs Node or Python MCP SDK.
- Verdict: **works** for window answers; **works with caveat** for the race.

### E. UserPromptSubmit hook injects pending window answers into the next turn
- Window writes `.agents/inbox.jsonl`; hook on UserPromptSubmit reads unread lines and prints them as `additionalContext` (cap 10,000 chars). Confirmed mechanism (HOOKS).
- Limit: fires only when a turn starts (a prompt or a Claude-started turn); an idle session never sees a window answer until the owner types something. The window could show "now press Enter in the terminal / type ok", poor UX, but zero new tech.
- Combine with Stop hook (`decision:"block"` + reason, 8-continuation cap) to inject pending answers when Claude would stop: confirmed behaviour for Stop, but the session must be running; for an idle session no hook fires.
- Verdict: **works with caveat**; good as the fallback layer, not as the primary.

### F. (extra) Cross-session messaging to your own session
- A hook script can post into its own session's socket using `CLAUDE_CODE_MESSAGING_SOCKET` + token (XS). That would start a turn in an idle session with the window's answer, with no preview flags.
- Cons: requires v2.1.224+/2.1.234+ Windows; message framing past the auth line undocumented (**unverified**); only the session's own hook/Bash child gets "own-child" delivery, a separate server process started by a hook is a child of the hook (likely counts, **unverified**); Desktop cannot show the approval dialog if a message is held; peer messages never count as approval (so a "yes, approve" from the window cannot answer a permission prompt, only free text for Claude to act on). The owner's approval for the boss's gates is a conversational answer, not a tool permission, so it still works as text.
- Verdict: **works with caveat / mostly unverified**; promising, needs a real test.

## 3. Verdict table

| Option | Opens window | Window -> running session | Terminal and window both | Verdict |
|---|---|---|---|---|
| A hook starts server + browser | yes | no | n/a | works with caveat |
| B inbox file + blocking Bash | via A | yes (boss polling) | window instant; terminal needs Esc | works with caveat |
| C channel (dev flag) | via A | yes, push, idle too | native for text; relay for tools | works with caveat (preview, Desktop unverified) |
| D MCP `wait_for_owner_answer` | via A | yes | like B | works (race caveat) |
| E UserPromptSubmit inject | via A | only on next turn | yes | works with caveat (not for idle) |
| F socket post from hook | via A | yes, starts a turn | yes | unverified |

## 4. Recommended design

Layered, each layer works without the next:
1. Window start (A): `SessionStart` hook, `async: true`, runs `scripts/office_start.py`: starts server once (pid/port file in `.agents/`), opens browser, prints one short line. Server writes answers to `.agents/inbox.jsonl` (append-only) and reads `.agents/events.jsonl` for display (already there).
2. Primary answer path (D): MCP server `office` with `wait_for_owner_answer(question_id, timeout_s)` plus `ask_owner`; boss uses it for questions and approvals while a question is open; sliced wait (<= 5 min per call) with the boss re-asking in text so a terminal answer is never lost: boss says in the terminal "answer here or in the window". If the owner types in the terminal, the boss treats that as the answer and the window shows "answered in terminal" (boss logs an event).
3. Fallback (E): `UserPromptSubmit` hook injects any unread window answers as `additionalContext`, so an answer sent while Claude was not waiting is never lost.
4. Optional later (C): same MCP server also declares `claude/channel` for push into an idle session; only after a test proves it works with `--agent orchestrator` in CLI and Desktop. Do not depend on it (preview, may change).
Skip B (D replaces it) unless MCP is rejected; B is the zero-dependency fallback for the boss prompt ("run wait_answer.py").

## 5. Minimal test plan (temp folder only)

Use `%TEMP%\office-test`, a throwaway project with its own `.claude/settings.json` and `.mcp.json`; nothing in ~/.claude.
1. A: hook script writes `started.txt`, starts `python -m http.server 8790` detached (`Start-Process -WindowStyle Hidden`), runs `start http://127.0.0.1:8790`. Run `claude` in the folder; check browser opens, session responds immediately with `async:true`, server survives `/exit` (expected: unverified; record it), no duplicate on restart.
2. Hook output: have the hook print 12,000 chars; confirm cap/preview behaviour on SessionStart.
3. D: 30-line MCP stdio server (Node SDK) with `wait_for_owner_answer` reading a file; tell Claude "call it"; write the answer file from another shell; confirm result returns. Then try a 3-minute wait (backgrounding?), and interrupt with Esc (does server get a cancel?) and typing in the terminal during the wait.
4. E: `UserPromptSubmit` hook printing the inbox line; append a line while idle, type "ok", confirm Claude sees it.
5. C: copy the webhook.ts from CHR, run `claude --dangerously-load-development-channels server:webhook`, `curl -d "hi" -H "X-Sender: dev" localhost:8788` while idle: does it start a turn? Repeat with `claude --agent orchestrator` and in the Desktop app (does the flag exist there?).
6. F: from a `UserPromptSubmit`/Bash child, print `$CLAUDE_CODE_MESSAGING_SOCKET`, `/status` Peer address, attempt the auth line + a text line via a pipe client; observe whether a turn starts on native Windows.
7. Record results in this file under "Test results"; mark each unverified item confirmed or refuted.

## 6. Not read (limits of this research)

About 1/3 of hooks.md (after char 200,000: common input fields, async section details, Elicitation hook), the Desktop page parts on hooks/channels, the Bash tool timeout page, agent-sdk/user-input.md, and remote-control.md were not read. Anything depending on those is marked unverified above.
