#!/data/data/com.termux/files/usr/bin/env bash
# OmegaOS-native helper: run_project.sh
# Place in commands/ folder
# Usage: run_project <project_name>

PROJECT_ROOT="${HOME}/Omega-President/Omega-President/projects"
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

# Detect the entry point automatically
ENTRY=""
LANGUAGE=""

# Python
if [[ -f "$PROJECT_DIR/src/main.py" ]]; then
    ENTRY="$PROJECT_DIR/src/main.py"
    LANGUAGE="python3"
# Node.js
elif [[ -f "$PROJECT_DIR/src/index.js" ]]; then
    ENTRY="$PROJECT_DIR/src/index.js"
    LANGUAGE="node"
# Shell
elif [[ -f "$PROJECT_DIR/src/main.sh" ]]; then
    ENTRY="$PROJECT_DIR/src/main.sh"
    LANGUAGE="bash"
else
    echo "[OmegaOS] No recognizable entry point found (main.py, index.js, main.sh)"
    exit 1
fi

# Run the project intelligently
if [[ -x $(command -v "$LANGUAGE") ]]; then
    echo "[OmegaOS] Executing $ENTRY using $LANGUAGE..."
    $LANGUAGE "$ENTRY"
else
    echo "[OmegaOS] Required interpreter '$LANGUAGE' not found"
    exit 1
fi

echo "[OmegaOS] Project '$PROJECT_NAME' execution complete."
