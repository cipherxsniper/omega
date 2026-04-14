#!/bin/bash

echo "🧠 OMEGA GIT INTELLIGENCE LAYER v3 (FINAL)"
echo "----------------------------------------"

# 1. Ensure git repo exists
if [ ! -d .git ]; then
  echo "📦 Initializing git repository..."
  git init
fi

# 2. Set identity (safe fallback)
git config user.name "cipherxsniper"
git config user.email "simpl3hoods@gmail.com"

# 3. Ensure main branch
git branch -M main

# 4. Clean unwanted runtime files
echo "🧹 Cleaning runtime junk..."
find . -name "*.log" -delete 2>/dev/null
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.pid" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# 5. Stage EVERYTHING important
echo "📦 Staging files..."
git add .

# 6. Create commit if needed
if git diff --cached --quiet; then
  echo "⚠️ Nothing to commit"
else
  git commit -m "OMEGA INTELLIGENCE LAYER v3 - full system snapshot"
fi

# 7. Check GitHub auth
echo "🔐 Checking GitHub authentication..."
gh auth status

# 8. Create repo if missing
REPO_NAME="Omega-Intelligence-Layer"
echo "🚀 Ensuring GitHub repo exists: $REPO_NAME"

gh repo view cipherxsniper/$REPO_NAME >/dev/null 2>&1
if [ $? -ne 0 ]; then
  gh repo create $REPO_NAME --public --source=. --remote=origin --push
else
  git remote add origin https://github.com/cipherxsniper/$REPO_NAME.git 2>/dev/null
fi

# 9. Push safely
echo "☁️ Pushing to GitHub..."
git push -u origin main --force

# 10. Verify
echo "✅ Verifying remote..."
git ls-remote origin

echo "🧠 OMEGA GIT INTELLIGENCE v3 COMPLETE"
