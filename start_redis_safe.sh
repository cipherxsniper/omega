#!/bin/bash

echo "📡 STARTING SAFE REDIS..."

pkill redis-server 2>/dev/null

redis-server --daemonize yes

# HARD WAIT LOOP (REAL FIX)
for i in {1..30}; do
  redis-cli ping >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ REDIS READY"
    exit 0
  fi

  echo "⏳ waiting for redis... ($i)"
  sleep 1
done

echo "❌ REDIS FAILED TO START PROPERLY"
exit 1
