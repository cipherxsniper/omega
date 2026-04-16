#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Omega Git Auto Push Starting..."

# Ensure git exists
if ! command -v git &> /dev/null; then
  echo "❌ Git not installed. Run: pkg install git -y"
  exit 1
fi

# Initialize repo if not already
if [ ! -d .git ]; then
  echo "📦 Initializing git repository..."
  git init
fi

# Ensure remote exists
if ! git remote | grep -q origin; then
  echo "🔗 Adding remote origin..."
  git remote add origin https://github.com/cipherxsniper/omega.git
fi

# Set branch
git branch -M main

# Stage everything
echo "📁 Adding files..."
git add .

# Commit (auto fallback message)
echo "💾 Creating commit..."
git commit -m "Omega auto update $(date)" || echo "⚠️ Nothing new to commit"

# Push
echo "📤 Pushing to GitHub..."
git push -u origin main

echo "✅ Done."
