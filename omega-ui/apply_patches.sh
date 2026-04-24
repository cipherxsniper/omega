#!/data/data/com.termux/files/usr/bin/bash

APP=~/Omega/omega-ui/src/App.js

echo "🧠 Injecting Omega Step Patch..."

# insert STEP PATCH before step() closing bracket marker (manual fallback safe append)
echo "\n// === OMEGA STEP PATCH ===" >> $APP
cat patch_step_function.js >> $APP

echo "\n🧠 Injecting Omega Draw Patch..."
echo "\n// === OMEGA DRAW PATCH ===" >> $APP
cat patch_draw_function.js >> $APP

echo "✅ Patches applied"
