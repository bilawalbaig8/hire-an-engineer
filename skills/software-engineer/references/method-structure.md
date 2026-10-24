# Structure mode: apply the Architect's plan

When to read this: the request is to create a project tree, set up the folders and a first skeleton, check names against the naming rules, or fix names and places in an existing project. The plan is the Architect's. You apply it; you never design it.

## What the plan is (the Architect's files)
The Architect's Project structure mode writes these files in the project (the Architect's own references: `software-architect/references/method-structure.md`, `software-architect/references/structure-trees.md`, `software-architect/references/naming-rules.md` and `software-architect/references/data-structures.md`):
| File | What you take from it |
|---|---|
| `docs/architecture/structure.md` | Each top folder with its purpose, owner role, what goes in and what never goes in; the organisation rule (feature-first or layer-first) and its trigger; the limits (default 4 folder levels, about 20 files per folder, about 400 lines per file; team heuristics, a project may change them); homes for tests, docs, assets, config, scripts and generated files; the "core data" section |
| `docs/architecture/tree.txt` | The target tree as plain text, one comment per folder. This is the list you build from. In an audit it starts with the "before" tree |
| `docs/architecture/naming.md` | The naming table for this project; which names are public paths |
| `docs/architecture/restructure-plan.md` | Audit only: numbered small steps, each with files touched, a check, a way back, a size and the role that applies it |
| `docs/decisions/` | Records for data structure and algorithm choices: size now and at 10 times, the simple default, what was chosen, what must be measured, the trigger to revisit |
If the project keeps its design in `docs/design/` instead, read there. A file the Architect did not write (for example an old `AGENTS.md` folder map) is a hint, not the plan. The plan format is the Architect's; do not invent a format of your own. If the files do not exist, see "No plan" below.

## No plan
- A single script or one-folder tool needs no tree: build it in the place the brief names.
- Anything with more than one folder: return `needs_answers` asking for the Architect's plan through the boss. Do not invent a structure and do not move anything. You may describe what you found, labelled as observation.
- An engine project (Unity, Unreal, Godot): moves need the editor (meta files, GUIDs, redirectors). Return it to the boss for the Game & Technical Engineer.

## Scaffold (a new tree)
1. Read the three plan files. List the forced folders first (they keep their names and places). Note the owner role of each folder: a folder owned by another role (for example `.github/workflows/`, `infra/`, `pipelines/`, `tests/e2e/`) is created empty-of-content only if the plan lists a first file, and its content stays with that role.
2. Read the project's brief for the folders you may write in. Never write outside them.
3. Dry run: print the list of folders and files you would create (path and one-line purpose each). Compare with `tree.txt`: anything not in the plan is dropped and listed as a question for the Architect (for example a `utils/` folder asked for in the brief but absent from the plan).
4. Create exactly that tree. No empty "future" folders: a folder exists when its first file exists. Never overwrite an existing file; if one is there, report it and skip.
5. Use a built-in or standard layout where the plan names one (S-SE-32 for the Python `src` layout, S-SE-34 for a Go module). Write your own small steps; do not install a template tool (S-SE-33 is background only).
6. Skeleton files: a header comment saying what the file is for, one placeholder test per code folder that the plan says has tests, and the test runner config the plan names. Nothing that looks like working features.
7. Run the placeholder test from a clean folder (a fresh checkout or copy). Run the naming check (below).
8. Write the layout note (`templates.md` section 1) in `docs/software-engineering/structure/`.
9. Answer in the 7-field shape. Evidence: the dry-run list, the test command and result, the naming check output.

## The naming check (by hand until the script exists)
There is no naming script yet. Check names with the shell and the plan's `docs/architecture/naming.md`:
- List every folder and file name (`git ls-files`, or a folder listing for a project without Git).
- Compare each against the row for its kind (folder, file by language, module, asset). Count: "212 of 220 files follow the rule".
- Report each violation with its path, the rule it breaks and the name the rule would give.
- Names the plan does not cover are not violations: list them as "not covered by the rules" for the Architect.
- The language's own guide wins where the naming file points at it (S-SE-35 for Python names).
Say in the answer that the check was done by hand and how (the command), and give the counts.

## Conform (an existing project)
1. Run the existing tests first. Their result is the baseline. If they do not run, say so; renames then have no safety net, which makes each rename a bigger approval.
2. Run the naming check. List the violations.
3. For each violating name, find every reference: imports, test files, config files, build and deploy files (a `Procfile`, a workflow file, a scheduled task), docs and links. Search for the old name as text and as a path. The list must say how each reference was found and what could hide others (dynamic imports, names built from strings, files outside the repo).
4. Names that other code, other repositories, players or saved data depend on are public paths (package import paths, URLs, asset addresses, save file names, event names). Changing them is a one-way door: return an approval with a forwarding step (re-export, alias, redirect, read-old-write-new for saves).
5. Return the rename list as `needs_approval` (`templates.md` section 4). No rename happens before the approval.
6. After the approval: work on a branch. One move or one rename rule per commit, with `git mv` and no content change in that commit; the imports and config updates in the next commit. Run the tests after each step and keep the same result as the baseline.
7. Never touch files owned by another role while updating references (a deploy file is DevOps's, a server file is the Backend's): list the reference and return it as a question or an approval for the owner of the file.
8. After the last step: run the naming check again; the number of violations must be what the approval allowed (usually 0). Write the layout note.

## Plan and code disagree
The plan says one thing and the real code another (for example the plan says `app/services/` and the code is in `server/handlers/`, and a deploy file points at `server/`). Do not follow the plan blindly and do not bend it. Report the conflict with file evidence (paths and lines), move nothing, and return a question for the Architect through the boss. A working entry point is never broken to match a plan.

## Done when
- Scaffold: the tree equals `tree.txt` (compare with a listing), the placeholder test passes from a clean folder, the naming check says 0 violations or lists each one, the layout note is written, extra requests are returned as questions.
- Conform: every violation has its references listed, the approval is returned, nothing was renamed before it, and the baseline test result is in the evidence.
- Both: no file outside the named folders changed (say how you know, for example `git status`), and "Code Reviewer review pending".
