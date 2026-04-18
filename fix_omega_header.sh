#!/bin/bash

FILE="omega_quantum_field_v20.py"

# keep only real python code (remove emoji headers)
grep -v "^🧠" $FILE | grep -v "^=" > temp.py

mv temp.py $FILE

echo "HEADER FIXED"
