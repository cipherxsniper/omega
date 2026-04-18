#!/bin/bash

FILE="omega_quantum_field_v17.py"

# remove old broken import lines if they exist
sed -i '/update_galaxies/d' $FILE
sed -i '/omega_galaxy/d' $FILE

# inject correct import at top
sed -i '1i from omega_galaxy_system_v17 import update_galaxies, galaxies, Galaxy' $FILE

# ensure loop call exists once
grep -q "update_galaxies(particles)" $FILE || echo "update_galaxies(particles)" >> $FILE

echo "✔ Galaxy system patched successfully"
