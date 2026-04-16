#!/data/data/com.termux/files/usr/bin/bash

SRC="$HOME/Omega"
SNAP="$HOME/Omega_SNAPSHOT"
DEST="omega_drive:OmegaCloud/OmegaBackup"

echo "🧠 Creating Omega snapshot..."

# wipe old snapshot
rm -rf "$SNAP"
mkdir -p "$SNAP"

# copy ONLY stable files
rsync -av \
  --exclude "*.log" \
  --exclude "*.tmp" \
  --exclude "__pycache__" \
  --exclude "*.pid" \
  --exclude "*.lock" \
  --exclude "omega_state.json" \
  --exclude "omega_memory.json" \
  "$SRC/" "$SNAP/"

echo "☁️ Syncing snapshot to Drive..."

rclone sync "$SNAP" "$DEST" \
  --fast-list \
  --transfers 4 \
  --checkers 8 \
  --retries 3

echo "✅ Snapshot sync complete"
