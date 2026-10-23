---
name: team-start
description: Use at the start of any real software job in any folder, including a brand new project (build an app, game or tool, design or plan a system, add a feature, review or fix code, an idea the person wants made), when the specialist team is not already switched on for the folder. Before doing the work it asks the owner ONE question, how to do it (with the specialist team and the live office window, or alone), turns the team on for the folder if chosen, and then works as the boss using the orchestrator skill. Not for quick questions, explanations or tiny edits.
---

# Team start

You are the first step of every real job. Decide whether this is a real job, ask how to run it, then do it that way. The owner never has to set anything up or type a command.

## Rules
1. **Skip the question** for a quick question, an explanation, a one-line edit or a small fix: just do it.
2. **Check the folder first** (look for these files in the project folder):
   - `.agents/enabled` exists: the team is already on. Do not ask. Use the `orchestrator` skill and follow it for the job.
   - `.agents/solo` exists: the owner chose solo here before. Do not ask. Do the job normally (the `hire-an-engineer` skill if present).
   - Neither exists: ask (rule 3).
3. **Ask exactly one question**, in the owner's own language, with the question tool if you have it (otherwise in chat), before any work or any file change:
   - Title: how should I do this?
   - **With the team (recommended for a project)**: Architect designs, Code Reviewers check, a boss plans and keeps the record, and a live office window shows who does what. The owner decides the big choices.
   - **Alone**: one Claude does it directly in this chat, no specialists, no window.
   - Give one plain sentence of your own recommendation for this job (small job: alone is fine; project or anything risky: the team).
   The owner may also answer in words ("team se karo", "akele karo", "sirf architect"). Their words win.
4. **If team:** run `python <this skill folder>/scripts/enable_team.py --project <project folder>` (use the real path of this skill's folder; it is the folder that contains this SKILL.md). It switches the team on for the folder and starts the office window. Tell the owner the office address it prints, once. Then invoke the `orchestrator` skill with the Skill tool and follow it for the whole job (sizing, plan, briefs, approvals, report). If the owner wanted only one specialist, call only that one.
5. **If alone:** run the same script with `--solo` (so you do not ask again for this folder), then do the job normally.
6. **Later in the same folder:** if the owner says "ab team se karo" or "akele karo", rerun the script with the other mode.
7. Never ask this question twice in one folder, never change anything before the owner answered, and never start the team for a job the owner said to do alone.

## What the team is (say this only if asked)
Specialists answer the boss, the boss talks to the owner. Hard-to-undo decisions come to the owner as approvals, in the terminal. The office window only shows the work; it does not take answers.
