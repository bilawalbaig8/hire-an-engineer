# Permissions for the specialist team

Plain-language guide to `permissions-snippet.json`. It is optional, and it is not installed automatically.

## Why

1. **The event log must stay honest.** `.agents/events.jsonl` is what the visual office displays and trusts. The specialists (architect, code-reviewer, ai-engineer, data-scientist, backend-engineer) have the Write tool. If one of them were prompt-injected by text in a reviewed repository, it could write fake lines into that file. Only the hook script (`scripts/log_event.py`) and the boss (through its helper script, run with Bash) should write there.
2. **Running someone else's tests runs someone else's code.** The Code Reviewer has Bash. Tests of a reviewed repository can do anything on your machine, so test running must be an explicit choice and never a default.

## How to use it

1. Open the project's `.claude/settings.json` (create it if missing; it must be strict JSON, no comments).
2. Copy the `deny` and `ask` lists from `permissions-snippet.json` into its `permissions` block. Merge with existing lists, do not overwrite them.
3. Do not copy the keys that start with an underscore (they are notes). Claude Code loaded the whole snippet without complaint in a test, so leaving them in is harmless.
4. Opt in to test running only if you want it: move single lines from `_opt_in_allow_examples.allow` into `permissions.allow`, and only for repositories you trust.

## What the snippet does

- **deny** `Edit`, `Write`, `NotebookEdit` on `/.agents/**`. A deny rule wins over every allow rule and over `acceptEdits`. The docs say deny rules apply to subagents too, and `Edit(...)` rules cover Write (so the extra `Write(...)` lines are belt and braces). The `/` prefix means "relative to the project folder", so the rule only covers the project's own `.agents` folder.
- **ask** on test runners (`pytest`, `python -m unittest`, `dotnet test`, `go test`): you are asked every time. `npm test` is deliberately absent, so it also asks by default, as any unlisted Bash command does.
- **opt-in allow examples**: narrow, exact commands that skip the question. `dotnet test --no-restore` avoids downloading packages. Go uses `GOPROXY=off` and vendored modules, so it cannot fetch code. Remember a deny or ask rule beats an allow rule, so an exact allow line only works if you remove the matching broad `ask` line for it.

## What it does NOT protect

- **`.team/runs/**` is not denied.** The boss must write run records there with the Write tool, and a deny rule cannot be scoped to one agent. So a specialist can still tamper with run records. What is possible instead: (a) the boss writes run records through a helper script with Bash and you then deny `Write(/.team/runs/**)` (needs a change in the boss agent, which this task did not touch); (b) check run records against git history; (c) a PreToolUse hook that blocks Write to `.team/runs/` unless the calling agent is the boss (unverified: whether the hook input identifies the calling subagent).
- **Writes through programs.** The docs say Edit deny rules cover Claude's file tools, recognized file commands in Bash (`cat`, `sed`, `tee`) and Bash redirects, but not a Python or Node script that opens the file itself. A specialist with Bash could run `python -c "open('.agents/events.jsonl','a')..."`. Only the OS sandbox (see the sandboxing docs) blocks that. Unverified here: whether the sandbox works on Windows, and how to deny writes to `.agents` for subagents but not for the boss's helper.
- **Test commands that are allowed run untrusted code.** An allow line is trust in that repository.
- **Settings are not locked.** Project settings can be edited by anyone with file access, including a tool that can write `.claude/settings.json`. Managed settings (organization level) cannot be overridden by project files.
- Deny and ask rules for Bash match the command text Claude writes, not every spelling of the same program; they are not a security boundary around a program (docs).

## Tested (Claude Code 2.1.308, headless, temp project)

- Write to `.agents/events.jsonl` with `--permission-mode acceptEdits`: refused ("File is in a directory that is denied by your permission settings"), file not created, reported in `permission_denials`.
- Write to `notes.txt` in the same project: worked.
- Same `.agents` write through a subagent with the Write tool: refused the same way, file not created.
- Bash `echo forged > .agents/events.jsonl`: not run, file not created. Unverified whether the cause was the deny rule on the redirect target or only that headless mode could not ask for approval.
- Not tested: the opt-in allow lines on a real test run; Windows path edge cases beyond the above.

## Sources

- https://code.claude.com/docs/en/permissions (evaluation order deny, ask, allow; path rule syntax; Bash matching; redirects; "Read and Edit deny rules apply to ... built-in file tools ... not to ... a Python or Node script")
- https://code.claude.com/docs/en/settings (scopes, precedence, lists merge across files)
- https://code.claude.com/docs/en/sub-agents (subagents inherit permission rules; deny rules apply to the main conversation and subagents)

## Headless runs cannot read `~/.claude/skills/` (tested)
- In a headless run (`claude -p ...`) reading files under `~/.claude/skills/` is refused. Permission rules did not help: `Read(~/.claude/skills/**)`, an absolute `//c/...` form and `additionalDirectories` were all still refused.
- Result: the boss could not read its own skill files and improvised (wrong event format, `.md` requests).
- For headless runs, evals and automation use the project-local install: `python scripts/install_agents.py --dest <project>/.claude --only orchestrator --only software-architect --only code-reviewer`.
- In an interactive session the person is asked once and can allow the read.
- Check an install with `--dry-run` (`0 new, N same, 0 differ`). Never use `--force` on hire-an-engineer files; use `--only`.

## The boss needs one allow rule for its event script (tested 2026-10-23)
In a headless run, `python .claude/skills/orchestrator/scripts/team_event.py ...` is refused unless it is allowed, and the boss then stops and asks (correct behaviour). The snippet now allows exactly that script (project-local and `~/.claude` paths) and nothing else. In an interactive session you are asked once instead.

## Headless runs: use the command-line flag (tested 2026-10-23)
In `claude -p` (headless) the `allow` rules of a project `settings.json` were NOT applied (even a minimal file with only `Bash(python:*)`), but the flag worked: `claude -p "..." --agent orchestrator --allowedTools "Bash(python .claude/skills/orchestrator/scripts/team_event.py:*)"` (put the prompt first). The `deny` rules did apply. Interactive sessions: you are asked and can choose to always allow (unverified whether settings `allow` is honoured there).

## Letting the Code Reviewer run tests (safe runner)
The reviewer's only way to run a branch's tests is `skills/code-reviewer/scripts/run_tests_safe.py --ref <branch>`: it copies the committed files of that ref to a scratch folder, runs one known test command with a stripped environment (no tokens or keys) and a timeout, prints JSON and deletes the copy. It never touches your working tree. It is **not a sandbox**: the tests are the author's code and run with your user's rights, so the owner's yes comes first (the boss asks). To allow it without a prompt each time, add `Bash(python .claude/skills/code-reviewer/scripts/run_tests_safe.py:*)` (first lines of `_opt_in_allow_examples` in the snippet); headless runs use `--allowedTools` with the same rule.
