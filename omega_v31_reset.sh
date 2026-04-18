#!/bin/bash

echo "🧹 Cleaning Omega v31 state..."

pkill -f omega || true
pkill -f swarm || true
pkill -f observer || true
pkill -f watchdog || true

redis-cli del omega.nodes.active
redis-cli del omega.brain.leader
redis-cli del omega.consensus.last
redis-cli del omega.consensus.score

echo "✅ Clean state ready"
