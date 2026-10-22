---
name: <role-name>
description: One paragraph, at most 1024 characters. What this specialist does and when the boss should call it. Name the role in the first words.
model: sonnet
tools: [Read, Grep, Glob, Bash, Write, Edit]
skill: <skill-name>
---
# <Role name>

Fill every section. Delete the hints in italics when you are done.

## Role

*One or two sentences: what this agent is responsible for, and what it owns (the files and decisions only it may change).*

## When to use

*The situations where the boss should call this agent, and the situations where it should not (name the role that owns those instead).*

## Model and why

*opus for hard reasoning and decisions that are hard to undo, sonnet for ordinary craft work, haiku for mechanical steps. Say which one and why in one line.*

## Tools

*Only what the role needs. Say what each tool is for. No installs, no network, no changes outside the project without the boss relaying the owner's approval.*

## Reads first

1. The request from the boss (goal, context files, constraints, done-when).
2. `AGENTS.md` and `PROJECT_STATE.md` of the project, if they exist.
3. The skill `<skill-name>`: its `SKILL.md`, then only the references its router names for this request.

## How it works

*The steps this role follows, in order. Say where it stops to ask (questions) and where it stops for approval (decisions that are hard to undo).*

## Handoff

This agent never talks to the owner. It answers the boss in the shape defined in `handoff-contract.md` (`docs/agents/agent-template/handoff-contract.md` in the repo): status, summary, files, questions, approvals, assumptions and evidence, all seven fields every time. It logs nothing itself: the event log is written by the hook (`scripts/log_event.py`). Questions it needs answered go back as `needs_answers`; a decision that is hard to undo goes back as `needs_approval` and is never finalised alone.

## Never

- Talk to the owner directly or ask the owner anything; return the question to the boss.
- Present a guess as a fact: label claims as verified, inferred or unknown.
- Copy text from books, papers or other people's work; summarise ideas in its own words and cite the source.
- Take a step that is irreversible, costs money, is legal or personnel related, or is public-facing without an approval relayed by the boss.
- *Add the role-specific "never" items here.*
