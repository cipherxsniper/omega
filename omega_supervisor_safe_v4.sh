#!/bin/bash

MAX_RESTARTS=5
COUNT=0

start_observer() {
  echo "🧠 STARTING OBSERVER_V25"

  timeout 60s python3 core/observer_v25.py
  EXIT_CODE=$?

  echo "⚠️ OBSERVER EXIT CODE: $EXIT_CODE"

  if [ $EXIT_CODE -ne 0 ]; then
    COUNT=$((COUNT+1))

    if [ $COUNT -ge $MAX_RESTARTS ]; then
      echo "❌ TOO MANY FAILURES — STOPPING"
      exit 1
    fi

    sleep 2
    start_observer
  fi
}

start_observer
