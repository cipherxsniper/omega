#!/bin/bash
FOLDER="$1"
[[ -z "$FOLDER" ]] && FOLDER="."

for file in "$FOLDER"/*; do
    [[ ! -f "$file" ]] && continue
    ext="${file##*.}"
    case "$ext" in
        sh) bash "$file" ;;
        py) python3 "$file" ;;
        js) node "$file" ;;
        *) echo "[OmegaOS] Skipping $file (unknown type)" ;;
    esac
done
