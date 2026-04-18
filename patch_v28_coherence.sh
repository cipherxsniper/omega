#!/bin/bash

FILE="wink_wink_brain_v28.py"

sed -i 's/signal =/signal = (signal + get_global_state()) \/ 2  # global coherence/' $FILE

echo "coherence stabilization applied"
