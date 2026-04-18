#!/bin/bash

echo "🧠 OMEGA v31 BOOTSTRAP STARTING..."

redis-server --daemonize yes

echo "⏳ Waiting for Redis..."

until redis-cli ping | grep -q PONG; do
  sleep 1
done

echo "✅ Redis ONLINE"
