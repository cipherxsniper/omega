#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "🧠 Omega SAFE GitHub Sync Starting..."

cd ~/Omega || exit

# -----------------------------
# INIT GIT
# -----------------------------
if [ ! -d ".git" ]; then
  git init
fi

# -----------------------------
# CLEAN IGNORE STRATEGY
# -----------------------------
cat > .gitignore << EOG
# AI models (VERY IMPORTANT)
.ollama/
models/
node_modules/
__pycache__/
*.pyc

# logs/cache
*.log
.cache/
*.tmp

# system noise
omega_env/
v29_backups/
.git/
EOG

# -----------------------------
# STAGE ONLY CODE
# -----------------------------
echo "📁 Staging system files..."
git add .

# -----------------------------
# COMMIT
# -----------------------------
git commit -m "Omega safe sync $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes"

# -----------------------------
# REMOTE (CHANGE THIS)
# -----------------------------
REPO="https://github.com/cipherxsniper/Omega.git"

if ! git remote | grep origin > /dev/null; then
  git remote add origin $REPO
fi

# -----------------------------
# PUSH
# -----------------------------
git branch -M main
git push -u origin main

echo "🧠 Omega SAFE SYNC COMPLETE"
