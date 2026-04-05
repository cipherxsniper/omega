# OmegaOS-native helper: omega_run_create_test.sh
# Place in PROJECT_DIR or OmegaOS commands folder

#!/data/data/com.termux/files/usr/bin/env bash
PROJECT_DIR="${PROJECT_DIR:-$PWD}"

ext="$1"
file="$PROJECT_DIR/my_test.$ext"

if ! [[ -f "$file" ]]; then
    case "$ext" in
        sh)
            echo "echo [OmegaOS Test] $file created and running!" > "$file"
            [[ -x $(command -v bash) ]] && bash "$file"
            ;;
        py)
            echo "print('[OmegaOS Test] $file created and running!')" > "$file"
            [[ -x $(command -v python3) ]] && python3 "$file"
            ;;
        js)
            echo "console.log('[OmegaOS Test] $file created and running!')" > "$file"
            [[ -x $(command -v node) ]] && node "$file"
            ;;
        json)
            echo "{\"test\":\"$file created!\"}" > "$file"
            ;;
        *)
            echo "[OmegaOS] Unsupported extension: $ext"
            exit 1
            ;;
    esac
fi

echo "[OmegaOS] $file created and executed if supported"
