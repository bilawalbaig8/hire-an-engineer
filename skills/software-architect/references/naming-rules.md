# Naming rules: the table, per-language notes, assets and versions

When to read this: Project structure mode, when you write `docs/architecture/naming.md` for a project, or check names during an audit. (This file is named `naming-rules.md` so it is never confused with the project output `docs/architecture/naming.md`.)

## 1. Which rule wins
1. **An existing, consistent convention in the project wins.** If the files already follow one style (for example `camelCase` JavaScript file names), keep it and write rules only for the gaps. Continue, do not overwrite. Count before you call a convention consistent ("212 of 220 files use it").
2. **Then the language's own guide.** Each language gets its own rules; never force one casing on two languages (linters will fight it).
3. **Then the team defaults below.**
4. **Never contradict the base skill:** branch names and commit messages (`hire-an-engineer/references/github.md`), the Unity repo rules and semantic versioning (`hire-an-engineer/references/technical-products.md`).

A mass rename to "fix" names is a restructure step with a cost (merge conflicts in open branches, broken links, lost history if done badly); plan it in `docs/architecture/restructure-plan.md`, never do it.

## 2. The default table (copy into the project's `docs/architecture/naming.md` and trim)
| Thing | Default rule |
|---|---|
| Folders | lower-case, one word or `kebab-case`; Unity and C# folders `PascalCase`; Godot `snake_case` [S-STR-17] |
| Files | the language's guide (section 3) |
| Modules and packages | short, lower-case nouns that name a feature or area; never `utils`, `misc` or `helpers` alone |
| Types, functions, variables | the language's casing (section 3); functions are verbs, types are nouns, booleans read as questions (`is_paid`, `isPaid`) |
| Branches | `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `chore/<topic>`, `wip/<topic>` (base skill `hire-an-engineer/references/github.md`) |
| Commits | Conventional Commits: `type(scope): description`, for example `feat: add order form` [S-STR-11] |
| Assets | `<kind>_<name>_<variant>` (for example `spr_coin_gold`, `sfx_coin_pickup`); no spaces [S-STR-13] |
| Versions | Semantic Versioning `MAJOR.MINOR.PATCH`; tags `v1.2.3` (or `<skill>-v<version>` in this repo) [S-STR-12] |
| Never in a name | "final", "new", "old", "copy", "v2" for a file that replaces another; dates in source file names |

## 3. Per-language notes
| Language | Files | Types | Functions and variables | Source |
|---|---|---|---|---|
| Python | `snake_case.py`; modules short and lower-case | `CapWords` classes | lower-case with underscores | [S-STR-6] |
| TypeScript / JavaScript | the project's existing style; if none, the Google guide (its own file names are `snake_case`); many projects use `kebab-case`: pick one and write it down | `UpperCamelCase` classes, interfaces, types | `lowerCamelCase`; `CONSTANT_CASE` for global constants | [S-STR-7] |
| C# / .NET / Unity | `PascalCase.cs`, one main type per file, file named after the type | `PascalCase` | `PascalCase` public members; the casing rules matter most for public APIs | [S-STR-8] |
| Go | lower-case package names, short, no underscores | exported names start upper-case | unexported start lower-case | [S-STR-10] (layout); the Go naming rules themselves were not checked in this pass, so say "inferred" |
| Rust | `snake_case` modules and files | `UpperCamelCase` | `snake_case` | [S-STR-9] |
| Godot (GDScript) | `snake_case` files and folders; C# scripts named after their `PascalCase` class | `PascalCase` nodes | the language's own guide | [S-STR-17] |

When a language is not in this table, read its official style guide (documentation only) and label the rule with where it came from.

## 4. Assets and keys that are public paths
- Asset file names follow the asset rule; the folder says the area (`Art/Characters/`).
- **Keys that code or players depend on are public paths:** Addressables addresses, asset IDs, localisation keys, save file names and locations, URLs, package import paths, event names sent to analytics. Changing them is a **one-way door**: return it as an approval with a forwarding step (a redirect, a re-export, an alias, a read-old-write-new step for saves).
- Unity: an asset moved or renamed outside the editor without its `.meta` file loses its references. Renames in Unity happen inside the editor, by the Game & Technical Engineer (role not built yet; the boss routes it).

## 5. Versions and releases
- Semantic Versioning: MAJOR for a breaking change, MINOR for a compatible feature, PATCH for a compatible fix [S-STR-12]. Conventional Commits types map onto these (`fix` to PATCH, `feat` to MINOR) [S-STR-11].
- A save format, a network message or a file format carries its own version field (see `data-structures.md` section 4).
- Never mark versions in file names; use tags and the changelog.

## 6. Writing `docs/architecture/naming.md` for a project
1. Count the current names (audit) or read the stack (new tree).
2. Keep what is consistent; write the language rules for what is missing.
3. One table, one page. Each row: the thing, the rule, one good example, one bad example.
4. Say which names are public paths and must not change without an approval.
5. Propose a naming check only when the owner asks; the Software Engineer (not built yet) writes it, DevOps runs it.

## Sources
[S-STR-6] [S-STR-7] [S-STR-8] [S-STR-9] [S-STR-10] [S-STR-11] [S-STR-12] [S-STR-13] [S-STR-17]
