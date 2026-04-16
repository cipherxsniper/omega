#!/data/data/com.termux/files/usr/bin/env bash
# OmegaOS-native Dev Hub: omega_dev_hub.sh
# Fully autonomous multi-language Dev Hub with parallel execution, live TUI, Cloud + GitHub

PROJECT_ROOT="${HOME}/Omega-President/Omega-President/projects"
OMEGA_CLOUD="${HOME}/Omega-President/Omega-President/OmegaCloud"
PROJECT_NAME="$1"

if [[ -z "$PROJECT_NAME" ]]; then
    echo "[OmegaOS] Usage: dev_hub <project_name>"
    exit 1
fi

PROJECT_DIR="$PROJECT_ROOT/$PROJECT_NAME"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "[OmegaOS] Project '$PROJECT_NAME' not found at $PROJECT_DIR"
    exit 1
fi

echo "[OmegaOS] === OmegaOS Dev Hub ==="
echo "[OmegaOS] Project: $PROJECT_NAME"
echo "[OmegaOS] Location: $PROJECT_DIR"

# Initialize logs
MASTER_LOG="$PROJECT_DIR/run.log"
echo "==== $(date) ====" >> "$MASTER_LOG"

# ===== Detect all source files recursively =====
declare -A EXT_TO_LANG=( ["py"]="python3" ["js"]="node" ["sh"]="bash" ["go"]="go" ["rs"]="rust" ["ts"]="ts-node" )
RUN_QUEUE=()

while IFS= read -r -d '' FILE; do
    EXT="${FILE##*.}"
    LANG="${EXT_TO_LANG[$EXT]}"
    if [[ -n "$LANG" ]]; then
        RUN_QUEUE+=("$LANG::$FILE")
    fi
done < <(find "$PROJECT_DIR/src" -type f -print0)

if [[ ${#RUN_QUEUE[@]} -eq 0 ]]; then
    echo "[OmegaOS] No executable source files detected in src/"
    exit 1
fi

echo "[OmegaOS] Detected ${#RUN_QUEUE[@]} executable file(s):"
for ITEM in "${RUN_QUEUE[@]}"; do
    echo "  - ${ITEM##*::} (${ITEM%%::*})"
done

# ===== Dependency Auto-Install =====
echo "[OmegaOS] Checking for dependencies..."
if [[ -f "$PROJECT_DIR/src/requirements.txt" ]]; then
    echo "[OmegaOS] Installing Python dependencies..."
    pip install -r "$PROJECT_DIR/src/requirements.txt"
fi
if [[ -f "$PROJECT_DIR/src/package.json" ]]; then
    echo "[OmegaOS] Installing Node.js dependencies..."
    cd "$PROJECT_DIR/src" && npm install && cd - >/dev/null
fi

# ===== Parallel Execution =====
declare -A PIDS
for ITEM in "${RUN_QUEUE[@]}"; do
    LANG="${ITEM%%::*}"
    FILE="${ITEM##*::}"
    LOG_FILE="$PROJECT_DIR/run_$(basename $FILE).log"

    if command -v "$LANG" >/dev/null 2>&1; then
        echo "[OmegaOS] Running $FILE using $LANG in background..."
        "$LANG" "$FILE" 2>&1 | tee -a "$LOG_FILE" &
        PIDS[$!]="$FILE::$LOG_FILE::$LANG"
    else
        echo "[OmegaOS] Skipping $FILE (Interpreter '$LANG' not found)"
        echo "[OmegaOS] Skipped $FILE due to missing interpreter" >> "$MASTER_LOG"
    fi
done

# ===== Live TUI Dashboard =====
echo "[OmegaOS] === Live Execution Dashboard ==="
while [[ ${#PIDS[@]} -gt 0 ]]; do
    for PID in "${!PIDS[@]}"; do
        FILE="${PIDS[$PID]%%::*}"
        LOG="${PIDS[$PID]#*::}"
        LANG="${LOG##*::}"
        LOG="${LOG%%::*}"
        if ! kill -0 "$PID" 2>/dev/null; then
            echo "[OmegaOS] Completed: $FILE ($LANG)"
            unset PIDS[$PID]
        fi
    done
    sleep 1
done

# ===== Consolidate logs =====
for ITEM in "${RUN_QUEUE[@]}"; do
    FILE="${ITEM##*::}"
    LOG_FILE="$PROJECT_DIR/run_$(basename $FILE).log"
    cat "$LOG_FILE" >> "$MASTER_LOG"
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

# ===== Final Dashboard =====
echo "[OmegaOS] === Project Dashboard ==="
echo "Files detected: ${#RUN_QUEUE[@]}"
echo "Cloud sync: $OMEGA_CLOUD_PROJECT"
if [[ -d "$PROJECT_DIR/.git" ]]; then
    echo "Git repository: present"
    echo "Last commit: $(git log -1 --pretty=format:'%h %s' 2>/dev/null)"
else
    echo "Git repository: none"
fi
echo "Last run consolidated log: $MASTER_LOG"
echo "[OmegaOS] Project '$PROJECT_NAME' execution complete."
