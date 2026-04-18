#!/bin/bash

echo "🧠 Omega v37 Recursive Identity System Booting..."

# CORE IDENTITY
nohup python omega_identity_core_v37.py &
nohup python omega_personality_evolution_v37.py &

# MEMORY + REFLECTION
nohup python memory_core.py &
nohup python omega_self_reflection_v37.py &
nohup python omega_contradiction_engine_v37.py &

# LANGUAGE LAYER
nohup python omega_language_v37.py &

# SYSTEM CORE
nohup python omega_bus_v36.py &
nohup python app.py &
nohup python bot.py &

echo "🧠 Omega v37 ONLINE — identity forming across time"
