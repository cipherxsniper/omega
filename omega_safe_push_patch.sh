#!/bin/bash

git add -A

# block push if merge in progress
if [ -f .git/MERGE_HEAD ]; then
  echo "MERGE IN PROGRESS - SKIPPING PUSH"
  exit 0
fi

git commit -m "Ω auto-sync"
git push origin main
