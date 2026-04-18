#!/bin/bash

CORE_IMPORT="from wink_wink_core_v22 import core_think"

echo "🧠 Attaching core v22 to all wink_wink_v*.py files..."

for file in wink_wink_v*.py; do
    if [ -f "$file" ]; then

        # skip core file itself
        if [[ "$file" == "wink_wink_core_v22.py" ]]; then
            continue
        fi

        echo "Patching $file"

        # only add import if missing
        if ! grep -q "core_think" "$file"; then
            sed -i "1i $CORE_IMPORT" "$file"
        fi

        # optional safety marker
        if ! grep -q "WINK_CORE_V22_ACTIVE" "$file"; then
            sed -i "1i # WINK_CORE_V22_ACTIVE" "$file"
        fi

    fi
done

echo "🧠 All wink_wink versions now share unified sentence intelligence core."
