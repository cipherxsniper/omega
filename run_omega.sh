#!/bin/bash

VERSION=$1

if [ -z "$VERSION" ]; then
  echo "Usage: bash run_omega.sh <version>"
  exit 1
fi

echo "🧬 Launching Omega v$VERSION"

bash "run_omega_v${VERSION}_evolution.sh"
