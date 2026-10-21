#!/usr/bin/env bash
# Usage: ./scripts/set_owner.sh <github-username> [repo-name]
set -e
OWNER="$1"; REPO="${2:-hire-an-engineer}"
[ -z "$OWNER" ] && { echo "Usage: $0 <github-username> [repo-name]"; exit 1; }
grep -rl "OWNER/REPO\|@OWNER" --include="*.md" --include="CODEOWNERS" . | while read f; do
  sed -i.bak -e "s#OWNER/REPO#$OWNER/$REPO#g" -e "s#@OWNER#@$OWNER#g" "$f" && rm "$f.bak"
done
echo "Placeholders set to $OWNER/$REPO"
