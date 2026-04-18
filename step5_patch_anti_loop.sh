#!/bin/bash

echo "🧠 STEP 5 — ADDING ANTI-LOOP FILTER"

for f in wink_wink_brain_v*.py; do
    echo "patching $f"

    awk '
    /while True:/ {
        print $0;
        print "    def anti_loop(msg, hist):";
        print "        return msg not in hist[-10:]";
        print "";
        print "    history = []";
        next;
    }
    {print}
    ' "$f" > tmp && mv tmp "$f"

done

echo "🧠 STEP 5 COMPLETE"
