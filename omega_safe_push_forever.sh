#!/data/data/com.termux/files/usr/bin/bash

WATCH_DIR="$HOME/Omega"
cd "$WATCH_DIR" || exit

echo "Ω SAFE GIT AUTO-PUSH ENGINE ONLINE"

while true; do

  # Skip if merge in progress
  if [ -f .git/MERGE_HEAD ]; then
    echo "[BLOCKED] merge in progress"
    sleep 10
    continue
  fi

  # Skip if repo is broken state
  if git status --porcelain | grep -q "UU\|AA\|DD"; then
    echo "[BLOCKED] unresolved conflicts detected"
    sleep 10
    continue
  fi

  # Add changes
  git add -A

  # Only commit if there is something
  if git diff --cached --quiet; then
    echo "[IDLE] no changes"
    sleep 10
    continue
  fi

  # Commit safely
  git commit -m "Ω auto-sync $(date '+%Y-%m-%d %H:%M:%S')"

  # Pull safely before push (prevents your non-fast-forward loop)
  git pull --rebase origin main --autostash

  # Push
  git push origin main

  echo "[SYNC COMPLETE]"
  sleep 15

done
