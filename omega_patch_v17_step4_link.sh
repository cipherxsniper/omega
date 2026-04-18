#!/data/data/com.termux/files/usr/bin/bash

FILE="omega_quantum_field_v17.py"

# inject import
grep -q "omega_galaxy_memory_v17" $FILE || sed -i '1i from omega_galaxy_memory_v17 import step_galaxy_system, galaxy_influence' $FILE

# fix missing galaxy call in loop
grep -q "step_galaxy_system" $FILE || sed -i '/update_galaxies/d' $FILE
grep -q "step_galaxy_system" $FILE || sed -i '/orbit_nodes/a step_galaxy_system(particles)' $FILE

echo "✔ v17 GALAXY MEMORY PATCH APPLIED"
