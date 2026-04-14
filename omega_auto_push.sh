#!/data/data/com.termux/files/usr/bin/env bash
# OmegaOS-native: Auto GitHub & Cloud Push

REPO_DIR="${HOME}/Omega-President/Omega-President/omega"
OMEGA_CLOUD="${HOME}/Omega-President/Omega-President/OmegaCloud"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "[OmegaOS] Starting Auto Push..."

# 1️⃣ Move to repo
cd "$REPO_DIR" || { echo "[OmegaOS] Repo not found!"; exit 1; }

# 2️⃣ Add all files
git add .

# 3️⃣ Commit automatically
git commit -m "[OmegaOS Auto] Update: $TIMESTAMP" >/dev/null 2>&1

# 4️⃣ Push to GitHub via SSH
echo "[OmegaOS] Pushing to GitHub..."
git push origin main

# 5️⃣ Sync to Omega Cloud
mkdir -p "$OMEGA_CLOUD"
rsync -a --exclude='.git/' "$REPO_DIR/" "$OMEGA_CLOUD/"

echo "[OmegaOS] Omega Cloud sync complete: $OMEGA_CLOUD"
echo "[OmegaOS] Auto Push finished at $TIMESTAMP"
