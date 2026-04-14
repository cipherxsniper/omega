CORE_SERVICES = [
    "omega_kernel_v47.py",
    "omega_process_supervisor_v2.py",
    "omega_event_bus_v12.py",
    "omega_execution_engine_v7.py",
    "omega_meta_brain_v10.py",
    "omega_router_v37.py",
    "omega_memory_persistence_v1.py",
    "omega_identity_kernel_v25.py"
]

def filter_core(services):
    return [s for s in services if s in CORE_SERVICES]
