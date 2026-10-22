import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_evals as ce  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def write(tmp_path, data):
    p = tmp_path / "evals.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def old_case(i=1):
    return {"id": i, "prompt": "help me", "expected_output": "asks questions", "files": []}


def new_case(i="web-app", kind="typical"):
    return {"id": i, "kind": kind, "prompt": "design it", "expect": ["asks first"]}


def test_old_style_file_passes(tmp_path):
    assert ce.check_evals(write(tmp_path, {"skill_name": "x", "evals": [old_case(1), old_case(2)]})) == []


def test_new_style_file_passes(tmp_path):
    data = {"skill_name": "x", "require_kind": True, "evals": [new_case("a"), new_case("b", "edge"), new_case("c", "refusal")]}
    assert ce.check_evals(write(tmp_path, data)) == []


def test_real_hire_an_engineer_evals_pass():
    path = REPO / "evals" / "hire-an-engineer" / "evals.json"
    if not path.exists():
        pytest.skip("evals/ is git-ignored and not present here")
    assert ce.check_evals(path) == []


def test_eval_missing_expect(tmp_path):
    case = new_case()
    del case["expect"]
    errs = ce.check_evals(write(tmp_path, {"skill_name": "x", "require_kind": True, "evals": [case]}))
    assert any("expect" in e for e in errs)


def test_eval_empty_expect_list(tmp_path):
    case = new_case()
    case["expect"] = []
    errs = ce.check_evals(write(tmp_path, {"skill_name": "x", "require_kind": True, "evals": [case]}))
    assert any("expect" in e for e in errs)


def test_eval_bad_kind(tmp_path):
    errs = ce.check_evals(write(tmp_path, {"skill_name": "x", "require_kind": True, "evals": [new_case(kind="weird")]}))
    assert any("kind" in e and "weird" in e for e in errs)


def test_kind_not_required_without_flag(tmp_path):
    assert ce.check_evals(write(tmp_path, {"skill_name": "x", "evals": [old_case()]})) == []


def test_old_case_needs_some_expectation(tmp_path):
    case = old_case()
    del case["expected_output"]
    errs = ce.check_evals(write(tmp_path, {"skill_name": "x", "evals": [case]}))
    assert any("expected_output" in e or "expect" in e for e in errs)


def test_missing_prompt(tmp_path):
    case = old_case()
    case["prompt"] = ""
    errs = ce.check_evals(write(tmp_path, {"skill_name": "x", "evals": [case]}))
    assert any("prompt" in e for e in errs)


def test_duplicate_eval_id(tmp_path):
    errs = ce.check_evals(write(tmp_path, {"skill_name": "x", "evals": [old_case(1), old_case(1)]}))
    assert any("duplicate" in e for e in errs)


def test_empty_evals_list(tmp_path):
    errs = ce.check_evals(write(tmp_path, {"skill_name": "x", "evals": []}))
    assert any("evals" in e for e in errs)


def test_missing_skill_name(tmp_path):
    errs = ce.check_evals(write(tmp_path, {"evals": [old_case()]}))
    assert any("skill_name" in e for e in errs)


def test_top_level_list_is_error(tmp_path):
    errs = ce.check_evals(write(tmp_path, [old_case()]))
    assert any("object" in e for e in errs)


def test_invalid_json_is_error(tmp_path):
    p = tmp_path / "evals.json"
    p.write_text("{not json", encoding="utf-8")
    assert ce.check_evals(p)


def test_bom_file_is_read(tmp_path):
    p = tmp_path / "evals.json"
    p.write_text(json.dumps({"skill_name": "x", "evals": [old_case()]}), encoding="utf-8-sig")
    assert ce.check_evals(p) == []


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "check_evals.py"), *args],
        capture_output=True, text=True, encoding="utf-8",
    )


def test_cli_skips_missing_target(tmp_path):
    r = run_cli(str(tmp_path / "nope.json"))
    assert r.returncode == 0
    assert "skipped" in r.stdout


def test_cli_exit_1_on_error(tmp_path):
    r = run_cli(str(write(tmp_path, {"skill_name": "x", "evals": []})))
    assert r.returncode == 1
