MAX_RESTARTS=5
COUNT=0

start_observer() {
  echo "🧠 STARTING OBSERVER_V24"

  python3 core/observer_v24.py
  EXIT_CODE=$?

  if [ $EXIT_CODE -ne 0 ]; then
    echo "⚠️ OBSERVER CRASHED ($EXIT_CODE)"
    COUNT=$((COUNT+1))

    if [ $COUNT -ge $MAX_RESTARTS ]; then
      echo "❌ OBSERVER STOPPED (too many crashes)"
      exit 1
    fi

    sleep 3
    start_observer
  fi
}

start_observer
