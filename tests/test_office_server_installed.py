"""Server lookups that make it work outside the repo: roster fallback, explicit roster and UI folder."""
import http.client
import json
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import office_server as os_  # noqa: E402

ROSTER = "| Name | Skill | Model | Owns |\n|---|---|---|---|\n| zed | s | opus | things |\n"


def _serve(project, repo, **kw):
    srv = os_.make_server(project, port=0, repo_root=repo, **kw)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def _get(srv, path):
    c = http.client.HTTPConnection("127.0.0.1", srv.port, timeout=5)
    c.request("GET", path)
    return c.getresponse().read()


def test_roster_falls_back_to_agent_frontmatter(tmp_path):
    agents = tmp_path / ".claude" / "agents"
    agents.mkdir(parents=True)
    (agents / "architect.md").write_text("---\nname: architect\nskill: software-architect\nmodel: opus\n---\nbody\n", encoding="utf-8")
    (agents / "orchestrator.md").write_text("---\nname: orchestrator\n---\n", encoding="utf-8")
    srv = _serve(tmp_path, tmp_path / "norepo")
    try:
        assert json.loads(_get(srv, "/roster")) == [
            {"name": "architect", "skill": "software-architect", "model": "opus", "owns": ""}]
    finally:
        srv.shutdown()
        srv.server_close()


def test_explicit_roster_and_ui_dir(tmp_path):
    r = tmp_path / "r.md"
    r.write_text(ROSTER, encoding="utf-8")
    ui = tmp_path / "ui"
    ui.mkdir()
    (ui / "index.html").write_text("<html>custom</html>", encoding="utf-8")
    srv = _serve(tmp_path, tmp_path / "norepo", ui_dir=ui, roster_path=r)
    try:
        assert json.loads(_get(srv, "/roster"))[0]["name"] == "zed"
        assert b"custom" in _get(srv, "/")
    finally:
        srv.shutdown()
        srv.server_close()


def test_project_roster_used_when_no_repo(tmp_path):
    (tmp_path / "docs" / "agents").mkdir(parents=True)
    (tmp_path / "docs" / "agents" / "roster.md").write_text(ROSTER, encoding="utf-8")
    srv = _serve(tmp_path, tmp_path / "norepo")
    try:
        assert json.loads(_get(srv, "/roster"))[0]["name"] == "zed"
    finally:
        srv.shutdown()
        srv.server_close()
