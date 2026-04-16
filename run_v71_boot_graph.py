from omega_node_registry_boot_v71 import OmegaNodeRegistryV71

registry = OmegaNodeRegistryV71()

# 1. scan all omega modules as nodes
registry.scan_scripts()

# 2. auto-connect graph
registry.connect_all()

# 3. output system state
print("[Ω V71 SYSTEM TELEMETRY]")
print(registry.telemetry())

print("\nNODE COUNT:", registry.node_count())
