# Structure trees: skeletons by stack, limits and where files go

When to read this: Project structure mode (`method-structure.md`), when you draw a target tree for a new project or for an audit. Not needed for System design or Data design.

The numbers in this file (depth, files per folder, lines per file, the switch points for feature-first) are **team heuristics, not sourced facts**. A project may change them in its `docs/architecture/structure.md`; say so when you change them.

## 1. How a tree is derived (never copied from a template)
1. **Forced folders first.** List what the framework or engine requires (route folders, engine folders, reserved names, manifests). They keep their names and places. Never move or rename them.
2. **One folder per feature or bounded area**, taken from the System design boundaries and the feature list. The top of the tree should say what the product does, not which framework it uses [S-STR-1].
3. **`shared/` only for code that two or more features use.** Nothing goes there "in case".
4. **Adapters for outside services** (payments, email, analytics, store APIs) in one place, one folder per provider.
5. **Homes for tests, docs, assets, config, scripts and generated files** by section 4.
6. **One purpose and one owner role per folder.** Never "everyone". The owner column comes from the team roster; a role that is not built yet is still named, with "not built yet".

## 2. Limits (team heuristics; changeable per project)
| Limit | Default | What it signals when broken |
|---|---|---|
| Depth below the source root | at most 4 folder levels (for example `src/features/booking/server/`) | a missing boundary, or a template copied whole |
| Files per folder | split at about 20 files | the folder holds more than one idea |
| Lines per file | flag a file over about 400 lines, or one that mixes concerns | a hidden module; a hotspot candidate (`method-recover.md` step 5) |
| Empty folders | none | a folder is created when its first file is; empty "future" folders fill with junk |
| Root files | only memory and config: `AGENTS.md`, `CLAUDE.md`, `PROJECT_STATE.md`, `README.md`, `CHANGELOG.md`, `.gitignore`, `.env.example`, the package manifest and framework config | stray scripts and notes at the root |

## 3. Feature-first or layer-first
| Option | Gives | Gives up |
|---|---|---|
| Flat or layer-first (`controllers/`, `services/`, `models/`) | Easy start; matches tutorials | One change touches every layer folder; folders grow without limit; boundaries are invisible |
| Feature-first (by feature, component or vertical slice) | A change stays in one folder; a feature can be deleted whole; a clear owner; the tree says what the product does [S-STR-3] [S-STR-4] | Shared code needs a home and a rule; a feature needs a public entry for other features |
| Hexagonal or clean layers inside each feature | Outside services can be swapped; the core can be tested alone | More files and indirection; worth it only where an outside service or a core rule needs isolation [S-FND-5] |

Decision rule:
- **Flat or layer-first is fine** for a tiny project (under about 10 source files, one feature) and wherever the framework imposes layers.
- **Feature-first** once there are 3 or more features or about 20 source files. Inside a feature a few layer files are fine (`ui`, `server`, `model`).
- **Write the trigger** in `docs/architecture/structure.md` ("move to feature-first at the third feature").

Rules inside the tree: `shared/` takes code only when a second feature needs it; a feature imports another feature only through its public entry; no import cycles between top folders. These rules can be made checkable (import-linter, dependency-cruiser, Unity assembly definitions) [S-REC-19] [S-REC-18] [S-GAME-37]; the Architect designs the rule, and only when the owner asks is it written (Software Engineer, role not built yet) and run in CI (DevOps) (`core-principles.md` section 6).

## 4. Where each kind of file goes
| Kind of file | Default home | Notes |
|---|---|---|
| Unit tests | Follow the language: next to the code (`*.test.ts`, Go `_test.go`), or a `tests/` tree that mirrors `src/` (Python), or a test assembly (Unity `Tests/EditMode`, `Tests/PlayMode`; a C# test project) | The builder of the code owns its unit tests |
| End-to-end tests | `tests/e2e/` | QA / Test Engineer |
| Docs | `docs/<role folder>/` | One owner per folder |
| Assets | The engine's or framework's folder (`Assets/<Game>/Art`, `public/`, `res/`) | Big binaries in Git LFS (base skill rule) |
| Config | Framework config at the root or in `config/`; committed defaults only | Never secrets; `.env.example` holds names only |
| Scripts | `scripts/`, each with a header comment saying what it does | Base skill rule |
| Generated files | Never committed: `build/`, `dist/`, `coverage/`, `node_modules/`, `.venv/`, Unity `Library/`, `Temp/`, `Logs/`, Unreal `Binaries/`, `Intermediate/`, `Saved/`; all in `.gitignore` | Generated code that must be committed lives in one `generated/` folder with a "do not edit" header and the command that makes it |
| CI and infrastructure | `.github/workflows/`, `infra/` | DevOps Engineer writes them |
| Pipelines | `pipelines/` | The Data Engineer designs the inside |
| Database migrations | the project's migrations folder | Backend Engineer writes the files; the Architect writes only migration plans in `docs/data/` |

## 5. Skeletons by stack
Each skeleton lists forced folders first. Comments say what goes in. Adjust names to the project's features; never add a folder that has no file yet.

**Web app (Next.js or similar).** Forced: `app/` (routes), `public/` (static files); `src/` is optional [S-STR-19]. Next.js is otherwise unopinionated, so feature folders are our choice.
```
app/                      # routes only: page, layout, route files; thin, calls features
public/                   # static files served as they are
src/features/<name>/      # one folder per feature: ui, server, model files
src/shared/               # code used by two or more features
src/integrations/<provider>/   # adapters for outside services
tests/e2e/                # end-to-end tests (QA)
```

**Backend service.** Forced: the language's module root (Go module; Python package). Go starts at the module root and grows `cmd/` and `internal/` [S-STR-10]; Python uses the `src/` layout [S-STR-5].
```
<pkg>/features/<name>/    # or <pkg>/<area>/: handlers, logic, model per feature
<pkg>/adapters/           # outside services, one folder per provider
migrations/               # Backend Engineer writes the files
tests/                    # mirrors the package (Python)
```

**Unity game.** Forced: `Assets/`, `Packages/`, `ProjectSettings/`; reserved names `Editor/`, `Resources/`, `StreamingAssets/`, `Plugins/` used only for their purpose [S-STR-14]. Keep your own content apart from third-party content, and no spaces in names [S-STR-13].
```
Assets/<Game>/Code/<Area>/    # one assembly definition per area; dependencies point one way
Assets/<Game>/Art/            # sprites, models, materials
Assets/<Game>/Audio/
Assets/<Game>/Scenes/
Assets/<Game>/Tests/          # EditMode and PlayMode test assemblies
Assets/ThirdParty/            # store and plugin content, kept apart
```
Moves happen inside the editor, or each `.meta` file moves with its file; otherwise references break.

**Unreal or Godot.** Unreal forced: `Source/`, `Content/`, `Config/`; `Binaries/`, `Intermediate/`, `Saved/` are generated [S-STR-16]. Add `Content/<Game>/<Area>/`. Godot: `project.godot` at the root; keep scene, script and assets of one thing together, snake_case names, third-party in `addons/` [S-STR-17].

**Mobile (Android or cross-platform).** Forced: the platform's module and resource folders. Add feature modules (`feature/<name>`) and shared core modules, each with a clear purpose and owner [S-STR-18].

**Python tool.** Forced: `pyproject.toml`. Add `src/<package>/` (src layout, so tests run against the installed copy) [S-STR-5], `tests/`, `scripts/`.

**Plugin or extension.** Forced: the host's manifest and entry (VS Code `package.json` with its `main` entry and an activate function [S-STR-20]; Unity package `package.json`, `Runtime/`, `Editor/`, `Tests/` [S-STR-15]; a Claude Code plugin manifest). Feature folders go inside the host's layout only.

**Monorepo.** Forced: the package manager's workspace file. Add `apps/<name>/`, `packages/<name>/`, `tools/`. No extra monorepo tool until a measured trigger (build time, many packages) [S-STR-21]; the tool site is written by a tool maker, so weigh it. One repository gives one source of truth but needs tooling at very large scale [S-STR-22].

## 6. One repo or several
Splitting into several repositories, or merging them, is costly to undo (history, tooling, access, release flow). Return it as an approval with a recommendation and what each option gives up; never decide it alone. Default recommendation for a small team: one repository with a workspace, and a written trigger for splitting.

## 7. Owners in the tree (team defaults)
| Folder kind | Owner role |
|---|---|
| Feature and shared code (general) | Software Engineer applies the tree (not built yet); the feature's builder writes inside it |
| Server, adapters, migrations | Backend Engineer |
| Engine project (Unity, Unreal, Godot) | Game & Technical Engineer applies the tree (not built yet) |
| `tests/e2e/` | QA / Test Engineer |
| `.github/workflows/`, `infra/` | DevOps Engineer (not built yet) |
| `pipelines/` | Data Engineer (not built yet) |
| `docs/architecture/`, `docs/decisions/`, `docs/data/` | Solution Architect |

## Sources
[S-STR-1] [S-STR-3] [S-STR-4] [S-STR-5] [S-STR-10] [S-STR-13] [S-STR-14] [S-STR-15] [S-STR-16] [S-STR-17] [S-STR-18] [S-STR-19] [S-STR-20] [S-STR-21] [S-STR-22] [S-FND-5] [S-GAME-37] [S-REC-18] [S-REC-19]. Package by component (S-STR-2, unverified) and Conway's law (S-STR-24, unverified) are leads only.
