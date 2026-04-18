#!/bin/bash

echo "🧠 STEP 4 — ADDING CROSS-BRAIN INFLUENCE"

for f in wink_wink_brain_v*.py; do
    echo "patching influence in $f"

    # inject influence block into loop
    awk '
    /while True:/ {
        print $0;
        print "    recent = fetch_recent(5)";
        print "    if recent:";
        print "        influence = sum(m[\"signal\"] for m in recent) / len(recent)";
        print "        try:";
        print "            signal = (signal + influence) / 2";
        print "        except:";
        print "            pass";
        next;
    }
    {print}
    ' "$f" > tmp && mv tmp "$f"

done

echo "🧠 STEP 4 COMPLETE"
