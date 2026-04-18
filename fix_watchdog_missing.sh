#!/bin/bash

echo "🧹 Fixing Omega v32 watchdog reference..."

# Remove watchdog launch if missing
sed -i '/watchdog/d' omega_v32_start.sh

echo "✅ watchdog disabled (missing file safe-mode)"
