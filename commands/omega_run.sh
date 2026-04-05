#!/data/data/com.termux/files/usr/bin/env bash
# Prototype for Termux/OmegaOS hybrid testing

PROJECT_DIR="${PROJECT_DIR:-$PWD}"

omega_run() {
    local ext="$1"
    local file="$PROJECT_DIR/my_test.$ext"

    case "$ext" in
        sh)
            [[ ! -f "$file" ]] && echo "echo [OmegaOS Test] $file created and running!" > "$file"
            [[ -x $(command -v bash) ]] && bash "$file"
            ;;
        py)
            [[ ! -f "$file" ]] && echo "print('[OmegaOS Test] $file created and running!')" > "$file"
            [[ -x $(command -v python3) ]] && python3 "$file"
            ;;
        js)
            [[ ! -f "$file" ]] && echo "console.log('[OmegaOS Test] $file created and running!')" > "$file"
            [[ -x $(command -v node) ]] && node "$file"
            ;;
        json)
            [[ ! -f "$file" ]] && echo "{\"test\":\"$file created!\"}" > "$file"
            ;;
        *)
            echo "[OmegaOS] Unsupported extension: $ext"
            return 1
            ;;
    esac

    echo "[OmegaOS] $file created and executed if supported"
}
