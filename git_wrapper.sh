#!/bin/bash

# Omega Git Wrapper (single control point)

if [[ "$1" == "push" ]]; then
  echo "[OMEGA WRAPPER] Redirecting push → controller"
  ~/Omega/omega_git_controller.sh
  exit 0
fi

# pass everything else through normally
git "$@"
