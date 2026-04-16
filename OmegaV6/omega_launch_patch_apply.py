# PATCH INSTRUCTIONS FOR omega_init_system.py

# FIND THIS LINE:
# proc = launch(service)

# REPLACE WITH:

from omega_launch_guard import safe_launch

proc = safe_launch(service)
