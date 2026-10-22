---
name: <skill-name>
description: One paragraph, at most 1024 characters. What this skill knows and does AND when to use it (trigger phrases, situations). Rename the folder and this name to match the agent's `skill` field.
---

# <Skill name>

What this knowledge folder lets an agent do, in two or three lines. It works on its own in any tool that reads skills, and the agent file `agents/<role-name>.md` puts a role, a model and a handoff on top of it.

## Rules (priority order)
1. *The rules that always apply, most important first. Keep this list short.*
2. Label every claim about existing work as `verified`, `inferred` or `unknown`.
3. Only cite sources marked `verified` in `references/sources.md` as fact; cite them by ID, for example `[S-AREA-1]`.

## Router: what to read when
| Situation | Read |
|---|---|
| *Typical request* | `references/example.md` |
| *Where the facts come from* | `references/sources.md` |

## Reporting gaps
If this skill falls short, offer the person a pre-filled issue link (see the root README); they review and submit it. Never include private details.
