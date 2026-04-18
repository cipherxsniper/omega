#!/bin/bash

MAX_RESTARTS=3
COUNT=0
RUNNING=1

trap "echo '🛑 STOP SIGNAL RECEIVED'; RUNNING=0; exit 0" SIGINT SIGTERM

start_observer() {
  echo "🧠 STARTING OBSERVER_V25 FIXED"

  python3 core/observer_v25_fixed.py
  EXIT_CODE=$?

  echo "⚠️ OBSERVER EXIT CODE: $EXIT_CODE"

  if [ $RUNNING -eq 0 ]; then
    exit 0
  fi

  COUNT=$((COUNT+1))

  if [ $COUNT -ge $MAX_RESTARTS ]; then
    echo "❌ OBSERVER STOPPED (max restarts reached)"
    exit 1
  fi

  sleep 2
  start_observer
}

start_observer
