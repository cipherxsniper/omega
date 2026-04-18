#!/data/data/com.termux/files/usr/bin/bash

FILE="omega_quantum_field_v17.py"

# import consciousness layer
grep -q "omega_conscious_field_v20" $FILE || sed -i '1i from omega_conscious_field_v20 import step_conscious_field, register_observation' $FILE

# inject observation hooks into loop
grep -q "step_conscious_field" $FILE || sed -i '/step_dark_matter_system/a step_conscious_field(particles)' $FILE

# mark rendering as observation event (critical)
sed -i 's/render/\
register_observation(p.x, p.y, 1.0)\nrender/g' $FILE

echo "🧠 v20 CONSCIOUS FIELD INTEGRATED"
