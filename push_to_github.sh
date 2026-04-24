#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "🧠 Omega GitHub Auto-Push Starting..."

cd ~/Omega || exit

# -----------------------------
# INIT GIT IF NOT EXISTS
# -----------------------------
if [ ! -d ".git" ]; then
  echo "📦 Initializing git repo..."
  git init
fi

# -----------------------------
# DEFAULT IGNORE RULES (safe for AI projects)
# -----------------------------
cat > .gitignore << EOG
node_modules
__pycache__
*.pyc
.ollama
.env
.DS_Store
*.log
EOG

# -----------------------------
# ADD FILES (handles large repo)
# -----------------------------
echo "📁 Adding files..."
git add .

# -----------------------------
# COMMIT (auto message)
# -----------------------------
echo "💾 Committing..."
git commit -m "Omega full system sync $(date '+%Y-%m-%d %H:%M:%S')" || echo "Nothing to commit"

# -----------------------------
# SET REMOTE (CHANGE THIS)
# -----------------------------
REPO_URL="https://github.com/YOUR_USERNAME/YOUR_REPO.git"

if ! git remote | grep origin > /dev/null; then
  echo "🔗 Adding remote..."
  git remote add origin $REPO_URL
fi

# -----------------------------
# PUSH
# -----------------------------
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "🧠 DONE: Omega synced to GitHub"
