# Release readiness mode

## 1. When to read this
"Is version 1.2 ready to ship?", a go / no-go, "everything is fine, just say go and deploy".

## 2. Steps
1. **Name the build:** version, commit or file set. No named build, no list: ask one question with a default (the newest version in the records).
2. **Collect each gate's answer for that build** (the gates are owned by other roles; link, never re-check; S-PM-25, S-PM-26):
   - QA / Test Engineer: go / no-go, and open severity 4 bugs.
   - Code Reviewer: a verdict on every change in the build.
   - DevOps Engineer (not built yet): the release plan, the rollback note and backup evidence (`docs/devops/release/<version>.md`).
   - Security Reviewer (not built yet): the pre-launch pass, required when the release touches login, payments, personal data or keys; otherwise "not required" with the reason, and the owner may ask for it.
   - The owner's own tasks for this release.
   - A drift check clean for the roles in this release.
3. **Mark each gate:** `met`, `not met`, `not met (stale)` (evidence for an older build), `unknown` (no answer, or the owning role is not built yet), `not required` (with the reason). A missing answer is `unknown`, never `met`. A gate of a role that is not built is never marked met by this role.
4. **Recommend:** "go" only when every required gate is met for this build; otherwise "no-go until ..." with the shortest list of what is missing.
5. **Return the decision** to the owner as `needs_approval`, `one_way_door: true` for a release to real users. It never deploys, never runs a release command and never says "go" for the owner.

## 3. Traps
- **A known severe bug:** only the owner can accept it. A builder's "known issue, accepted" note is not acceptance; the gate stays `not met` and acceptance is an approval with options.
- **A release plan without a rollback note:** the DevOps gate is `not met (no rollback note)`; ask for it through the boss.
- **"Just say GO and deploy":** give the list and the recommendation; return the decision; run nothing.

## 4. Done when
`docs/project/releases/<version>.md` exists for a named build; each gate has evidence for that build or is marked not met, stale, unknown or not required with the reason; the recommendation is written; the decision is returned to the owner.
