#!/bin/bash

echo "🧠 OMEGA v5 SELF-EVOLVING GIT INTELLIGENCE"
echo "=========================================="

BASE=$(pwd)
USER="cipherxsniper"
EMAIL="simpl3hoods@gmail.com"

WORKSPACE="$BASE/_omega_v5"
mkdir -p "$WORKSPACE"

# ---------------------------
# 1. Intelligent classification
# ---------------------------
classify_file () {
  FILE="$1"

  case "$FILE" in
    *brain*|*cognition*|*attention*|*ml*|*quantum*) echo "Omega-Brains" ;;
    *memory*|*state*|*graph*|*checkpoint*|*snapshot*) echo "Omega-Memory" ;;
    *engine*|*executor*|*swarm*|*cluster*|*bus*) echo "Omega-Engines" ;;
    *log*|*.log|*.tmp|nohup*) echo "IGNORE" ;;
    *) echo "Omega-Core" ;;
  esac
}

# ---------------------------
# 2. Commit intelligence
# ---------------------------
generate_commit_msg () {
  local repo=$1
  case "$repo" in
    Omega-Brains)
      echo "🧠 Cognitive evolution: brain subsystem optimization"
      ;;
    Omega-Memory)
      echo "🧬 Memory graph evolution and persistence stabilization"
      ;;
    Omega-Engines)
      echo "⚙️ Engine layer synchronization and execution tuning"
      ;;
    Omega-Core)
      echo "🔷 Core system evolution and structural refinement"
      ;;
    *)
      echo "🔁 Omega autonomous system update"
      ;;
  esac
}

# ---------------------------
# 3. Setup repo
# ---------------------------
setup_repo () {
  REPO=$1
  DIR="$WORKSPACE/$REPO"

  mkdir -p "$DIR"
  cd "$DIR" || exit

  git init
  git branch -M main
  git config user.name "$USER"
  git config user.email "$EMAIL"

  echo "🧹 .gitignore"
  cat > .gitignore <<EOF
*.log
*.tmp
nohup.out
__pycache__/
v*/backups/
EOF

  echo "📦 Collecting intelligent files..."

  while IFS= read -r file; do
    target=$(classify_file "$file")

    if [[ "$target" == "$REPO" ]]; then
      mkdir -p "$(dirname "$file")"
      cp --parents "$BASE/$file" "$DIR/" 2>/dev/null
    fi

  done < <(find "$BASE" -type f)

  git add .

  if git diff --cached --quiet; then
    echo "⚠️ No changes for $REPO"
    return
  fi

  MSG=$(generate_commit_msg "$REPO")
  git commit -m "$MSG"

  echo "🚀 Pushing $REPO"

  gh repo create "$USER/$REPO" --public --source=. --remote=origin --push 2>/dev/null

  git remote remove origin 2>/dev/null
  git remote add origin "https://github.com/$USER/$REPO.git"

  git push -u origin main --force
}

# ---------------------------
# 4. Self-evolving orchestration
# ---------------------------
echo "🧠 Analyzing system state..."

REPOS=("Omega-Core" "Omega-Brains" "Omega-Memory" "Omega-Engines")

for r in "${REPOS[@]}"; do
  setup_repo "$r"
done

echo ""
echo "🧠 OMEGA v5 EVOLUTION COMPLETE"
echo "✔ Self-classification active"
echo "✔ Semantic commit engine active"
echo "✔ Distributed repo intelligence active"
echo "✔ Evolution cycle complete"
