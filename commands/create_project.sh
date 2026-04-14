#!/data/data/com.termux/files/usr/bin/env bash

PROJECT_DIR="$HOME/Omega-President/Omega-President/projects"
project_name="$1"

if [[ -z "$project_name" ]]; then
    echo "[OmegaOS] Usage: create_project <name>"
    exit 1
fi

proj_path="$PROJECT_DIR/$project_name"

mkdir -p "$proj_path"

# Create intelligent structure
mkdir -p "$proj_path/src"
mkdir -p "$proj_path/config"

# Default files
echo "# $project_name" > "$proj_path/README.md"
echo "print('Hello from $project_name')" > "$proj_path/src/main.py"
echo "{\"project\":\"$project_name\"}" > "$proj_path/config/config.json"

echo "[OmegaOS] Project '$project_name' created at $proj_path"
