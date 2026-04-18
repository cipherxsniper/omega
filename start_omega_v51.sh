#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 Starting Omega v51 (STABLE MODE)"

pkill -f omega_v51_cluster.py || true

nohup python omega_v51_cluster.py > cluster.log 2>&1 &

sleep 3

nohup python omega_v51_dashboard.py > dashboard.log 2>&1 &

echo "✔ Omega v51 running"
echo "→ API: http://127.0.0.1:8080/status"
