#!/data/data/com.termux/files/usr/bin/env bash
# OmegaOS-native helper: omega_run_project.sh (Cloud + GitHub-aware)
# Place in commands/ folder
# Usage: run_project <project_name>

PROJECT_ROOT="${HOME}/Omega-President/Omega-President/projects"
OMEGA_CLOUD="${HOME}/Omega-President/Omega-President/OmegaCloud"
PROJECT_NAME="$1"

if [[ -z "$PROJECT_NAME" ]]; then
    echo "[OmegaOS] Usage: run_project <project_name>"
    exit 1
fi

PROJECT_DIR="$PROJECT_ROOT/$PROJECT_NAME"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "[OmegaOS] Project '$PROJECT_NAME' not found at $PROJECT_DIR"
    exit 1
fi

echo "[OmegaOS] Running project '$PROJECT_NAME'..."

# ================= Detect entry points =================
declare -A LANG_FILES
LANG_FILES=(
    ["python3"]="main.py"
    ["node"]="index.js"
    ["bash"]="main.sh"
)

RUN_QUEUE=()
for LANG in "${!LANG_FILES[@]}"; do
    FILE="$PROJECT_DIR/src/${LANG_FILES[$LANG]}"
    if [[ -f "$FILE" ]]; then
        RUN_QUEUE+=("$LANG::$FILE")
    fi
done

if [[ ${#RUN_QUEUE[@]} -eq 0 ]]; then
    echo "[OmegaOS] No recognizable entry points found in src/ (main.py, index.js, main.sh)"
    exit 1
fi

# ================= Logging =================
LOG_FILE="$PROJECT_DIR/run.log"
echo "==== $(date) ====" >> "$LOG_FILE"

# ================= Execute entry points =================
for ITEM in "${RUN_QUEUE[@]}"; do
    LANG="${ITEM%%::*}"
    FILE="${ITEM##*::}"

    if [[ -x $(command -v "$LANG") ]]; then
        echo "[OmegaOS] Executing $FILE using $LANG..."
        echo "[OmegaOS] Running $FILE using $LANG" >> "$LOG_FILE"
        "$LANG" "$FILE" 2>&1 | tee -a "$LOG_FILE"
    else
        echo "[OmegaOS] Interpreter '$LANG' not found, skipping $FILE"
        echo "[OmegaOS] Interpreter '$LANG' not found, skipping $FILE" >> "$LOG_FILE"
    fi
done

# ================= Omega Cloud Sync =================
OMEGA_CLOUD_PROJECT="$OMEGA_CLOUD/$PROJECT_NAME"
mkdir -p "$OMEGA_CLOUD_PROJECT"
rsync -a --exclude='.git/' "$PROJECT_DIR/" "$OMEGA_CLOUD_PROJECT/"
echo "[OmegaOS] Project '$PROJECT_NAME' synced to Omega Cloud: $OMEGA_CLOUD_PROJECT"

# ================= GitHub Auto-Push =================
if [[ -d "$PROJECT_DIR/.git" ]]; then
    cd "$PROJECT_DIR" || exit
    git add .
    git commit -m "[OmegaOS Auto] Project run: $(date)" >/dev/null 2>&1
    git push origin main >/dev/null 2>&1
    echo "[OmegaOS] Project '$PROJECT_NAME' pushed to GitHub (if remote configured)"
fi

echo "[OmegaOS] Project '$PROJECT_NAME' execution complete."
