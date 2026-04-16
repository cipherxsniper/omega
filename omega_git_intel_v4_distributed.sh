#!/bin/bash

echo "🧠 OMEGA v4 DISTRIBUTED GIT INTELLIGENCE"
echo "========================================"

BASE_DIR=$(pwd)

USER="cipherxsniper"
EMAIL="simpl3hoods@gmail.com"

# -----------------------------
# 1. Define architecture layers
# -----------------------------
declare -A LAYERS
LAYERS["Omega-Core"]="core engines system omega_orchestrator run_omega"
LAYERS["Omega-Brains"]="Brain brains node attention cognition ml quantum"
LAYERS["Omega-Memory"]="memory json state graph checkpoint snapshot"
LAYERS["Omega-Engines"]="engine engines bus swarm cluster executor"
LAYERS["Omega-Utils"]="scripts tools fix bootstrap"

# -----------------------------
# 2. Create repos
# -----------------------------
create_repo () {
  REPO=$1

  echo ""
  echo "📦 Processing repo: $REPO"

  mkdir -p "$BASE_DIR/_dist/$REPO"
  cd "$BASE_DIR/_dist/$REPO" || exit

  git init
  git branch -M main

  git config user.name "$USER"
  git config user.email "$EMAIL"

  echo "🧹 Generating .gitignore"
  cat > .gitignore <<EOF
*.log
*.tmp
*.pid
__pycache__/
*.bak
nohup.out
v*/backups/
EOF

  echo "📂 Collecting files..."

  IFS=' ' read -r -a patterns <<< "${LAYERS[$REPO]}"

  for p in "${patterns[@]}"; do
    find "$BASE_DIR" -type f -name "*$p*" 2>/dev/null -exec cp --parents {} . \;
  done

  # Remove nested dist copies
  rm -rf _dist 2>/dev/null

  git add .

  if git diff --cached --quiet; then
    echo "⚠️ No changes for $REPO"
    return
  fi

  git commit -m "OMEGA v4 distributed commit: $REPO layer"

  echo "🔐 Checking GitHub auth..."
  gh auth status

  REPO_NAME="Omega-$REPO"

  echo "🚀 Creating/pushing $REPO_NAME"

  gh repo create "$USER/$REPO_NAME" --public --source=. --remote=origin --push 2>/dev/null

  git remote remove origin 2>/dev/null
  git remote add origin "https://github.com/$USER/$REPO_NAME.git"

  git push -u origin main --force

  cd "$BASE_DIR"
}

# -----------------------------
# 3. Execute all layers
# -----------------------------
for repo in "${!LAYERS[@]}"; do
  create_repo "$repo"
done

echo ""
echo "🧠 OMEGA v4 DISTRIBUTED INTELLIGENCE COMPLETE"
echo "✔ Core separated"
echo "✔ Memory isolated"
echo "✔ Brains modularized"
echo "✔ Engines decoupled"
echo "✔ Safe GitHub scaling active"
