def normalize_services(self, discovered, manifest):
    discovered_set = set(discovered)

    normalized = []
    degraded = []
    missing_core = []

    for svc in manifest:
        if svc["exec"] in discovered_set:
            normalized.append(svc)
        else:
            # classify severity instead of just rejecting
            if svc["name"] in ["runtime", "kernel"]:
                missing_core.append(svc)
                print(f"❌ CRITICAL MISSING CORE: {svc['exec']}")
            else:
                degraded.append(svc)
                print(f"⚠️ DEGRADED SERVICE (skipped): {svc['exec']}")

    return normalized, degraded, missing_core
