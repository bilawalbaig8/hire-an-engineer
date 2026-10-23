#!/usr/bin/env python3
"""Run a branch's tests in a scratch copy, so the user's working tree is never touched.

Usage: python run_tests_safe.py --ref BRANCH_OR_COMMIT [--repo DIR] [--timeout SECONDS] [--runner auto|unittest|pytest|go|dotnet]

What it does: copies the committed files of REF (git archive) into a new temp folder, runs ONE known test command there
(no shell, fixed arguments, a timeout, a stripped environment without tokens or keys, no bytecode or cache files),
prints one JSON object and deletes the copy. It never checks out, stashes or edits anything in the repository.

What it does not do: it is not a sandbox. The tests are the author's code and they run on this machine with your user's
rights. Ask the owner before running it for a ref you do not trust (the boss relays that approval).
Exit code 0 with the JSON on stdout; 2 with a message on stderr for misuse (not a git repo, unknown ref, bad runner).
"""
from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

RUNNERS = ("auto", "unittest", "pytest", "go", "dotnet")
TAIL = 4000
WARNING = ("These tests are the branch author's code. They ran on this machine with your user's rights, "
           "in a scratch copy that is now deleted. This is not a sandbox.")
KEEP_ENV = ("PATH", "SYSTEMROOT", "SystemRoot", "WINDIR", "COMSPEC", "PATHEXT", "LANG", "LC_ALL", "TZ")


class Misuse(Exception):
    pass


def _git(repo: Path, *args: str, text: bool = True):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=text)


def check_ref(repo: Path, ref: str) -> None:
    if not repo.is_dir() or _git(repo, "rev-parse", "--git-dir").returncode != 0:
        raise Misuse(f"{repo} is not a git repository")
    if not ref or ref.startswith("-"):
        raise Misuse(f"bad ref: {ref!r}")
    if _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").returncode != 0:
        raise Misuse(f"unknown ref: {ref}")


def extract_ref(repo: Path, ref: str, dest: Path) -> None:
    proc = subprocess.run(["git", "archive", "--format=tar", ref], cwd=repo, capture_output=True)
    if proc.returncode != 0:
        raise Misuse(f"git archive failed for {ref}: {proc.stderr.decode('utf-8', 'replace').strip()}")
    root = dest.resolve()
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tar:
        for member in tar.getmembers():
            target = (dest / member.name).resolve()
            if root != target and root not in target.parents:
                raise Misuse(f"unsafe path in archive: {member.name}")
            if member.issym() or member.islnk():
                continue  # links are never created
            tar.extract(member, dest)


def detect_runner(copy: Path) -> str | None:
    names = {p.name for p in copy.iterdir()}
    if "go.mod" in names:
        return "go"
    if any(n.endswith((".sln", ".csproj")) for n in names):
        return "dotnet"
    py = any(copy.rglob("test_*.py")) or any(copy.rglob("*_test.py"))
    if py:
        cfg = {"pytest.ini", "tox.ini", "conftest.py"} & names
        pyproject = copy / "pyproject.toml"
        if cfg or (pyproject.is_file() and "pytest" in pyproject.read_text(encoding="utf-8", errors="replace")):
            return "pytest"
        return "unittest"
    return None


def command_for(runner: str) -> tuple[list[str], dict]:
    if runner == "unittest":
        return [sys.executable, "-m", "unittest", "discover", "-v"], {}
    if runner == "pytest":
        return [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], {}
    if runner == "go":
        return ["go", "test", "./..."], {"GOFLAGS": "-mod=vendor", "GOPROXY": "off"}
    if runner == "dotnet":
        return ["dotnet", "test", "--no-restore"], {}
    raise Misuse(f"unknown runner: {runner}")


def clean_env(copy: Path, extra: dict) -> dict:
    env = {k: os.environ[k] for k in KEEP_ENV if k in os.environ}
    home = str(copy / ".home")
    (copy / ".home").mkdir(exist_ok=True)
    env.update({"HOME": home, "USERPROFILE": home, "TEMP": home, "TMP": home, "TMPDIR": home,
                "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1", "CI": "1"})
    env.update(extra)
    return env


def _tail(text: bytes | None) -> str:
    s = (text or b"").decode("utf-8", "replace")
    return s[-TAIL:]


def kill_tree(proc: subprocess.Popen) -> None:
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
        else:
            os.killpg(proc.pid, 9)
    except (OSError, ProcessLookupError):
        pass
    try:
        proc.kill()
    except OSError:
        pass


def run_command(cmd: list[str], cwd: Path, env: dict, timeout: float) -> dict:
    start = time.monotonic()
    kwargs = {"creationflags": getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)} if os.name == "nt" else {"start_new_session": True}
    try:
        proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    except OSError as e:
        return {"exit_code": None, "timed_out": False, "stdout_tail": "", "stderr_tail": f"cannot start {cmd[0]}: {e}",
                "duration_s": 0.0, "started": False}
    timed_out = False
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        kill_tree(proc)
        try:
            out, err = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            out, err = b"", b""
    return {"exit_code": None if timed_out else proc.returncode, "timed_out": timed_out,
            "stdout_tail": _tail(out), "stderr_tail": _tail(err),
            "duration_s": round(time.monotonic() - start, 2), "started": True}


def _onexc(func, path, exc):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except OSError:
        pass


def run(repo: Path, ref: str, timeout: float, runner: str) -> dict:
    check_ref(repo, ref)
    scratch = Path(tempfile.mkdtemp(prefix="review-tests-"))
    out: dict = {"ref": ref, "scratch_dir": str(scratch), "warning": WARNING, "runs_on_this_machine": True}
    try:
        extract_ref(repo, ref, scratch)
        chosen = detect_runner(scratch) if runner == "auto" else runner
        out["runner"] = chosen
        if chosen is None:
            out.update(passed=None, exit_code=None, timed_out=False, command=None,
                       note="No test runner found (no unittest/pytest tests, go.mod or .NET project). Nothing was run.")
        else:
            cmd, extra = command_for(chosen)
            res = run_command(cmd, scratch, clean_env(scratch, extra), timeout)
            out.update(command=" ".join(cmd), **res)
            out["passed"] = (res["exit_code"] == 0) if res["started"] and not res["timed_out"] else False
            out["note"] = ("Timed out and was killed." if res["timed_out"] else
                           ("Tests passed." if out["passed"] else "Tests failed or could not start."))
    finally:
        shutil.rmtree(scratch, onexc=_onexc) if sys.version_info >= (3, 12) else shutil.rmtree(scratch, onerror=_onexc)
        out["scratch_deleted"] = not scratch.exists()
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--ref", required=True)
    p.add_argument("--repo", default=".")
    p.add_argument("--timeout", type=float, default=300.0)
    p.add_argument("--runner", default="auto")
    args = p.parse_args(argv)
    try:
        if args.runner not in RUNNERS:
            raise Misuse(f"--runner must be one of {', '.join(RUNNERS)}")
        if args.timeout <= 0 or args.timeout > 3600:
            raise Misuse("--timeout must be between 1 and 3600 seconds")
        result = run(Path(args.repo).resolve(), args.ref, args.timeout, args.runner)
    except Misuse as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
