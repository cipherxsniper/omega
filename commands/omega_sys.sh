#!/bin/bash
# Executes any Bash command inside OmegaOS
if [[ $# -eq 0 ]]; then
    echo "[OmegaOS] Usage: sys <command> [args...]"
    exit 1
fi
"$@"
