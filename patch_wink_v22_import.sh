#!/bin/bash

FILE="wink_wink_v22.py"

# add import at top if not exists
grep -q "wink_wink_core_v22" $FILE || sed -i '1i from wink_wink_core_v22 import core_think' $FILE

echo "patched v22 with core memory + sentence engine"
