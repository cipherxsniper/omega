#!/data/data/com.termux/files/usr/bin/env bash
# OmegaOS-native helper: omega_manage_project.sh
# Fully autonomous Project Manager: multi-language, Cloud + GitHub-aware, intelligent execution

PROJECT_ROOT="${HOME}/Omega-President/Omega-President/projects"
OMEGA_CLOUD="${HOME}/Omega-President/Omega-President/OmegaCloud"
PROJECT_NAME="$1"

if [[ -z "$PROJECT_NAME" ]]; then
    echo "[OmegaOS] Usage: manage_project <project_name>"
    exit 1
fi

PROJECT_DIR="$PROJECT_ROOT/$PROJECT_NAME"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "[OmegaOS] Project '$PROJECT_NAME' not found at $PROJECT_DIR"
    exit 1
fi

echo "[OmegaOS] === OmegaOS Project Manager ==="
echo "[OmegaOS] Project: $PROJECT_NAME"
echo "[OmegaOS] Location: $PROJECT_DIR"

# Initialize log
LOG_FILE="$PROJECT_DIR/run.log"
echo "==== $(date) ====" >> "$LOG_FILE"

# ===== Detect all source files =====
declare -A EXT_TO_LANG=( ["py"]="python3" ["js"]="node" ["sh"]="bash" ["go"]="go" ["rs"]="rust" )
RUN_QUEUE=()

while IFS= read -r -d '' FILE; do
    EXT="${FILE##*.}"
    LANG="${EXT_TO_LANG[$EXT]}"
    if [[ -n "$LANG" ]]; then
        RUN_QUEUE+=("$LANG::$FILE")
    fi
done < <(find "$PROJECT_DIR/src" -type f \( -name "*.py" -o -name "*.js" -o -name "*.sh" -o -name "*.go" -o -name "*.rs" \) -print0)

if [[ ${#RUN_QUEUE[@]} -eq 0 ]]; then
    echo "[OmegaOS] No executable source files detected in src/"
    exit 1
fi

echo "[OmegaOS] Detected ${#RUN_QUEUE[@]} executable file(s):"
for ITEM in "${RUN_QUEUE[@]}"; do
    echo "  - ${ITEM##*::} (${ITEM%%::*})"
done

# ===== Dependency Check =====
for LANG in "${!EXT_TO_LANG[@]}"; do
    if [[ ${#RUN_QUEUE[@]} -gt 0 ]] && ! command -v "$LANG" >/dev/null 2>&1; then
        echo "[OmegaOS] Warning: Interpreter '$LANG' not installed!"
    fi
done

# ===== Execute Each File =====
for ITEM in "${RUN_QUEUE[@]}"; do
    LANG="${ITEM%%::*}"
    FILE="${ITEM##*::}"
    if command -v "$LANG" >/dev/null 2>&1; then
        echo "[OmegaOS] Running $FILE using $LANG..."
        echo "[OmegaOS] [$LANG] $FILE run at $(date)" >> "$LOG_FILE"
        "$LANG" "$FILE" 2>&1 | tee -a "$LOG_FILE"
    else
        echo "[OmegaOS] Skipping $FILE (Interpreter '$LANG' not found)"
        echo "[OmegaOS] Skipped $FILE due to missing interpreter" >> "$LOG_FILE"
    fi
done

# ===== Cloud Sync =====
OMEGA_CLOUD_PROJECT="$OMEGA_CLOUD/$PROJECT_NAME"
mkdir -p "$OMEGA_CLOUD_PROJECT"
rsync -a --exclude='.git/' "$PROJECT_DIR/" "$OMEGA_CLOUD_PROJECT/"
echo "[OmegaOS] Project synced to Omega Cloud: $OMEGA_CLOUD_PROJECT"

# ===== GitHub Auto-Push =====
if [[ -d "$PROJECT_DIR/.git" ]]; then
    cd "$PROJECT_DIR" || exit
    git add .
    git commit -m "[OmegaOS Auto] Run: $(date)" >/dev/null 2>&1
    git push origin main >/dev/null 2>&1
    echo "[OmegaOS] GitHub push completed (if remote configured)"
fi

# ===== Dashboard =====
echo "[OmegaOS] === Project Dashboard ==="
echo "Files detected: ${#RUN_QUEUE[@]}"
echo "Cloud sync: $OMEGA_CLOUD_PROJECT"
if [[ -d "$PROJECT_DIR/.git" ]]; then
    echo "Git repository: present"
    echo "Last commit: $(git log -1 --pretty=format:'%h %s' 2>/dev/null)"
else
    echo "Git repository: none"
fi
echo "Last run logged in: $LOG_FILE"

echo "[OmegaOS] Project '$PROJECT_NAME' execution complete."
