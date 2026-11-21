# Installing Hire an Engineer

You do not need a terminal. The easiest way is to let your AI do it; or pick your tool below and follow the steps by hand.

## Ask your AI to install it (easiest)

Copy this into Claude Code, Cursor, Codex, Antigravity or another coding agent:

```text
Install the Hire an Engineer skill for me from https://github.com/bilawalbaig8/hire-an-engineer — follow docs/INSTALL.md in that repo.
```

Using your own fork? Put your fork's link in the message instead.

### Steps for the AI agent doing the install

1. **Get the skill folder.** Download `https://github.com/bilawalbaig8/hire-an-engineer/releases/latest/download/hire-an-engineer.zip` and unzip it; it holds one folder, `hire-an-engineer/`, with `SKILL.md` inside. If the repository is a fork with no releases, copy the `skills/hire-an-engineer/` folder from the repository instead. Never use GitHub's "Source code" zip, and run no script from the repository.
2. **Put it where your tool reads skills:**
   - Claude Code: `~/.claude/skills/hire-an-engineer/` (Windows: `%USERPROFILE%\.claude\skills\hire-an-engineer\`), for every project. Tell the person they can instead run `/plugin install hire-an-engineer --marketplace bilawalbaig8/hire-an-engineer` themselves, which also gives them the live agent crew view.
   - Any other tool: `<project>/hire-an-engineer/`, then add this line to the project's `AGENTS.md` (or the tool's rules file): `Follow the skill at hire-an-engineer/SKILL.md and read its references when its router says so.` If the tool has its own skills folder, use that instead.
3. **Check:** `<skills folder>/hire-an-engineer/SKILL.md` exists, with no nested `hire-an-engineer/hire-an-engineer/`.
4. **Tell the person** in one or two plain sentences where it was installed and that a new chat or session picks it up. Then ask what they want to build.

## Install it yourself

**Roman Urdu mein khulasa:** Hire an Engineer ek skill hai jo aapke AI tool ko senior software engineer bana deti hai. Aap apna idea aasan zabaan mein batate hain; planning, building, testing aur documents woh sambhalti hai. Install: [Releases](https://github.com/bilawalbaig8/hire-an-engineer/releases/latest) page se `hire-an-engineer.zip` download karein. **claude.ai** mein zip ko unzip KIYE BAGHAIR Settings se upload karein. **Claude Code** mein unzip karke `hire-an-engineer` folder ko `.claude/skills` ke andar rakhein. Pehla message: *"Mujhe apni bakery ke orders ke liye ek simple app chahiye."* Check karne ke liye Claude se poochein: *"what skills do you have?"*

## 1. Download the right file

Open the [latest release](https://github.com/bilawalbaig8/hire-an-engineer/releases/latest) and download **`hire-an-engineer.zip`** (or `hire-an-engineer.skill`; it is the same zip with another name) from the **Assets** list.

> **Do not** use GitHub's **"Source code (zip)"** links on the release page or the green **Code → Download ZIP** button. They have the wrong folder layout and the install will not work.

## 2. Install for your tool

| Your tool | Go to |
|---|---|
| claude.ai (website or app) | [claude.ai](#claudeai) |
| Claude Code | [Claude Code, no terminal](#claude-code-without-a-terminal) or [with a terminal](#claude-code-with-a-terminal) |
| Cursor, Codex, Antigravity, Gemini CLI, others | [Other tools](#cursor-codex-antigravity-gemini-cli-and-other-tools) |

**What is tested:** Claude Code and claude.ai. Other tools are best effort: the skill is plain files, so it usually works, but I have not verified every tool.

### claude.ai
1. Use the `.zip` or `.skill` file from step 1 **as it is. Do not unzip it.**
2. In claude.ai, open **Settings** and look for **Capabilities** (or **Skills**), then upload the file there. Menu names can change; if you cannot find it, check claude.ai's help for "Skills". Some versions also let you open a `.skill` file in a chat and click **Save skill**.
3. Make sure **code execution / file creation** is turned on in the same settings. The skill needs it.
4. Check it worked: start a new chat and ask *"what skills do you have?"*. `hire-an-engineer` should be listed and switched on.

### Claude Code in one line (plugin)

In Claude Code, type this at the prompt, answer `y` to add the marketplace, then pick a scope:

```text
/plugin install hire-an-engineer --marketplace bilawalbaig8/hire-an-engineer
```

This also installs the **agent crew** view beside the chat, which shows each AI lane at work. It opens by itself, or with `/crew`. To add it to a skill you installed from files:

```text
/plugin install agent-crew --marketplace bilawalbaig8/hire-an-engineer
```

Optional project board (tasks by stage, what waits for you), opened with `/board`:

```text
/plugin install hire-an-engineer-board --marketplace bilawalbaig8/hire-an-engineer
```

Update later from the `/plugin` menu. Prefer files? Use one of the two routes below instead (not both).

### Claude Code without a terminal
The goal: the file `SKILL.md` must end up at `.claude\skills\hire-an-engineer\SKILL.md` inside your user folder.

**Windows**
1. Right-click `hire-an-engineer.zip` → **Extract All** → Extract.
2. **Warning:** Windows often creates `hire-an-engineer\hire-an-engineer\`. Open folders until you see `SKILL.md` and a `references` folder together. That inner folder is the one to copy.
3. Press **Win + R**, type `%USERPROFILE%\.claude` and press Enter. (If Windows says it cannot find it, start Claude Code once and try again.)
4. In that window, create a folder named `skills` if it is not there.
5. Copy the `hire-an-engineer` folder (the one that holds `SKILL.md`) into `skills`.
6. Check: you can open `...\.claude\skills\hire-an-engineer\SKILL.md`. If you must go through `hire-an-engineer\hire-an-engineer\SKILL.md`, you have one folder too many; move the inner one up.

**macOS**
1. Double-click `hire-an-engineer.zip`. You get a `hire-an-engineer` folder.
2. In Finder choose **Go → Go to Folder**, type `~/.claude` and press Return. (Press **Cmd + Shift + .** to show hidden folders. If the folder is missing, start Claude Code once and try again.)
3. Create a folder named `skills` if it is not there.
4. Drag the `hire-an-engineer` folder into `skills`. You should be able to open `~/.claude/skills/hire-an-engineer/SKILL.md`.

**Check it worked:** close Claude Code, start it again, and ask *"what skills do you have?"*. `hire-an-engineer` should be in the list.

### Claude Code with a terminal
Go to the folder where you saved the download first, then unzip and copy.

macOS / Linux:
```bash
cd ~/Downloads
unzip hire-an-engineer.zip
# all projects (personal skills)
mkdir -p ~/.claude/skills && cp -r hire-an-engineer ~/.claude/skills/
# or one project only (run from the project folder instead)
# mkdir -p .claude/skills && cp -r ~/Downloads/hire-an-engineer .claude/skills/
```

Windows PowerShell:
```powershell
cd "$env:USERPROFILE\Downloads"
Expand-Archive hire-an-engineer.zip .
# all projects (personal skills)
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse hire-an-engineer "$env:USERPROFILE\.claude\skills\"
# or one project only (run from the project folder instead)
# New-Item -ItemType Directory -Force .claude\skills | Out-Null
# Copy-Item -Recurse "$env:USERPROFILE\Downloads\hire-an-engineer" .claude\skills\
```
If you downloaded the `.skill` file, rename it to `.zip` first. If you cloned the repo instead of downloading a release, the folder is `skills/hire-an-engineer` inside the clone. Then do the "check it worked" step above.

### Cursor, Codex, Antigravity, Gemini CLI and other tools
Tool folders and settings change often, so this guide does not guess them. The route that works in any tool that can read your project files:

1. Unzip `hire-an-engineer.zip` and put the `hire-an-engineer` folder **inside your project**, so you have `<your project>/hire-an-engineer/SKILL.md`.
2. In the project's `AGENTS.md` (or your tool's rules / instructions file, if it does not read `AGENTS.md`), add this one line:
   `Follow the skill at hire-an-engineer/SKILL.md and read its references when its router says so.`
3. Start a new chat or session in that project and ask for something to build. Check it worked by asking *"which skill are you following?"*.

If your tool supports Agent Skills, it may have its own skills folder. See that tool's documentation and put the same `hire-an-engineer` folder there.

**Chat apps other than claude.ai:** if the app has project files or a knowledge area, upload the whole `hire-an-engineer` folder's files there. Pasting 30+ files into one chat is not practical. Chat-only apps can plan, design and write documents, but they cannot build and test software the way a coding agent can.

## Check it worked (all tools)
Ask: *"what skills do you have?"* (Claude) or *"which skill are you following?"* (tools using the `AGENTS.md` route). Then try a first message, for example:
- English: *"I want to build a booking app for my salon."*
- Roman Urdu: *"Mujhe apni bakery ke orders ke liye ek simple app chahiye."*

## Updating
Download the newer release, delete the old `hire-an-engineer` folder, then copy the new one in (copying over it would leave removed files behind).
- **claude.ai:** delete the old skill in the Skills settings, then upload the new file.
- **Without a terminal:** delete `.claude\skills\hire-an-engineer` in File Explorer / Finder, then copy the new folder in as above.
- macOS / Linux: `rm -rf ~/.claude/skills/hire-an-engineer && cp -r hire-an-engineer ~/.claude/skills/`
- Windows PowerShell: `Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\hire-an-engineer"; Copy-Item -Recurse hire-an-engineer "$env:USERPROFILE\.claude\skills\"`

Your projects keep their own `AGENTS.md` and `PROJECT_STATE.md`, so nothing is lost.

## Uninstall or turn it off
- **Claude Code:** delete the folder `.claude\skills\hire-an-engineer` (user folder, or the project's `.claude/skills/` if you installed it per project).
- **Other tools:** delete the `hire-an-engineer` folder from your project and remove the line you added to `AGENTS.md` / the rules file.
- **claude.ai:** open the Skills settings and switch it off, or delete it there.

**Removing the skill does not delete your projects' files.** While working, the skill may create these in your project, and they stay until you delete them yourself: `AGENTS.md`, `PROJECT_STATE.md`, `TASKS.md`, `REPORT.md`, `QUESTIONS.md`, a `docs/` folder, and Git commits and branches. They are plain files you can keep, edit or delete.

## Which version do I have?
The version is in the release name on the [Releases](https://github.com/bilawalbaig8/hire-an-engineer/releases) page (for example `hire-an-engineer-v0.5.0`) and on the **last line of `SKILL.md`** inside the folder. The file you download is always named `hire-an-engineer.zip`, so the name of the file does not tell you the version. The [CHANGELOG](https://github.com/bilawalbaig8/hire-an-engineer/blob/main/CHANGELOG.md) lists what changed in each one.
