#!/bin/bash

FILE="wink_wink_v22.py"

# Replace the line: state = analyze(signal)
# with learning-enhanced version

sed -i 's/state = analyze(signal)/learn()\n    state = modulate_state(analyze(signal))/' $FILE

echo "✔ Loop upgraded with learning system"
