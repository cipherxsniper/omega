#!/bin/bash

echo "🧠 Omega v36 Autonomous Cognitive OS Booting..."

# CORE GOVERNANCE FIRST
nohup python omega_governance_v36.py &
nohup python omega_bus_v36.py &

# MEMORY + LEARNING
nohup python memory_core.py &
nohup python omega_learning_loop_v36.py &

# DECISION ENGINE
nohup python omega_quantum_decision_v36.py &

# SELF-MOD SYSTEM
nohup python omega_self_modify_v36.py &

# LANGUAGE LAYER
nohup python omega_language_v36.py &

# OPTIONAL SIGNAL ENGINE
nohup python omega_signal_engine_v36.py &

# APP + BOT
nohup python app.py &
nohup python bot.py &

echo "🧠 Omega v36 ONLINE — governed cognition active"
