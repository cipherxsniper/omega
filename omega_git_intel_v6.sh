#!/data/data/com.termux/files/usr/bin/bash

# =========================
# OMEGA GIT INTELLIGENCE v6
# =========================

WATCH_DIR="$HOME/Omega"
cd "$WATCH_DIR" || exit

echo "🧠 OMEGA GIT INTELLIGENCE v6 ONLINE"
echo "-----------------------------------"

# Safety ignore enforcement
cat <<EOF >> .gitignore
_dist/
logs/
nohup.out
*.lock
v28_backups/
v29_backups/
EOF

# Debounce system (prevents spam commits)
LAST_COMMIT_TIME=0
DEBOUNCE_SECONDS=10

commit_changes() {
    git add -A

    # Skip if nothing to commit
    if git diff --cached --quiet; then
        echo "🟡 No meaningful changes detected"
        return
    fi

    # Intelligent commit message
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

    echo "🧠 Committing Omega system update..."

    git commit -m "Omega v6 auto-sync [$TIMESTAMP]"

    echo "🚀 Pushing to GitHub..."
    git push

    echo "✅ Sync complete"
}

# =========================
# FILE WATCH LOOP
# =========================

while true; do

    # Wait for filesystem event
    inotifywait -r -e modify,create,delete,move "$WATCH_DIR" >/dev/null 2>&1

    NOW=$(date +%s)
    DIFF=$((NOW - LAST_COMMIT_TIME))

    if [ "$DIFF" -lt "$DEBOUNCE_SECONDS" ]; then
        echo "⏳ Change ignored (debounce active)"
        continue
    fi

    LAST_COMMIT_TIME=$NOW

    echo "🔄 Change detected in Omega system..."

    sleep 2  # lets nano finish writing file

    commit_changes

done
