#!/bin/bash

echo "🧠 Applying omega_global_thought_bus_v23 to all wink_wink_v*.py files..."

for file in wink_wink_v*.py; do
  echo "Patching $file"

  cat << 'PATCH' > tmp_patch.py
import time
from omega_global_thought_bus_v23 import run_observer

while True:
    try:
        print(run_observer("$file"))
        time.sleep(1)
    except KeyboardInterrupt:
        break
PATCH

  cp tmp_patch.py "$file"

done

rm -f tmp_patch.py

echo "🧠 All wink_wink versions now unified under global thought bus v23"
