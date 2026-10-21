# Installing skills

Each skill is a folder: `SKILL.md` plus optional `references/`. Releases also provide `<name>.skill` and `<name>.zip`.

## claude.ai
Download `<name>.skill` from Releases → upload it in Settings (Skills / Capabilities), or open the file in a chat and click **Save skill**. Code execution / file creation must be enabled.

## Claude Code
If you downloaded a release, unzip it first (`unzip hire-an-engineer.zip`, or on Windows `Expand-Archive hire-an-engineer.zip .`; a `.skill` file is a zip archive, so rename it to `.zip` first). If you cloned the repo, use `skills/hire-an-engineer` as the folder below.

macOS / Linux:
```bash
# all projects (personal skills)
mkdir -p ~/.claude/skills && cp -r hire-an-engineer ~/.claude/skills/
# or one project
mkdir -p .claude/skills && cp -r hire-an-engineer .claude/skills/
```

Windows PowerShell:
```powershell
# all projects (personal skills)
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse hire-an-engineer "$env:USERPROFILE\.claude\skills\"
# or one project
New-Item -ItemType Directory -Force .claude\skills | Out-Null
Copy-Item -Recurse hire-an-engineer .claude\skills\
```

## Other agents (Cursor, Codex, Antigravity, Gemini CLI, …)
- If the tool supports Agent Skills, copy the folder into its skills directory.
- If not, add to your project's `AGENTS.md` (or the tool's rules file):
  `Follow the skill at <path>/hire-an-engineer/SKILL.md and read its references when its router says so.`
Conventions change often — check your tool's current documentation.

## Updating
Download the newer release (or `git pull`), delete the old `hire-an-engineer` folder, then copy the new one in (copying over it would leave removed files behind):
- macOS / Linux: `rm -rf ~/.claude/skills/hire-an-engineer && cp -r hire-an-engineer ~/.claude/skills/`
- Windows PowerShell: `Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\hire-an-engineer"; Copy-Item -Recurse hire-an-engineer "$env:USERPROFILE\.claude\skills\"`

Your projects keep their own `AGENTS.md` and `PROJECT_STATE.md`, so nothing is lost.
