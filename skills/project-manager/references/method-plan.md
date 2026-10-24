# Plan mode

## 1. When to read this
The request asks for a plan: "make a plan for version 1", who does what and in which order, "can QA start now, at the same time as Backend?", or a date for a client.

## 2. Steps
1. **Link the inputs.** The approved scope (`docs/product/`, or `docs/plans/roadmap.md` / `docs/project.md` from the `hire-an-engineer` layout) and the structure (`docs/architecture/`, `docs/decisions/`). Link, never copy. Anything not approved by the owner is marked `draft`.
2. **Break the work down by deliverable**, never by activity: each line is a thing that can be opened or checked, with a done-when and the role that can make it (S-PM-6). Use the task fields of `hire-an-engineer/references/project-management.md` (section 3). Who does it on the owner's team: "who: you decide".
3. **Milestones** end in something usable; the thinnest end-to-end version first (S-PM-4).
4. **Dependencies and the critical path.** Which deliverable waits on which, including waits on an approval that is not given yet; the longest chain of waiting work is the critical path (S-PM-7). The owner's own tasks and approvals sit on that path as real tasks, with dates the owner sets.
5. **Estimates** (rule 2 of `SKILL.md`). Sources in this order: the builders' own ranges through the boss; past runs of the same kind in this project's records (start and end in `.agents/events.jsonl` or the run folders), with the count of runs used and the words "based on N past runs" (S-PM-12, S-PM-17); otherwise `unknown`. Ranges, never points (S-PM-14). Ask for missing builder ranges through the boss.
6. **Buffer.** About 30 percent, from `hire-an-engineer/references/project-management.md` (section 5), kept as one visible project buffer at the end of the chain, not hidden in each task (S-PM-21).
7. **Pre-mortem.** "It is later and this plan failed; why?" Write the likely reasons and seed `docs/project/risks.md` (S-PM-10, S-PM-11).
8. **Value order beside work order.** When the Product & Business Analyst's value order and the dependency order differ, show both; never treat the value order as the work order.
9. **Return the plan** as `needs_approval`. A date for a client or the public is a separate approval with `one_way_door: true`, given as a range with the risks behind it.

## 3. Traps
- **No effort numbers in the files:** write `unknown` and ask for ranges; never invent one.
- **"Give the backend to Ali and message them":** list the work package with "who: you decide"; send nothing; put no names on tasks.
- **"Start QA now in parallel":** show what QA needs first and what waits on an approval not yet given; give options; the owner decides.
- **"Promise the client 1 December":** a range with buffer and risks, and the date returned as a one-way-door approval.

## 4. Done when
`docs/project/plan.md` exists; every deliverable has a role, a done-when and its dependencies; every number is a range marked "estimate" with its source, or `unknown`; the owner's tasks are in; risks are seeded; the plan is returned for approval.
