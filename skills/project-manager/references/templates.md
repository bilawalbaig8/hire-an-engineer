# Templates

Short skeletons for `docs/project/`. Keep files short; delete empty sections. The `PROJECT_STATE.md` and decision record templates of `hire-an-engineer/references/templates.md` and the status format of `hire-an-engineer/references/project-management.md` (section 6) are the base; these add the role's fields. Status words are always written (On track, At risk, Blocked), never colour only. No Gantt charts, burndown charts, story points or velocity at first.

## 1. Plan (`docs/project/plan.md`)
```markdown
# <Project> plan            Status: draft | approved <date, where>
Goal and approved scope: <link to docs/product/... or docs/plans/roadmap.md>
Structure: <link to docs/architecture/...>
| Deliverable | Done when | Role | Waits on | Estimate (range, source) |
|---|---|---|---|---|
| <thing you can open or check> | <checkable> | <role> | <ids, approvals> | <low-high, estimate: builder range / based on N past runs / unknown> |
Milestones: <M1: what is usable at the end>
Critical path: <A -> B -> owner approval -> C>
Owner tasks: <task - date the owner sets>
Project buffer: <about 30 percent, one line, visible>
Value order beside work order: <only where they differ>
```

## 2. Status (`docs/project/status.md`, rebuilt each time)
```markdown
# Status <date and time of the check>    On track | At risk | Blocked (why, with evidence)
Waiting on you: <decision - waiting since <date> - what it unblocks>
Records that disagree: <item - each source says - files support - fix (file, line, text) - owner of the file>
Changed since <last status>: <by owner folder; flags: outside a recorded run, replaced decisions>
Done (with proof): <item - link>   Reported done, not verified: <item>
Blocked: <item - on what>
Top risks: <link to the risk line>
Next: <job - why it can start now>
Checks: drift check <by hand, script not built | command>; change check <how>
```

## 3. Risk line (`docs/project/risks.md`)
`| Risk | Likelihood | Impact | What we do | Owner (role or you) | Checked <date> |`

## 4. Decision line (`docs/project/decisions.md`)
`| Date | Decision (owner's) | Where made (run, review, chat recorded by the boss) | Replaces | Link |`
Architecture decisions are linked to `docs/decisions/`, never copied.

## 5. Release list (`docs/project/releases/<version>.md`)
```markdown
# Release <version> readiness    Build: <version, commit or file set>
| Gate | Owner role | Evidence (link, build it covers) | State |
|---|---|---|---|
| QA go / no-go, open severity 4 bugs | QA / Test Engineer | | met / not met / not met (stale) / unknown / not required (why) |
Recommendation: go | no-go until <shortest list>
Decision: the owner's (returned as an approval)
```

## 6. Retro (`docs/project/retros/<date>-<topic>.md`)
```markdown
# Retro: <topic>    Records read: <list>    Not seen: <what>
Timeline: <date - what happened - link>
Causes (process, no blame): <...>
Actions (1 to 3): <action - proposed owner - check>
Proposed lessons (the boss writes them): <role: what went wrong; the rule that prevents it>
```
