from omega_node_registry_boot_v71_safe import OmegaNodeRegistryV71Safe

g = OmegaNodeRegistryV71Safe()

g.scan_scripts()
g.connect_all()

print("[Ω SAFE GRAPH V7.1]")
print(g.telemetry())
print("NODE COUNT:", g.node_count())
