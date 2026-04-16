# ============================================================
# OMEGA MASTER LAUNCHER v1
# Runs FULL Omega ecosystem safely
# ============================================================

import os
import sys
import time
import traceback
import importlib.util

OMEGA_ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(OMEGA_ROOT, "omega_master.log")


# ============================================================
# LOGGER
# ============================================================
def log(msg):
    line = f"[OMEGA-MASTER] {time.strftime('%H:%M:%S')} {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except:
        pass


# ============================================================
# LOAD MODULE SAFE
# ============================================================
def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ============================================================
# BOOT SYSTEM
# ============================================================
def boot():

    log("BOOT SEQUENCE START")

    # ----------------------------
    # 1. LOAD ORCHESTRATOR
    # ----------------------------
    orch_path = os.path.join(OMEGA_ROOT, "system", "omega_orchestrator_v8.py")

    if not os.path.exists(orch_path):
        log("ORCHESTRATOR NOT FOUND")
        sys.exit(1)

    orchestrator_module = load_module(orch_path, "omega_orchestrator_v8")

    log("Orchestrator loaded")

    # ----------------------------
    # 2. CREATE ORCHESTRATOR
    # ----------------------------
    if hasattr(orchestrator_module, "OmegaOrchestrator"):
        core = orchestrator_module.OmegaOrchestrator()
    else:
        log("Invalid orchestrator interface")
        sys.exit(1)

    # ----------------------------
    # 3. START SYSTEM
    # ----------------------------
    try:
        log("Starting Omega Core...")

        core.run()

    except KeyboardInterrupt:
        log("Shutdown requested by user")

    except Exception as e:
        log("FATAL ERROR")
        log(str(e))
        traceback.print_exc()

    log("SYSTEM STOPPED")


# ============================================================
# ENTRY
# ============================================================
if __name__ == "__main__":
    boot()
