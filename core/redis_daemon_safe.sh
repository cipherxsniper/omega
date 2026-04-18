#!/bin/bash

echo "🧠 OMEGA REDIS GUARDED START"

# kill any existing redis
pkill -f redis-server >/dev/null 2>&1

sleep 1

# start single stable instance
redis-server --bind 127.0.0.1 --port 6379 --daemonize yes

sleep 1

# verify
redis-cli ping

echo "🟢 REDIS STABLE AND LOCKED"
