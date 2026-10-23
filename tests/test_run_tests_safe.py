"""skills/code-reviewer/scripts/run_tests_safe.py: run a branch's tests in a scratch copy, never in the user's tree."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "code-reviewer" / "scripts" / "run_tests_safe.py"
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid"]


def git(repo, *args):
    return subprocess.run([*GIT, *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def make_repo(tmp_path, files_main, files_branch=None, branch="review/x"):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    for name, text in files_main.items():
        p = repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "main")
    if files_branch is not None:
        git(repo, "checkout", "-q", "-b", branch)
        for name, text in files_branch.items():
            p = repo / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "--allow-empty", "-m", "branch")
        git(repo, "checkout", "-q", "main")
    return repo


def run(repo, *args, env=None):
    e = {**os.environ, **(env or {})}
    r = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(repo), *args],
                       capture_output=True, text=True, encoding="utf-8", env=e)
    return r


def result(r):
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


PASSING = {"shop/__init__.py": "", "shop/m.py": "def f():\n    return 1\n",
           "tests/__init__.py": "",
           "tests/test_m.py": "import unittest\nfrom shop.m import f\n\n\nclass T(unittest.TestCase):\n    def test_f(self):\n        self.assertEqual(f(), 1)\n"}
FAILING = {**PASSING, "shop/m.py": "def f():\n    return 2\n"}


def test_passing_branch_reports_pass_and_leaves_the_repo_untouched(tmp_path):
    repo = make_repo(tmp_path, PASSING, PASSING)
    before = git(repo, "status", "--porcelain")
    r = result(run(repo, "--ref", "review/x"))
    assert r["exit_code"] == 0 and r["passed"] is True and r["runner"] == "unittest"
    assert git(repo, "status", "--porcelain") == before == ""
    assert git(repo, "branch", "--show-current").strip() == "main"
    assert not list(repo.rglob("__pycache__"))
    assert r["scratch_deleted"] is True and not Path(r["scratch_dir"]).exists()


def test_failing_branch_reports_failure_with_output(tmp_path):
    repo = make_repo(tmp_path, PASSING, FAILING)
    r = result(run(repo, "--ref", "review/x"))
    assert r["passed"] is False and r["exit_code"] != 0
    assert "AssertionError" in (r["stdout_tail"] + r["stderr_tail"])


def test_it_tests_the_ref_not_the_working_tree(tmp_path):
    repo = make_repo(tmp_path, PASSING, FAILING)
    (repo / "shop" / "m.py").write_text("def f():\n    return 1\n", encoding="utf-8")  # dirty tree would pass
    assert result(run(repo, "--ref", "review/x"))["passed"] is False


def test_secrets_in_the_environment_are_not_passed_on(tmp_path):
    probe = {**PASSING, "tests/test_m.py": "import os, unittest\n\n\nclass T(unittest.TestCase):\n    def test_env(self):\n        self.assertIsNone(os.environ.get('MY_SECRET_TOKEN'))\n"}
    repo = make_repo(tmp_path, probe, probe)
    r = result(run(repo, "--ref", "review/x", env={"MY_SECRET_TOKEN": "hunter2"}))
    assert r["passed"] is True


def test_timeout_kills_a_slow_test(tmp_path):
    slow = {**PASSING, "tests/test_m.py": "import time, unittest\n\n\nclass T(unittest.TestCase):\n    def test_slow(self):\n        time.sleep(60)\n"}
    repo = make_repo(tmp_path, slow, slow)
    r = result(run(repo, "--ref", "review/x", "--timeout", "2"))
    assert r["timed_out"] is True and r["passed"] is False


def test_unknown_ref_is_a_clean_error(tmp_path):
    repo = make_repo(tmp_path, PASSING, PASSING)
    r = run(repo, "--ref", "no/such")
    assert r.returncode == 2 and "no/such" in r.stderr and r.stdout.strip() == ""


def test_not_a_git_repo_is_a_clean_error(tmp_path):
    r = run(tmp_path, "--ref", "main")
    assert r.returncode == 2 and "git" in r.stderr.lower()


def test_no_test_runner_found_is_reported_not_guessed(tmp_path):
    repo = make_repo(tmp_path, {"README.md": "hello"}, {"README.md": "hello2"})
    r = result(run(repo, "--ref", "review/x"))
    assert r["runner"] is None and r["passed"] is None and "no test runner" in r["note"].lower()


def test_unknown_runner_argument_is_refused(tmp_path):
    repo = make_repo(tmp_path, PASSING, PASSING)
    r = run(repo, "--ref", "review/x", "--runner", "rm -rf")
    assert r.returncode == 2


def test_the_output_says_the_code_ran_on_this_machine(tmp_path):
    repo = make_repo(tmp_path, PASSING, PASSING)
    assert "ran on this machine" in result(run(repo, "--ref", "review/x"))["warning"].lower()
