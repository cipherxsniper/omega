#!/bin/bash

while true; do
  echo "🧠 OMEGA V10 RESTART LOOP STARTED"

  bash run_omega_v10.sh >> logs/v10_forever.log 2>&1

  echo "⚠️ V10 CRASHED — RESTARTING IN 2s"
  sleep 2
done
