#!/bin/bash

FILE="wink_wink_brain_v28.py"

grep -q "omega_global_thought_bus_v23" $FILE || sed -i '1i from omega_global_thought_bus_v23 import register_node, broadcast, get_recent, get_global_state' $FILE

echo "v28 imports patched"
