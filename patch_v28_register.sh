#!/bin/bash

FILE="wink_wink_brain_v28.py"

grep -q "register_node(" $FILE || sed -i '/while True/i NODE_NAME = "wink_wink_v28"\nregister_node(NODE_NAME)\n' $FILE

echo "v28 node registered"
