#!/bin/bash

cd ~/Omega

echo "🧠 OMEGA v14 SAFE BOOT"

mkdir -p core memory logs nodes runtime bus

# STEP 1: REDIS SAFE START
bash start_redis_safe.sh

# STEP 2: OBSERVER SAFE START
bash start_observer_safe.sh

sleep 2

echo "📊 SYSTEM STATUS"
ps aux | grep redis
ps aux | grep observer

echo "🧠 OMEGA READY"
