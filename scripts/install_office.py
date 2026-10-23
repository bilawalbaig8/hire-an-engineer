"""Put the virtual office into any project folder (next to the team from install_agents.py).

Copies the office runtime into <DIR>/.agents/office/ (stdlib only), merges the hooks and the deny rule into
<DIR>/.claude/settings.json (and, only with --with-mcp, adds an `office` entry to <DIR>/.mcp.json). Never touches anything outside DIR,
never deletes or overwrites existing settings keys, never adds allow or ask rules (it prints them as optional lines).
A file that differs from the shipped copy is not overwritten unless --force is given.
Usage: python scripts/install_office.py --project DIR [--dry-run] [--force] [--with-mcp]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OFFICE_REL = Path(".agents") / "office"
SCRIPTS = ("office_server.py", "office_launch.py", "office_mcp.py", "log_event.py", "agent_contract.py", "check_roster.py")
# (source relative to the repo, destination relative to .agents/office/)
FILES = [(Path("scripts") / n, Path(n)) for n in SCRIPTS] + [
    (Path("docs/agents/roster.md"), Path("roster.md")),
    (Path("docs/agents/visual-office/index.html"), Path("ui/index.html")),
    (Path("docs/agents/visual-office/mock-v2.html"), Path("ui/mock-v2.html")),
]
PROJ = "${CLAUDE_PROJECT_DIR}"
LOG_CMD = f'python "{PROJ}/.agents/office/log_event.py"'
LAUNCH_CMD = f'python "{PROJ}/.agents/office/office_launch.py"'
HOOKS = {  # event -> (matcher or None, command, async)
    "SubagentStart": (None, LOG_CMD, False),
    "SubagentStop": (None, LOG_CMD, False),
    "PostToolUse": ("Write|Edit", LOG_CMD, False),
    "SessionStart": ("startup", LAUNCH_CMD, True),
}
DENY_DEFAULT = ["Edit(/.agents/**)", "Write(/.agents/**)", "NotebookEdit(/.agents/**)"]
MCP_ENTRY = {"type": "stdio", "command": "python",
             "args": ["${CLAUDE_PROJECT_DIR:-.}/.agents/office/office_mcp.py"], "timeout": 3600000}


@dataclass
class Item:
    kind: str  # new | same | differs | merged | conflict
    label: str
    src: Path | None = None
    dst: Path | None = None
    text: str | None = None  # full new text for a JSON file


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except ValueError as e:
        raise ValueError(f"{path} is not valid JSON ({e}); fix it first, nothing was changed") from e
    if not isinstance(data, dict):
        raise ValueError(f"{path} must hold a JSON object; nothing was changed")
    return data


def _dump(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def _snippet_permissions(src_root: Path) -> dict:
    try:
        perms = json.loads((src_root / "docs/agents/permissions-snippet.json").read_text(encoding="utf-8"))["permissions"]
        return perms if isinstance(perms, dict) else {}
    except (OSError, ValueError, KeyError):
        return {}


def _deny_rules(src_root: Path) -> list[str]:
    rules = [r for r in _snippet_permissions(src_root).get("deny", []) if isinstance(r, str)]
    return rules or DENY_DEFAULT


def _optional_lines(src_root: Path) -> list[str]:
    perms = _snippet_permissions(src_root)
    return [f"allow: {r}" for r in perms.get("allow", [])] + [f"ask:   {r}" for r in perms.get("ask", [])]


def merge_settings(data: dict, deny: list[str]) -> tuple[dict, list[str]]:
    """Add the office hooks and deny rules to a settings dict; returns (dict, list of what was added)."""
    added: list[str] = []
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("settings.json: 'hooks' is not an object; nothing was changed")
    for event, (matcher, cmd, is_async) in HOOKS.items():
        groups = hooks.setdefault(event, [])
        if not isinstance(groups, list):
            raise ValueError(f"settings.json: hooks.{event} is not a list; nothing was changed")
        present = any(
            isinstance(g, dict) and any(isinstance(h, dict) and h.get("command") == cmd for h in g.get("hooks", []) or [])
            for g in groups
        )
        if present:
            continue
        hook = {"type": "command", "command": cmd}
        if is_async:
            hook["async"] = True
        groups.append({"matcher": matcher, "hooks": [hook]} if matcher else {"hooks": [hook]})
        added.append(f"hook {event}")
    perms = data.setdefault("permissions", {})
    if not isinstance(perms, dict):
        raise ValueError("settings.json: 'permissions' is not an object; nothing was changed")
    denied = perms.setdefault("deny", [])
    if not isinstance(denied, list):
        raise ValueError("settings.json: permissions.deny is not a list; nothing was changed")
    for rule in deny:
        if rule not in denied:
            denied.append(rule)
            added.append(f"deny {rule}")
    return data, added


def plan(src_root: Path, project: Path, with_mcp: bool = False) -> list[Item]:
    items: list[Item] = []
    office = project / OFFICE_REL
    for rel_src, rel_dst in FILES:
        src, dst = src_root / rel_src, office / rel_dst
        if not src.is_file():
            if rel_dst.name == "mock-v2.html":  # optional fallback page
                continue
            raise FileNotFoundError(f"missing in the repo: {src}")
        kind = "new" if not dst.exists() else ("same" if _digest(src) == _digest(dst) else "differs")
        items.append(Item(kind, (OFFICE_REL / rel_dst).as_posix(), src, dst))
    # settings.json
    sp = project / ".claude" / "settings.json"
    existing = _load_json(sp)
    data, added = merge_settings(existing if existing is not None else {}, _deny_rules(src_root))
    if existing is None:
        items.append(Item("new", ".claude/settings.json (hooks + deny rule)", dst=sp, text=_dump(data)))
    elif added:
        items.append(Item("merged", f".claude/settings.json: added {', '.join(added)}", dst=sp, text=_dump(data)))
    else:
        items.append(Item("same", ".claude/settings.json", dst=sp))
    if not with_mcp:  # window answers are off: no MCP server unless asked for
        return items
    # .mcp.json
    mp = project / ".mcp.json"
    mdata = _load_json(mp)
    servers = (mdata or {}).get("mcpServers", {})
    if not isinstance(servers, dict):
        raise ValueError(".mcp.json: 'mcpServers' is not an object; nothing was changed")
    if mdata is None:
        items.append(Item("new", ".mcp.json (office server)", dst=mp, text=_dump({"mcpServers": {"office": MCP_ENTRY}})))
    elif "office" not in servers:
        mdata.setdefault("mcpServers", {})["office"] = MCP_ENTRY
        items.append(Item("merged", ".mcp.json: added mcpServers.office", dst=mp, text=_dump(mdata)))
    elif servers["office"] == MCP_ENTRY:
        items.append(Item("same", ".mcp.json", dst=mp))
    else:
        items.append(Item("conflict", ".mcp.json: an 'office' entry already exists and was left as it is", dst=mp))
    return items


def install(src_root: Path, project: Path, force: bool = False, dry_run: bool = False, with_mcp: bool = False) -> int:
    if not project.is_dir():
        raise NotADirectoryError(f"project folder not found: {project}")
    items = plan(src_root, project, with_mcp=with_mcp)
    for it in items:
        if it.kind != "same":
            print(f"{it.kind} {it.label}")
    counts = {k: sum(1 for i in items if i.kind == k) for k in ("new", "same", "differs", "merged", "conflict")}
    print(", ".join(f"{n} {k}" for k, n in counts.items()))
    if all(i.kind == "same" for i in items):
        print("all same: nothing to do")
    if dry_run:
        return 0
    differing = [i.dst for i in items if i.kind == "differs"]
    if differing and not force:
        listing = "\n".join(f"  {p}" for p in differing)
        raise FileExistsError(f"{len(differing)} file(s) differ and were not overwritten (use --force):\n{listing}")
    written = 0
    for it in items:
        if it.kind in ("same", "conflict") or it.dst is None:
            continue
        it.dst.parent.mkdir(parents=True, exist_ok=True)
        if it.text is not None:
            it.dst.write_text(it.text, encoding="utf-8", newline="\n")
        else:
            shutil.copy2(it.src, it.dst)
        written += 1
    return written


def next_steps(src_root: Path) -> str:
    lines = [
        "",
        "Next steps",
        "  Start the team:   claude --agent orchestrator   (the office window opens by itself)",
        "  Open the window:  python .agents/office/office_launch.py --status   (prints http://127.0.0.1:<port>/)",
        "  Stop it:          python .agents/office/office_launch.py --stop",
        "  Headless runs (claude -p) need: --allowedTools \"Bash(python .claude/skills/orchestrator/scripts/team_event.py:*)\"",
        "  Optional permission lines (not added for you; add them to .claude/settings.json yourself if you want them):",
    ]
    lines += [f"    {x}" for x in _optional_lines(src_root)]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--project", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--with-mcp", action="store_true",
                   help="also add the office MCP server to .mcp.json (only needed when window answers are switched on)")
    args = p.parse_args(argv)
    try:
        install(REPO_ROOT, args.project.resolve(), force=args.force, dry_run=args.dry_run, with_mcp=args.with_mcp)
    except FileExistsError as e:
        print(e, file=sys.stderr)
        return 1
    except (ValueError, OSError) as e:
        print(e, file=sys.stderr)
        return 2
    print(next_steps(REPO_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
