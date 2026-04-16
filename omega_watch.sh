#!/data/data/com.termux/files/usr/bin/bash

clear
echo "🧠 OMEGA OBSERVER ONLINE"
echo "========================="

while true; do
  clear
  echo "🧠 OMEGA LIVE STATUS"
  echo "========================="

  echo ""
  echo "📊 CORE:"
  tail -n 3 ~/Omega/logs/core.log 2>/dev/null

  echo ""
  echo "🐍 PYTHON:"
  tail -n 3 ~/Omega/logs/python.log 2>/dev/null

  echo ""
  echo "🟢 NODE:"
  tail -n 3 ~/Omega/logs/node.log 2>/dev/null

  echo ""
  echo "🌐 REDIS:"
  ps aux | grep redis | grep -v grep

  sleep 3
done
