#!/bin/bash

for f in wink_wink_brain_v*.py; do
  echo "Patching $f"

  sed -i '1i from wink_wink_global_brain import GLOBAL_BRAIN' "$f"

  sed -i '/print(/i \
GLOBAL_BRAIN.publish(__file__, state if "state" in locals() else "unknown", signal if "signal" in locals() else 0.5, sentence if "sentence" in locals() else "tick")' "$f"

done

echo "All wink_wink brains connected to global memory bus."
