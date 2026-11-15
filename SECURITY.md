# Security

Skills are instructions for AI agents, so a security problem here usually means "the instructions make an agent do something unsafe". Examples: leak a secret, spend money or delete data without asking, follow instructions hidden in a repo, email or web page, or skip a safety check.

## How to report (privately)

**Do not open a public issue.** Use GitHub's private reporting:

1. Go to the repository on GitHub → **Security** tab → **Report a vulnerability**, or open this link directly: <https://github.com/bilawalbaig8/hire-an-engineer/security/advisories/new>
2. Say what the skill made the agent do, which tool you used (Claude Code, claude.ai, Cursor, …), and the skill version if you know it.
3. Don't include real keys, passwords or customer data. Use made-up values.

## What is in scope

- The skill's instructions (`skills/hire-an-engineer/`) causing an agent to take unsafe actions or expose secrets.
- The GitHub workflows in `.github/workflows/` (for example release or issue-triage behaviour that could be abused).
- The packaging and validation scripts in `scripts/`.

Not in scope: problems in the AI tools themselves (Claude, Cursor, Codex, …), or in projects you built using the skill. Report those to the tool's vendor.

## Supported versions

Only the **latest release** is supported: <https://github.com/bilawalbaig8/hire-an-engineer/releases/latest>. If you use an older version, update first and check whether the problem is still there.

## What to expect

This is a one-person project. Reports are handled on a best-effort basis, usually within a week. Fixes are published as a new release and noted in the [CHANGELOG](CHANGELOG.md).
