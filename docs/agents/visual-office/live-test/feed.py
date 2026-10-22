#!/usr/bin/env python3
"""Append a sample log to a project's .agents/events.jsonl one line at a time, like a real run.

  python feed.py normal-run.events.jsonl C:/tmp/office-project --delay 1.5

Every line gets the current UTC time as `ts`. A line `#wait-answer ID` in the sample makes
this script wait until the window has written an answer for ID to .team/inbox.jsonl (what the
office server does for POST /answer) and then log the matching `approval_given` with
by="window", the way the Boss would. If nothing arrives in --answer-timeout seconds it logs the
sample's own answer with by="terminal". A follow-up question from the window gets a canned
`boss_reply` and the wait continues. Test helper only; not part of the product.
"""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def inbox_entries(path: Path) -> list[dict]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out = []
    for ln in lines:
        try:
            v = json.loads(ln)
        except ValueError:
            continue
        if isinstance(v, dict):
            out.append(v)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sample")
    ap.add_argument("project")
    ap.add_argument("--delay", type=float, default=1.5, help="seconds between lines (default 1.5)")
    ap.add_argument("--answer-timeout", type=float, default=120.0)
    ap.add_argument("--append", action="store_true", help="keep the existing log instead of starting empty")
    args = ap.parse_args()

    project = Path(args.project)
    events = project / ".agents" / "events.jsonl"
    inbox = project / ".team" / "inbox.jsonl"
    events.parent.mkdir(parents=True, exist_ok=True)
    if not args.append:
        events.write_text("", encoding="utf-8")

    def write(ev: dict) -> None:
        with open(events, "a", encoding="utf-8", newline="") as f:
            f.write(json.dumps(ev) + "\n")

    answered: dict[str, dict] = {}
    run_id = "feed"
    seen_inbox = len(inbox_entries(inbox))
    for raw in Path(args.sample).read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith("#wait-answer"):
            ident = raw.split(None, 1)[1].strip()
            print(f"waiting for an answer to {ident} (timeout {args.answer_timeout:.0f}s)", flush=True)
            deadline = time.time() + args.answer_timeout
            while time.time() < deadline:
                entries = inbox_entries(inbox)
                new, seen_inbox = entries[seen_inbox:], len(entries)
                hit = [e for e in new if str(e.get("id")) == ident]
                if not hit:
                    time.sleep(0.5)
                    continue
                entry = hit[-1]
                if str(entry.get("answer", "")).startswith("question:"):
                    write({"ts": now(), "type": "boss_reply", "agent": "orchestrator", "run_id": run_id, "id": ident,
                           "text": "I will check with the specialist and come back to you."})
                    print("  follow-up question answered with a canned boss_reply", flush=True)
                    continue
                answered[ident] = entry
                print(f"  answer received: {str(entry.get('answer'))[:80]!r}", flush=True)
                break
            else:
                print("  no answer, continuing as if answered in the terminal", flush=True)
            continue
        if raw.startswith("#"):
            continue
        ev = json.loads(raw)
        run_id = ev.get("run_id", run_id)
        ev["ts"] = now()
        if ev.get("type") == "approval_given" and str(ev.get("id")) in answered:
            entry = answered[str(ev["id"])]
            ans = str(entry.get("answer", ""))
            ev["by"] = "window"
            ev["answer_text"] = ans
            if ans.startswith("rejected"):
                ev["decision"] = "rejected"
            elif ans.startswith("approved"):
                ev["decision"] = "approved"
                if " option " in ans:
                    ev["option"] = ans.split(" option ", 1)[1].split(" ", 1)[0]
        write(ev)
        print(f"{ev['ts']} {ev['type']} {ev.get('agent', '')}", flush=True)
        time.sleep(args.delay)
    return 0


if __name__ == "__main__":
    sys.exit(main())
