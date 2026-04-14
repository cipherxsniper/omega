#!/data/data/com.termux/files/usr/bin/bash

# ===== CONFIG =====
USERNAME="cipherxsniper"
REPO_NAME="omega-intelligence-layer-v3"
BRANCH="main"

echo "🧠 Initializing Git repo..."

cd ~/Omega || exit

git init

git config user.name "$USERNAME"
git config user.email "simpl3hoods@gmail.com"

echo "📦 Adding files..."
git add .

echo "🧾 Committing..."
git commit -m "Omega Intelligence Layer v3 snapshot"

echo "🌐 Setting branch..."
git branch -M $BRANCH

echo "🔗 Adding remote..."

git remote remove origin 2>/dev/null

git remote add origin https://github.com/$USERNAME/$REPO_NAME.git

echo "🚀 Pushing to GitHub..."

git push -u origin $BRANCH

echo "✅ DONE"
