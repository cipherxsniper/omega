#!/bin/bash

FILE="wink_wink_v22.py"

# insert imports after first line (safe injection)
sed -i '1a from wink_learning_core_v23 import learn, modulate_state, get_policy' $FILE

echo "✔ Imports injected into v22"
