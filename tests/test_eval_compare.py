import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "ai-engineer" / "scripts" / "eval_compare.py"
spec = importlib.util.spec_from_file_location("eval_compare", SCRIPT)
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)

CASES = [
    {"id": "o1", "set": "open", "contains": ["refund"]},
    {"id": "o2", "set": "open", "contains": ["hello"]},
    {"id": "h1", "set": "held_out", "contains": ["cannot"], "not_contains": ["password"]},
]


def run(tmp_path, cases, before, after, extra=()):
    files = []
    for name, data in (("c", cases), ("b", before), ("a", after)):
        f = tmp_path / f"{name}.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        files.append(str(f))
    return ec.main(["--cases", files[0], "--before", files[1], "--after", files[2], *extra])


def test_open_gain_held_out_loss_is_reported(tmp_path, capsys):
    before = {"o1": "no", "o2": "hello", "h1": "I cannot share that"}
    after = {"o1": "refund ok", "o2": "hello", "h1": "the password is x"}
    assert run(tmp_path, CASES, before, after) == 1
    out = capsys.readouterr().out
    assert "open: before 1 of 2, after 2 of 2" in out
    assert "held_out: before 1 of 1, after 0 of 1" in out
    assert "regressions (pass -> fail): h1" in out


def test_no_change_passes(tmp_path, capsys):
    same = {"o1": "refund", "o2": "hello", "h1": "I cannot"}
    assert run(tmp_path, CASES, same, same) == 0
    assert "after 2 of 2" in capsys.readouterr().out


def test_missing_output_is_listed_and_blocks(tmp_path, capsys):
    before = {"o1": "refund", "o2": "hello", "h1": "I cannot"}
    after = {"o1": "refund", "o2": "hello"}
    assert run(tmp_path, CASES, before, after) == 1
    assert "missing recorded output: h1" in capsys.readouterr().out


def test_no_held_out_set_blocks(tmp_path, capsys):
    only_open = [c for c in CASES if c["set"] == "open"]
    same = {"o1": "refund", "o2": "hello"}
    assert run(tmp_path, only_open, same, same) == 1
    assert "blocked" in capsys.readouterr().out


def test_strict_fails_on_open_regression(tmp_path):
    before = {"o1": "refund", "o2": "hello", "h1": "I cannot"}
    after = {"o1": "no", "o2": "hello", "h1": "I cannot"}
    assert run(tmp_path, CASES, before, after) == 0
    assert run(tmp_path, CASES, before, after, ["--strict"]) == 1


def test_bad_set_name_is_exit_2(tmp_path, capsys):
    bad = [{"id": "x", "set": "train", "contains": []}]
    assert run(tmp_path, bad, {}, {}) == 2
