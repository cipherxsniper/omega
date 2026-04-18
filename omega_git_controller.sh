#!/bin/bash

# =========================
# OMEGA GIT CONTROLLER v1
# Single source of truth for all Git operations
# =========================

set -e

REPO="$HOME/Omega"
cd "$REPO"

echo "[OMEGA GIT] Starting controlled push pipeline..."

# 1. Safety check
if [ -f .git/MERGE_HEAD ]; then
  echo "[BLOCKED] Merge in progress"
  exit 1
fi

# 2. Stage changes
git add -A

# 3. Commit with timestamp if changes exist
if git diff --cached --quiet; then
  echo "[OMEGA GIT] No changes to commit"
  exit 0
fi

MSG="omega-sync $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$MSG"

# 4. Push
git push origin main

echo "[OMEGA GIT] Push complete"
