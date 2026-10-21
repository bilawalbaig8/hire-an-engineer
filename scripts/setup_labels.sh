#!/usr/bin/env bash
# One-time: create base labels. Requires GitHub CLI (gh) logged in. Run from the repo folder.
set -e
create() { gh label create "$1" --color "$2" --description "$3" --force; }
create "needs-triage"      "fbca04" "New, not yet reviewed"
create "type: gap"         "d73a4a" "Skill missed or mishandled a situation"
create "type: improvement" "a2eeef" "Make an existing skill better"
create "type: new-skill"   "7057ff" "Idea for a new skill"
create "accepted"          "0e8a16" "Will be fixed or added"
create "fixed"             "0e8a16" "Fixed in a release"
create "wontfix"           "ffffff" "Not planned"
create "possible-secret"   "b60205" "May contain a secret — remove and rotate"
echo "Labels ready."
