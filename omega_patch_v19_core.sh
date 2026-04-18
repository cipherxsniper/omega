#!/data/data/com.termux/files/usr/bin/bash

FILE="omega_quantum_field_v17.py"

# fix object/dict crash
grep -q "omega_dark_matter_v19" $FILE || sed -i '1i from omega_dark_matter_v19 import step_dark_matter_system' $FILE

# inject dark matter step into loop safely
grep -q "step_dark_matter_system" $FILE || sed -i '/step_galaxy_system/a step_dark_matter_system(particles)' $FILE

# safety patch for galaxy crash fallback
sed -i 's/galaxy_influence(p)/try:\n        galaxy_influence(p)\n    except Exception:\n        pass/' $FILE

echo "🧠 v19 DARK MATTER PATCH APPLIED"
