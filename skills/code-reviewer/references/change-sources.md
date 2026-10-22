# Where the change comes from and what else holds risk

When to read this: when the change is uncommitted, a pull request with no network, a re-review, or contains lockfiles, generated or vendored code, CI and deploy config, or saved-data formats. Items marked "general practice" come from experience, not from a cited source.

## Getting the change
- **Uncommitted work** ("review what I just did"): read `git diff`, `git diff --staged` and the untracked files (`git ls-files --others --exclude-standard`; read them, they are not in either diff).
- **Pull request by number with no network:** ask the boss or the person for a local branch or a patch; do not guess. Check whether the branch is out of date with its base, and do not assume the default branch is called `main`. Use three-dot diffs (`base...branch`).
- **Re-review:** read the previous file in `docs/reviews/`, confirm each earlier finding is resolved or still open, and do not re-raise fixed ones.
- **The review file** lands in the working tree and may be committed with the change. A same-day, same-topic name gets a numeric suffix; never overwrite.

## Files that are easy to skip
- **Lockfiles, generated and vendored code:** do not skip lockfile diffs. Check new packages, resolved URLs that point at another registry, and install scripts. Sample generated and vendored code, and say so. (general practice)
- **CI, build and deploy config:** GitHub Actions (`pull_request_target`, secrets exposed to forks, unpinned actions), Dockerfiles, `postinstall` and build scripts. A script that runs on every build is code that runs with the build's secrets. (general practice)
- **Persisted formats beyond databases:** save-game and player data, serialized caches; a changed shape can break data already on disk. Unity: `.meta` GUIDs (a changed or missing `.meta` breaks references), renamed serialized fields without `FormerlySerializedAs`. Treat a breaking change to stored data like a migration (see `review-method`). (general practice)
