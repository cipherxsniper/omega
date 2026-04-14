# ============================================================
# OMEGA SYSTEM v6 — CORE LAUNCHER (UPDATED)
# Entry Point for Full Omega Ecosystem
# ============================================================

import os
import sys
import time
import traceback
import importlib.util

# ============================================================
# CONFIG
# ============================================================

OMEGA_ROOT = os.path.dirname(os.path.abspath(__file__))

# ✅ UPDATED TO ORCHESTRATOR V7
ORCHESTRATOR_PATH = os.path.join(
    OMEGA_ROOT,
    "system",
    "omega_orchestrator_v8.py"
)

LOG_FILE = os.path.join(OMEGA_ROOT, "omega_boot.log")


# ============================================================
# LOGGER
# ============================================================

def log(message: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[OMEGA][{timestamp}] {message}"
    print(line)

    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ============================================================
# SYSTEM CHECK
# ============================================================

def system_check():
    log("Running system checks...")

    checks = {
        "omega_root": os.path.exists(OMEGA_ROOT),
        "orchestrator_exists": os.path.exists(ORCHESTRATOR_PATH),
    }

    for k, v in checks.items():
        log(f"CHECK {k}: {'OK' if v else 'FAIL'}")

    if not all(checks.values()):
        raise RuntimeError("System check failed. Missing core components.")

    log("System check passed.")


# ============================================================
# DYNAMIC MODULE LOADER
# ============================================================

def load_orchestrator():
    log("Loading Omega Orchestrator v8...")

    try:
        spec = importlib.util.spec_from_file_location(
            "omega_orchestrator_v8",
            ORCHESTRATOR_PATH
        )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        log("Orchestrator loaded successfully.")
        return module

    except Exception as e:
        log(f"FAILED to load orchestrator: {e}")
        traceback.print_exc()
        raise


# ============================================================
# BOOT SEQUENCE
# ============================================================

def boot():
    log("======================================")
    log("OMEGA SYSTEM BOOT SEQUENCE INITIATED")
    log("======================================")

    system_check()

    orchestrator = load_orchestrator()

    log("Handing control to orchestrator...")

    # Preferred entry patterns
    if hasattr(orchestrator, "OmegaOrchestrator"):
        core = orchestrator.OmegaOrchestrator()
        if hasattr(core, "run"):
            core.run()
        else:
            log("Orchestrator missing .run() method")
    elif hasattr(orchestrator, "run"):
        orchestrator.run()
    else:
        log("No valid entry point found in orchestrator")
        raise RuntimeError("Invalid orchestrator interface")

    log("Omega system running.")


# ============================================================
# SAFETY WRAPPER
# ============================================================

if __name__ == "__main__":
    try:
        boot()
    except Exception as e:
        log("FATAL ERROR DURING BOOT")
        log(str(e))
        traceback.print_exc()
        sys.exit(1)
