# Method: Technical docs mode (README, guides, release notes)

## 1. When to read this
A README, a user guide, a setup or troubleshooting page, a handoff guide, or plain release notes for users.

## 2. Pick the kind of document
Keep the four kinds apart; one page is one kind:
- **Tutorial:** learn by doing, one safe path from start to a working result.
- **How-to guide:** do one task, for someone who already knows the basics.
- **Reference:** facts to look up (commands, settings, limits), no story.
- **Explanation:** why it works this way.
A user guide is usually a getting-started tutorial, short how-to pages and one reference page.

## 3. Steps
1. Read the brief, the old document if any, and the style guide and glossary.
2. Read the code and the real setup files (package files, scripts, config examples). The code wins over the old document.
3. Run only read-only commands to check steps (for example `--help`, `--version`, listing files). No installs, no network commands, no deploys, no reading of `.env` or secret files.
4. Write it in two layers: plain words first, technical notes last (`hire-an-engineer/references/documents.md`). Name a screenshot or picture for each screen a user must find; do not invent one.
5. Mark each step `tested` (you ran it in this session, with the command and result) or `not run`. List a clean-clone test by the owner or the QA / Test Engineer as a missing check when it has not happened.
6. List what changed from the old version and where the old one was wrong.
7. If the brief asks you to document something you cannot find in the code, say it was not found and ask; write nothing invented.

## 4. Release notes
- Plain notes for users, written from the changelog and the merged changes; the technical `CHANGELOG.md` stays separate (`hire-an-engineer/references/versioning-release.md` section 5).
- Leave out details that would help an attacker: "fixed a security problem", not how it worked.
- Edit `CHANGELOG.md` only when the brief names it (owner decision Q7).
- Notes are drafts; a person publishes them.

## 5. Where files go
`README.md`, `docs/guides/`, and release notes in the file or folder the brief names (if none is named and the project has none, `docs/writing/release-notes/`). `CHANGELOG.md` only when the brief names it.

## 6. Checker
A checker script for this skill (for example a docs-against-code or character-count checker) is not built yet. Use commands already on the machine or a small standard-library script run from a temporary folder, and give each result with its command.

## 7. Done when
The document is of one clear kind, every step is marked `tested` or `not run`, the differences from the old version are listed, and the answer names the missing checks (for example the clean-clone test).
