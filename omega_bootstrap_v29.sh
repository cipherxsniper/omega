#!/bin/bash

echo "🧠 OMEGA BOOTSTRAP v29 STARTING..."

mkdir -p logs

# =========================
# 1. REDIS BOOTSTRAP
# =========================
echo "📡 Checking Redis..."

if ! pgrep redis-server > /dev/null; then
  echo "📡 Starting Redis..."
  redis-server --daemonize yes
fi

# wait until redis is alive
until redis-cli ping >/dev/null 2>&1; do
  echo "⏳ Waiting for Redis..."
  sleep 1
done

echo "✅ Redis ONLINE"

# =========================
# 2. CLEAN OLD PROCESSES
# =========================
echo "🧹 Cleaning old Omega processes..."
pkill -f swarm_brain_v27.py 2>/dev/null
pkill -f observer 2>/dev/null
pkill -f omega_node 2>/dev/null

sleep 1

# =========================
# 3. START BRAIN
# =========================
echo "🧠 Starting Brain..."

nohup python3 swarm_brain_v27.py > logs/brain.log 2>&1 &
echo "✅ Brain running"

# =========================
# 4. START NODE WATCHDOG (AUTO HEAL)
# =========================
echo "⚙️ Starting Node Watchdog..."

cat > omega_node_watchdog_v29.sh << 'EON'
#!/bin/bash

mkdir -p logs

while true; do
  COUNT=$(ps aux | grep observer_v27_node.py | grep -v grep | wc -l)

  if [ "$COUNT" -lt 3 ]; then
    echo "⚡ Node deficit detected: spawning nodes..."
    nohup python3 observer_v27_node.py > logs/node_auto.log 2>&1 &
  fi

  sleep 3
done
EON

chmod +x omega_node_watchdog_v29.sh

echo "disabled legacy watchdog"
echo "✅ Node watchdog running"

# =========================
# 5. CONTROL CENTER STREAM
# =========================
echo "📊 Starting Control Stream..."

tail -f logs/brain.log logs/watchdog.log logs/node_auto.log 2>/dev/null &
