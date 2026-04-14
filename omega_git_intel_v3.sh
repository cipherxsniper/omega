#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 Omega Git Intelligence Layer v3 initializing..."

cd ~/Omega || exit 1

# -----------------------------
# CONFIG
# -----------------------------

LOCK_FILE=".omega_git_lock"
THRESHOLD=20

if [ -f "$LOCK_FILE" ]; then
  echo "⚠️ Sync already running — exiting"
  exit 0
fi

touch "$LOCK_FILE"

cleanup() {
  rm -f "$LOCK_FILE"
}
trap cleanup EXIT

# -----------------------------
# INIT GIT IF NEEDED
# -----------------------------

if [ ! -d .git ]; then
  git init
  git remote add origin https://github.com/cipherxsniper/omega.git
fi

git branch -M main

# -----------------------------
# INTELLIGENCE STAGING
# -----------------------------

echo "📊 Analyzing Omega system changes..."

git add -A

# remove noise immediately
git reset HEAD *.log 2>/dev/null
git reset HEAD *.pid 2>/dev/null
git reset HEAD nohup.out 2>/dev/null
git reset HEAD __pycache__/ 2>/dev/null
git reset HEAD *.tmp 2>/dev/null

# -----------------------------
# INTELLIGENCE SCORING
# -----------------------------

PY_CHANGES=$(git diff --cached --name-only | grep "\.py$" | wc -l)
JSON_CHANGES=$(git diff --cached --name-only | grep "\.json$" | wc -l)
SH_CHANGES=$(git diff --cached --name-only | grep "\.sh$" | wc -l)

SCORE=$((PY_CHANGES * 10 + JSON_CHANGES * 4 + SH_CHANGES * 6))

echo "📈 Change Score: $SCORE"

if [ "$SCORE" -lt "$THRESHOLD" ]; then
  echo "⚠️ Change too small — not significant enough to evolve Omega"
  git reset
  exit 0
fi

# -----------------------------
# GENERATE INTELLIGENCE MESSAGE
# -----------------------------

MSG="🧠 Omega evolution sync"

if [ "$PY_CHANGES" -gt 0 ]; then
  MSG="$MSG | neural update ($PY_CHANGES modules)"
fi

if [ "$JSON_CHANGES" -gt 0 ]; then
  MSG="$MSG | memory restructure ($JSON_CHANGES files)"
fi

if [ "$SH_CHANGES" -gt 0 ]; then
  MSG="$MSG | system automation update ($SH_CHANGES scripts)"
fi

MSG="$MSG | score:$SCORE"

# -----------------------------
# COMMIT
# -----------------------------

echo "💾 Committing intelligence layer..."

git commit -m "$MSG"

# -----------------------------
# PUSH WITH SAFETY RETRIES
# -----------------------------

echo "🚀 Pushing Omega evolution..."

for i in 1 2 3; do
  git push -u origin main && break
  echo "⚠️ retry $i/3..."
  sleep 2
done

echo "✅ Omega Git Intelligence Layer v3 complete."
