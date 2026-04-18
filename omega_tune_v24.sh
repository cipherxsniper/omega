#!/bin/bash

echo "🧠 tuning omega v24 stability..."

# reduce chaos
sed -i 's/"coupling": 0.08/"coupling": 0.05/g' omega_quantum_field_v24.py

echo "✔ coupling reduced"
echo "run again: python omega_quantum_field_v24.py"
