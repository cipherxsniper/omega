from omega_interface_registry_v43 import register_system_state, validate_patch

def safe_patch(old, new):
    registry = register_system_state()

    if not validate_patch(old, new, registry):
        print("[Ω PATCH GUARD] BLOCKED unsafe migration")
        return False

    print("[Ω PATCH GUARD] Approved migration")
    return True
