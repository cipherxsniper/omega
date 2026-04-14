SERVICE_PRIORITY = {
    # 🔴 CORE (must run)
    "omega_kernel_v47.py": "CORE",
    "omega_process_supervisor_v2.py": "CORE",
    "omega_event_bus_v12.py": "CORE",

    # 🟡 SUPPORT (important but not critical)
    "omega_execution_engine_v7.py": "SUPPORT",
    "omega_meta_brain_v10.py": "SUPPORT",
    "omega_router_v37.py": "SUPPORT",

    # 🔵 LAZY (spawn on demand)
    "omega_memory_persistence_v1.py": "LAZY",
    "omega_identity_kernel_v25.py": "LAZY",
}

PRIORITY_ORDER = {
    "CORE": 0,
    "SUPPORT": 1,
    "LAZY": 2
}

def get_priority(service):
    return SERVICE_PRIORITY.get(service, "LAZY")
