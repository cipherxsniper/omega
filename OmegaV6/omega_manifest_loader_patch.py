import os
import json

def load_manifest():
    """
    Omega Root-Aware Manifest Loader
    Prevents directory mismatch failures
    """

    search_paths = [
        "./omega_manifest.json",
        "../omega_manifest.json",
        os.path.expanduser("~/Omega/OmegaV6/omega_manifest.json"),
        os.path.expanduser("~/Omega/omega_manifest.json"),
    ]

    for path in search_paths:
        if os.path.exists(path):
            print(f"[OMEGA PATCH] Manifest found: {path}")
            with open(path, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("[OMEGA PATCH] ❌ Invalid JSON in manifest")
                    return None

    print("[OMEGA PATCH] ❌ Manifest not found anywhere")
    return None
