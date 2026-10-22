import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_sources as cs  # noqa: E402

HEADER = "| ID | Title | Author | Year | URL | Use | Cost/licence | Status |\n|---|---|---|---|---|---|---|---|\n"


def row(id_="S-FND-1", status="verified", url="https://example.org/a"):
    return f"| {id_} | A book | An Author | 2021 | {url} | Teaches things | Paid | {status} |\n"


def write_sources(tmp_path, body):
    skill = tmp_path / "skills" / "demo"
    (skill / "references").mkdir(parents=True)
    (skill / "references" / "sources.md").write_text(body, encoding="utf-8")
    return skill


def test_good_table_passes(tmp_path):
    skill = write_sources(tmp_path, "# Sources\n\n" + HEADER + row() + row("S-FND-2", "unverified"))
    assert cs.check_sources(skill / "references" / "sources.md") == []


def test_multiple_tables_share_one_id_space(tmp_path):
    body = "## A\n\n" + HEADER + row("S-FND-1") + "\n## B\n\n" + HEADER + row("S-WEB-1")
    skill = write_sources(tmp_path, body)
    assert cs.check_sources(skill / "references" / "sources.md") == []


def test_duplicate_id(tmp_path):
    body = HEADER + row("S-FND-1") + row("S-FND-1")
    errs = cs.check_sources(write_sources(tmp_path, body) / "references" / "sources.md")
    assert any("duplicate" in e and "S-FND-1" in e for e in errs)


def test_bad_status(tmp_path):
    body = HEADER + row(status="maybe")
    errs = cs.check_sources(write_sources(tmp_path, body) / "references" / "sources.md")
    assert any("Status" in e and "maybe" in e for e in errs)


def test_missing_url(tmp_path):
    body = HEADER + row(url="n/a")
    errs = cs.check_sources(write_sources(tmp_path, body) / "references" / "sources.md")
    assert any("URL" in e for e in errs)


def test_bad_id_shape(tmp_path):
    body = HEADER + row("S-1")
    errs = cs.check_sources(write_sources(tmp_path, body) / "references" / "sources.md")
    assert any("S-1" in e and "S-AREA-n" in e for e in errs)


def test_row_with_wrong_column_count(tmp_path):
    body = HEADER + "| S-FND-1 | A book | verified |\n"
    errs = cs.check_sources(write_sources(tmp_path, body) / "references" / "sources.md")
    assert any("8 columns" in e for e in errs)


def test_file_without_sources_table_is_error(tmp_path):
    errs = cs.check_sources(write_sources(tmp_path, "# Sources\n\nnothing here\n") / "references" / "sources.md")
    assert any("no table" in e for e in errs)


def test_errors_carry_file_and_line(tmp_path):
    body = HEADER + row(status="maybe")
    path = write_sources(tmp_path, body) / "references" / "sources.md"
    errs = cs.check_sources(path)
    assert errs[0].startswith(f"{path}:3:")


def test_ref_to_unknown_id(tmp_path):
    skill = write_sources(tmp_path, HEADER + row("S-FND-1"))
    (skill / "references" / "core.md").write_text("See [S-FND-9] for more.\n", encoding="utf-8")
    errs = cs.check_refs(skill)
    assert any("S-FND-9" in e and "unknown" in e for e in errs)


def test_verified_ref_ok(tmp_path):
    skill = write_sources(tmp_path, HEADER + row("S-FND-1"))
    (skill / "references" / "core.md").write_text("Teams decide early [S-FND-1].\n", encoding="utf-8")
    assert cs.check_refs(skill) == []


def test_unverified_cited_as_fact(tmp_path):
    skill = write_sources(tmp_path, HEADER + row("S-FND-2", "unverified"))
    (skill / "references" / "core.md").write_text("Always do this [S-FND-2].\n", encoding="utf-8")
    errs = cs.check_refs(skill)
    assert any("S-FND-2" in e and "unverified" in e for e in errs)


def test_unverified_cited_with_the_word_is_ok(tmp_path):
    skill = write_sources(tmp_path, HEADER + row("S-FND-2", "unverified"))
    (skill / "references" / "core.md").write_text("Maybe this (unverified source) [S-FND-2].\n", encoding="utf-8")
    assert cs.check_refs(skill) == []


def test_sources_md_itself_is_not_scanned_for_refs(tmp_path):
    body = HEADER + row("S-FND-1") + "\nSee also [S-NOPE-1].\n"
    skill = write_sources(tmp_path, body)
    assert cs.check_refs(skill) == []


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "check_sources.py"), *args],
        capture_output=True, text=True, encoding="utf-8",
    )


def test_cli_skips_missing_target(tmp_path):
    r = run_cli(str(tmp_path / "skills" / "nope"))
    assert r.returncode == 0
    assert "skipped" in r.stdout


def test_cli_exit_1_on_error(tmp_path):
    skill = write_sources(tmp_path, HEADER + row(status="maybe"))
    r = run_cli(str(skill))
    assert r.returncode == 1
    assert "maybe" in r.stdout


def test_cli_exit_0_when_clean(tmp_path):
    skill = write_sources(tmp_path, HEADER + row())
    r = run_cli(str(skill))
    assert r.returncode == 0
