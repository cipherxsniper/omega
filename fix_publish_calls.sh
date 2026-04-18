#!/bin/bash

echo "🧠 FIXING BROKEN publish() CALLS"

for f in wink_wink_brain_v*.py; do
    echo "patching $f"

    # convert publish(node, msg) → publish(node, msg, state, signal)

    sed -i 's/publish(NODE_ID, output)/publish(NODE_ID, output, state, signal)/g' "$f"

done

echo "🧠 CALLS FIXED"
