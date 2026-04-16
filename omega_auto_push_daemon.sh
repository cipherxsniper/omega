#!/bin/bash

WATCH_DIR="$HOME/Omega"
cd "$WATCH_DIR" || exit

echo "🧠 Omega Auto Push Daemon ONLINE"

while true; do

    # Only act if there are changes
    if [[ -n $(git status --porcelain) ]]; then

        echo "🧬 Changes detected..."

        git add -A

        git commit -m "Ω auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"

        git pull origin main --allow-unrelated-histories --no-edit

        git push origin main

        echo "🚀 Synced to GitHub"

    fi

    sleep 10

done
