# Installing skills

Each skill is a folder: `SKILL.md` plus optional `references/`. Releases also provide `<name>.skill` and `<name>.zip`.

## claude.ai
Download `<name>.skill` from Releases → upload it in Settings (Skills / Capabilities), or open the file in a chat and click **Save skill**. Code execution / file creation must be enabled.

## Claude Code
```bash
# all projects
mkdir -p ~/.claude/skills && cp -r skills/hire-an-engineer ~/.claude/skills/
# or one project
mkdir -p .claude/skills && cp -r skills/hire-an-engineer .claude/skills/
```

## Other agents (Cursor, Codex, Antigravity, Gemini CLI, …)
- If the tool supports Agent Skills, copy the folder into its skills directory.
- If not, add to your project's `AGENTS.md` (or the tool's rules file):
  `Follow the skill at <path>/hire-an-engineer/SKILL.md and read its references when its router says so.`
Conventions change often — check your tool's current documentation.

## Updating
Download the newer release (or `git pull`) and replace the folder. Your projects keep their own `AGENTS.md` and `PROJECT_STATE.md`, so nothing is lost.
