#!/bin/bash

echo "📡 Starting Redis..."
pkill redis-server 2>/dev/null

redis-server > redis.log 2>&1 &
sleep 1

if redis-cli ping | grep -q PONG; then
  echo "✅ Redis ONLINE"
else
  echo "❌ Redis FAILED"
  exit 1
fi

echo "🧠 Omega stack ready"
