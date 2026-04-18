#!/bin/bash

FILE="wink_wink_brain_v28.py"

sed -i 's/memory\["sentences"\].append/broadcast(NODE_NAME, sentence, state, signal)  # replaced/' $FILE

echo "broadcast patch applied"
