#!/bin/bash
# Simple editor bridge
if [[ -z "$1" ]]; then
    echo "[OmegaOS] Usage: edit <file>"
    exit 1
fi
nano "$1"
