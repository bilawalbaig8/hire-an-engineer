# Recover and review mode: working out the architecture of existing code

When to read this: the project already has code and the request is to understand it, review it, document it, check it for drift, or plan to modernise it.

You will not trust documents over code. Every claim you write carries a label: `verified in code`, `inferred`, or `unknown` (see `core-principles`, section 8). You never claim a component you found no evidence for.

All commands below use only git, the standard shell and the Python standard library. They were run on a small test repository and behave as described. Heavier tools (dependency-cruiser, import-linter, ArchUnit, code-maat) need an install: **ask the boss to ask the owner before installing anything.**

## The six steps

### Step 1: inventory and entry points
Goal: what is here, and every way execution starts.

```bash
git ls-files | sed 's/.*\.//' | sort | uniq -c | sort -rn      # file types
git ls-files | head -100                                        # layout
ls; cat README* 2>/dev/null | head -60                          # first impressions only; verify in code
```
Read build and deploy files: `package.json`, `pyproject.toml`, `requirements.txt`, `pom.xml`, `build.gradle`, `*.csproj`, `go.mod`, `Dockerfile`, `docker-compose.yml`, CI files in `.github/workflows/`, infrastructure files (`*.tf`, `*.yaml`), config and `.env.example` (never print secret values).

Find entry points (things that start work). Patterns by ecosystem:

| Ecosystem | Look for |
|---|---|
| Python | `if __name__ == "__main__"`, `argparse`, `click`, `@app.route`, `@router.`, `FastAPI(`, `Flask(`, `celery`, `manage.py`, files named in `pyproject.toml` scripts |
| JS / TS | `"main"`, `"bin"`, `"scripts"` in `package.json`; `app.listen`, `express()`, Next.js `pages/` and `app/` folders, `export default async function handler`, queue consumers |
| Java / Kotlin | `public static void main`, `@SpringBootApplication`, `@RestController`, `@Scheduled`, `@KafkaListener` |
| C# / Unity | `static void Main`, `Program.cs`, `Startup`, ASP.NET controllers; Unity: scenes in build settings, `MonoBehaviour` with `Awake`/`Start`, `RuntimeInitializeOnLoadMethod`, `[assembly:` definitions and `.asmdef` files |
| Go | `func main()`, `cmd/` folders, `http.HandleFunc` |
| Any | scheduled jobs (cron files, CI schedules), message consumers, webhooks, CLI commands |

```bash
grep -rnE "if __name__ == .__main__.|argparse|@(app|router)\.|app\.(route|get|post)|click\.command" --include=*.py . | grep -v "^./.git"
```
Output of step 1: a list of entry points, each marked `verified in code` with file and line, and a first guess of who and what talks to the system (`inferred` until confirmed).

### Step 2: data model and state
Goal: what is stored, where, and who writes it. Data ownership usually reveals the real module boundaries.

- Find schemas and migrations (`schema.sql`, `migrations/`, ORM models, `*.prisma`, `*.proto`, Unity ScriptableObjects and save files).
- For each table or collection: which module reads it and which writes it (grep for the table name).
- Other state: caches, files, queues, in-memory singletons, remote configuration.
- Output: a data table (store, what it holds, writers, readers). A store with many writers across modules is a boundary smell. [S-REC-5]

### Step 3: static structure (who imports whom)
Goal: layers, cycles, central modules. Treat automatic grouping as a hint, not truth (unverified source S-REC-8 reports low accuracy for automatic clustering). A Dependency Structure Matrix is a useful way to see layers. [S-REC-11]

For Python, this script prints the import edges between your own modules, finds import cycles, and shows the most imported modules. Save as `arch_imports.py` outside the project (or in a temp folder) and run `python arch_imports.py <project folder>`:

```python
import ast, sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SKIP = {".git", "node_modules", "venv", ".venv", "__pycache__", "build", "dist", "site-packages"}
mods = {}
for p in root.rglob("*.py"):
    rel = p.relative_to(root)
    if SKIP & set(rel.parts):
        continue
    parts = list(rel.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    if parts:
        mods[".".join(parts)] = p

def internal(name):
    while name:
        if name in mods:
            return name
        name = name.rpartition(".")[0]
    return None

edges = {m: set() for m in mods}
for m, p in mods.items():
    try:
        tree = ast.parse(p.read_text(encoding="utf-8-sig"))
    except (SyntaxError, UnicodeDecodeError):
        print("skipped (cannot parse):", p)
        continue
    pkg = m if p.name == "__init__.py" else m.rpartition(".")[0]
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            targets = [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            if n.level:
                base = pkg.split(".")[: max(len(pkg.split(".")) - (n.level - 1), 0)] if pkg else []
                mod = ".".join(base + ([n.module] if n.module else []))
            else:
                mod = n.module or ""
            subs = [f"{mod}.{a.name}" for a in n.names if f"{mod}.{a.name}" in mods]
            targets = subs or [mod]
        else:
            continue
        for t in targets:
            t = internal(t)
            if t and t != m:
                edges[m].add(t)

# strongly connected components (Tarjan): any group of 2+ modules is an import cycle
index, low, stack, on, sccs, counter = {}, {}, [], set(), [], [0]
def visit(v):
    index[v] = low[v] = counter[0]; counter[0] += 1
    stack.append(v); on.add(v)
    for w in edges[v]:
        if w not in index:
            visit(w); low[v] = min(low[v], low[w])
        elif w in on:
            low[v] = min(low[v], index[w])
    if low[v] == index[v]:
        comp = []
        while True:
            w = stack.pop(); on.discard(w); comp.append(w)
            if w == v:
                break
        if len(comp) > 1:
            sccs.append(sorted(comp))
sys.setrecursionlimit(10000)
for v in sorted(edges):
    if v not in index:
        visit(v)

print("EDGES (importer -> imported):")
for a in sorted(edges):
    for b in sorted(edges[a]):
        print(f"  {a} -> {b}")
print("CYCLES:", sccs if sccs else "none")
fan_in = {m: sum(m in e for e in edges.values()) for m in mods}
print("FAN-IN (most imported first):", sorted(fan_in.items(), key=lambda kv: -kv[1])[:5])
```

What it sees: imports written in Python files, including imports inside functions. What it misses: dynamic imports, string-based wiring, dependency injection configured elsewhere, other languages. So it is `verified in code` for the edges it prints and `unknown` for what it cannot see. For other languages: read import statements with `grep -rn "^import\|^from\|require(\|using "`, or ask before installing dependency-cruiser (JS/TS) or use ArchUnit (Java). [S-REC-18] [S-REC-17]

Look for: cycles (anything printed under CYCLES), a lower layer importing a higher one (for example a data module importing a request handler), a screen or handler reaching straight into storage while a service layer exists, one module imported by nearly everything (a hidden centre), and modules nobody imports (dead or entry points).

### Step 4: trace real behaviour
Goal: confirm the structure against what actually happens.

Pick 3 to 5 important use cases ("a customer places an order", "the nightly report runs", "a player finishes a level"). For each, follow it from the entry point to the data store, naming each function or module in order, and note what happens on failure. Write each as a short numbered flow (later a sequence diagram). Note what static analysis misses: reflection, events, configuration-driven wiring, message queues, scheduled jobs. If you cannot follow a step, the flow is `inferred` or `unknown` at that step.

### Step 5: history and hotspots
Goal: where change and risk concentrate, and why things are shaped the way they are. Needs git history; **if there is none or it is a single squashed commit, skip this step and say so in the summary.**

Files changed most often (hotspot candidates; confirm that they are also complex before calling them a problem). [S-REC-1]
```bash
git log --diff-filter=M --format= --name-only | grep . | sort | uniq -c | sort -rn | head -15
```
This also works with Windows-friendly Python (standard library only). It prints churn and **change coupling**: files that keep changing together, even across module boundaries, which reveals the real dependencies. Commits touching more than 30 files are ignored (bulk edits, formatting):
```python
import collections, itertools, subprocess

out = subprocess.run(
    ["git", "log", "--no-renames", "--diff-filter=M", "--name-only", "--format=@@%H"],
    capture_output=True, text=True, encoding="utf-8", check=True,
).stdout
commits, cur = [], None
for line in out.splitlines():
    if line.startswith("@@"):
        cur = []; commits.append(cur)
    elif line.strip():
        cur.append(line.strip())

churn = collections.Counter(f for c in commits for f in set(c))
print(f"{len(commits)} commits. HOTSPOT CANDIDATES (files changed most often):")
for f, n in churn.most_common(10):
    print(f"  {n:4d}  {f}")

pairs = collections.Counter()
for c in commits:
    files = sorted(set(c))
    if 2 <= len(files) <= 30:
        pairs.update(itertools.combinations(files, 2))
print("CHANGE COUPLING (share = pair commits / commits of the rarer file):")
for (a, b), n in pairs.most_common(8):
    print(f"  {n:3d} together  {n / min(churn[a], churn[b]):.0%}  {a}  <->  {b}")
```
Run it from the project folder. Treat small numbers with care: a pair that changed together twice is a hint, not a finding.

Why-archaeology: find when something appeared and what the author said.
```bash
git log -S"some_function_name" --oneline -- path/to/file     # commits that added or removed this text
git log --follow --oneline -- path/to/file                   # history of one file across renames
git blame -L 10,30 path/to/file                              # who last changed these lines, in which commit
```
These are standard git features (the official page was not fetched during research, so cite git's own help, `git help log`, rather than a source ID). A decision you reconstruct this way is written as an ADR with `Status: inferred` and the commit hashes as evidence. [S-REC-14]

### Step 6: hypothesise, check, and write it up
1. Write down the architecture you *think* the authors intended (boxes, allowed arrows, which folders belong to which box). This is a reflexion model (unverified source S-REC-7 describes the idea).
2. Compare it with the real edges from step 3. Each difference is either **erosion** (the code drifted from the intent) or a **wrong hypothesis** (your guess was off). Say which, with evidence. [S-REC-9]
3. For rules worth keeping, propose automated checks (import rules, no-cycles) so drift is caught in future; write them only when the owner asks. [S-REC-17] [S-REC-18]
4. Write the result (below).

## What to write

```
docs/architecture/overview.md       C4 context + container view and an arc42-style summary (see method-design)
docs/architecture/diagrams/         sources + rendered images; mark inferred links dashed
docs/architecture/conformance.md    intended vs actual table (below)
docs/architecture/risks.md          risks in ATAM style, plus drift risks [S-FND-15]
docs/decisions/NNNN-title.md        inferred decisions, Status: inferred, with evidence
```
Conformance table:

| Intended rule or boundary | What the code does | Evidence (file:line, command) | Label | Erosion or wrong guess |
|---|---|---|---|---|

Every row, every box and every arrow in your output carries a label (`verified in code`, `inferred`, `unknown`). Include a short "Not covered" list (what you did not read, what the scripts cannot see).

## Fallbacks

- **No git history:** skip step 5, say hotspots and change coupling were not analysed, and still label everything.
- **Huge repo or monorepo:** do not read everything. Take each entry point and the top 10 hotspots, trace one use case through each, and say what was sampled. Treat each top-level app or package as one container first.
- **Unfamiliar language:** use the entry-point table and build files to find the main folders, read a few central files, use `grep` for imports, and label more things `inferred`.
- **Generated or vendored code:** list it and exclude it from the graph.
- **Cannot run anything:** work from reading only, and mark every runtime claim `inferred`.

## If you are asked to modernise
Propose the strangler-fig approach: put a thin entry point in front of the old system, move one slice at a time behind it, keep both running, and retire the old slice when the new one proves itself. State when it does not fit (cannot intercept requests, tiny system, must decommission quickly). [S-REC-12] [S-REC-13] [S-WEB-7] Each slice move is a decision record; moves that cannot be undone go back as approvals.

## Sources
[S-FND-15] [S-REC-1] [S-REC-5] [S-REC-9] [S-REC-11] [S-REC-12] [S-REC-13] [S-REC-14] [S-REC-17] [S-REC-18] [S-WEB-7]
