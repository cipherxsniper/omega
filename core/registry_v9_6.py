VALID_TARGETS = {
    "kernel": "omega_kernel_v55.py",
    "chat": "omega_chat_assistant_v9_bus.py",
    "ml": "omega_ml_core_v12.py"
}

def resolve(target):
    if target not in VALID_TARGETS:
        print("[SWARM] ignoring phantom module:", target)
        return None
    return VALID_TARGETS[target]
