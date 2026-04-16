#!/data/data/com.termux/files/usr/bin/env bash
# OmegaOS-native create_test helper (ENHANCED + FORCE FIXED)

PROJECT_DIR="${PROJECT_DIR:-$PWD}"

ext="$1"
mode="$2"

run_test() {
    local ext="$1"
    local file="$PROJECT_DIR/my_test.$ext"

    # 🔥 FIXED LOGIC HERE
    if [[ "$mode" == "force" || ! -f "$file" ]]; then
        case "$ext" in
            sh)
                echo "echo [OmegaOS Test] $file created and running!" > "$file"
                command -v bash >/dev/null && bash "$file"
                ;;
            py)
                echo "print('[OmegaOS Test] $file created and running!')" > "$file"
                command -v python3 >/dev/null && python3 "$file"
                ;;
            js)
                echo "console.log('[OmegaOS Test] $file created and running!')" > "$file"
                command -v node >/dev/null && node "$file"
                ;;
            json)
                echo "{\"test\":\"$file created!\"}" > "$file"
                ;;
        esac

        echo "[OmegaOS] $file created or re-created and executed"
    else
        echo "[OmegaOS] $file already exists"
    fi
}

# Multi-run
if [[ "$ext" == "all" ]]; then
    for t in sh py js json; do
        run_test "$t"
    done
    exit 0
fi

# Single run
run_test "$ext"
