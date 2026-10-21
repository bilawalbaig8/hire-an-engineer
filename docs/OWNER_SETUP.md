# Owner setup checklist (one time)

## 1. Create and push
```bash
cd hire-an-engineer
./scripts/set_owner.sh <your-github-username> hire-an-engineer   # fills in your username everywhere
git init -b main && git add . && git commit -m "feat: initial release of hire-an-engineer"
gh repo create <your-github-username>/hire-an-engineer --public --source . --push \
  --description "Open-source skills for AI agents: hire-an-engineer and more"
./scripts/setup_labels.sh
git tag hire-an-engineer-v0.1.0 && git push origin hire-an-engineer-v0.1.0   # creates the first release
```
(No GitHub CLI? Create an empty public repo on github.com, then `git remote add origin … && git push -u origin main`, and create labels from the Issues → Labels page.)

## 2. Nobody else can change the repo
On a personal public repo, only you and invited collaborators can push. Keep it that way:
- **Settings → Collaborators:** add nobody.
- **Settings → General → Features → Pull requests:** untick (disable entirely) — or set to *Collaborators only*.
- **Settings → Rules → Rulesets → New branch ruleset** for `main`: block force pushes, restrict deletions, require status check *Validate skills*. Add yourself to the bypass list if you push directly.
- **Settings → General → Features:** keep **Issues** on (anyone can report). Wiki off. Discussions optional.
- **Settings → Actions → General:** workflow permissions *Read repository contents* by default (workflows request what they need).

Note: anyone can still **fork** a public repo and change *their copy* — that's what open source and the MIT License allow. Your repo stays unchanged.

## 3. Safety
- **Settings → Code security:** enable secret scanning, push protection, private vulnerability reporting, Dependabot alerts.
- Turn on 2-factor authentication on your GitHub account.

## 4. Optional
- **Projects:** create a board (Backlog / Accepted / In progress / Fixed) and set it to auto-add issues from this repo (Project → Workflows → Auto-add).
- Pin the repo on your profile; add topics: `claude-skills`, `hire-an-engineer`, `ai-agents`, `claude-code`.

## Release flow for every update
1. Fix from an issue → update the skill → add a CHANGELOG entry and bump the version in README.
2. Commit with `Fixes #<issue>` so the issue closes automatically.
3. Tag `<skill-name>-v<version>` and push the tag → the release workflow validates, packages and publishes.
