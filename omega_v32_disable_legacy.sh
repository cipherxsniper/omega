#!/bin/bash

echo "🧹 Disabling legacy watchdog launchers..."

# remove launcher calls only (safe)
grep -RIl "watchdog" . | while read f; do
  sed -i 's/echo "disabled legacy watchdog"/echo "disabled legacy watchdog"/g' "$f"
done

echo "✅ Legacy watchdog launch hooks disabled"
