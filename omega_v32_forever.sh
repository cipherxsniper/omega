#!/bin/bash

mkdir -p logs

echo "🧠 OMEGA V32 FOREVER SUPERVISOR STARTED"

while true; do
  nohup bash omega_v32_master.sh > logs/master.log 2>&1

  echo "⚠️ MASTER EXITED — RESTARTING IN 2s"
  sleep 2
done
