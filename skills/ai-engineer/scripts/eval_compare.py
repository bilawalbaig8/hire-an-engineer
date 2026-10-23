#!/usr/bin/env python3
"""Offline eval compare: two prompt versions, case by case, on recorded outputs.

Standard library only. It never calls a model and never touches the network.

Files (JSON):
  cases   list of {"id", "set": "open" | "held_out", "kind": optional,
                   "contains": [..], "not_contains": [..]}
  before  {"case id": "recorded output of the current version"}
  after   {"case id": "recorded output of the candidate"}

A case passes when every `contains` text is in the output and no `not_contains`
text is. A case with no recorded output is `missing` (it does not pass and is
listed). Prints `k of n` before and after per set, and the cases that flipped.
Exit code 0 = no regression, 1 = a regression or a missing output on a held-out
case, 2 = bad input. Use --strict to also fail on any regression in the open set.
"""
import argparse
import json
import sys

SETS = ("open", "held_out")


def passes(case, output):
    if output is None:
        return None
    text = output.lower()
    if any(s.lower() not in text for s in case.get("contains", [])):
        return False
    if any(s.lower() in text for s in case.get("not_contains", [])):
        return False
    return True


def compare(cases, before, after):
    result = {s: {"n": 0, "before": 0, "after": 0, "regressions": [], "fixed": [], "missing": []} for s in SETS}
    for case in cases:
        s = case.get("set")
        if s not in result:
            raise ValueError(f"case {case.get('id')!r}: set must be 'open' or 'held_out'")
        r = result[s]
        r["n"] += 1
        b, a = passes(case, before.get(case["id"])), passes(case, after.get(case["id"]))
        if a is None or b is None:
            r["missing"].append(case["id"])
        r["before"] += bool(b)
        r["after"] += bool(a)
        if b and a is False:
            r["regressions"].append(case["id"])
        if b is False and a:
            r["fixed"].append(case["id"])
    return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--cases", required=True)
    p.add_argument("--before", required=True)
    p.add_argument("--after", required=True)
    p.add_argument("--strict", action="store_true")
    args = p.parse_args(argv)
    try:
        cases, before, after = (json.load(open(f, encoding="utf-8-sig")) for f in (args.cases, args.before, args.after))
        result = compare(cases, before, after)
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    bad = False
    for s in SETS:
        r = result[s]
        print(f"{s}: before {r['before']} of {r['n']}, after {r['after']} of {r['n']}")
        if r["regressions"]:
            print(f"  regressions (pass -> fail): {', '.join(r['regressions'])}")
        if r["fixed"]:
            print(f"  fixed (fail -> pass): {', '.join(r['fixed'])}")
        if r["missing"]:
            print(f"  missing recorded output: {', '.join(r['missing'])}")
        if s == "held_out" and (r["regressions"] or r["missing"]):
            bad = True
        if s == "open" and args.strict and r["regressions"]:
            bad = True
    if result["held_out"]["n"] == 0:
        print("held_out: no cases - release check is blocked until a held-out set exists")
        bad = True
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
