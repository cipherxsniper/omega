#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "🧠 OMEGA GIT INTELLIGENCE LAYER v3 (ADVANCED)"
echo "--------------------------------------------"

PROJECT_DIR="$HOME/Omega"
REPO_NAME="omega-intelligence-core"
DESCRIPTION="Omega autonomous cognitive system snapshot"

cd "$PROJECT_DIR" || { echo "❌ Omega directory not found"; exit 1; }

# -----------------------------
# 1. Safety cleanup
# -----------------------------
echo "🧹 Cleaning temp/cache files..."

find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.log" -delete 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true

# -----------------------------
# 2. Init git if needed
# -----------------------------
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# -----------------------------
# 3. Set identity (safe local override)
# -----------------------------
git config user.name "cipherxsniper"
git config user.email "simpl3hoods@gmail.com"

# -----------------------------
# 4. Ensure GitHub CLI login
# -----------------------------
echo "🔐 Checking GitHub auth..."
gh auth status >/dev/null 2>&1 || {
    echo "❌ GitHub CLI not authenticated. Run: gh auth login"
    exit 1
}

# -----------------------------
# 5. Create repo if not exists
# -----------------------------
echo "🚀 Creating GitHub repository (if not exists)..."

gh repo view "$REPO_NAME" >/dev/null 2>&1 || {
    gh repo create "$REPO_NAME" \
        --public \
        --source=. \
        --remote=origin \
        --push
}

# -----------------------------
# 6. Ensure remote is correct
# -----------------------------
if ! git remote | grep -q origin; then
    echo "🔗 Adding GitHub remote..."
    git remote add origin "https://github.com/cipherxsniper/$REPO_NAME.git"
fi

# -----------------------------
# 7. Stage everything safely
# -----------------------------
echo "📦 Staging files..."
git add .

# -----------------------------
# 8. Smart commit message
# -----------------------------
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

git commit -m "🧠 Omega Intelligence Layer v3 Advanced Sync - $TIMESTAMP" || {
    echo "⚠️ No changes to commit"
}

# -----------------------------
# 9. Push with fallback
# -----------------------------
echo "☁️ Pushing to GitHub..."

git branch -M main

git push -u origin main || {
    echo "⚠️ Push failed, trying force-safe push..."
    git push -u origin main --force-with-lease
}

echo ""
echo "✅ OMEGA GIT INTELLIGENCE LAYER v3 COMPLETE"
echo "🌐 Repo: https://github.com/cipherxsniper/$REPO_NAME"
