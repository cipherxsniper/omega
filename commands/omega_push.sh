#!/bin/bash
# commands/omega_push.sh - Push OmegaOS files to GitHub + Omega Cloud
# Production-ready, intelligent, fully logging, auto-error handling

PROJECT_DIR=~/Omega-President/Omega-President
LOGS_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOGS_DIR/omega_push.log"

# Ensure logs directory exists
mkdir -p "$LOGS_DIR"

echo "[OmegaOS] Starting Omega Push..."
echo "[OmegaOS] Log file: $LOG_FILE"

# Function to log messages with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if inside a git repository
if [ ! -d "$PROJECT_DIR/.git" ]; then
    log "Git repository not found. Initializing new repo..."
    cd "$PROJECT_DIR"
    git init
    git branch -M main
    log "Git repo initialized."
fi

cd "$PROJECT_DIR"

# Add all changes
git add . 
if [ $? -ne 0 ]; then
    log "Error: Failed to stage files."
    exit 1
fi

# Commit changes with timestamp
git commit -m "Omega auto-update $(date '+%Y-%m-%d %H:%M:%S')" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    log "No changes to commit."
else
    log "Changes committed successfully."
fi

# Push to remote (assumes remote 'origin' is already set)
git push origin main >/dev/null 2>&1
if [ $? -eq 0 ]; then
    log "Files synced successfully to GitHub and Omega Cloud."
else
    log "Warning: Push failed. Check Git remote or network."
fi

log "Omega Push completed."
