import time
import traceback
import json
import os
from datetime import datetime

from omega_adaptive_convergence_v15 import OmegaAdaptiveConvergenceV15


# -----------------------------
# CONFIG
# -----------------------------
LOG_FILE = "omega_v15.log"
MEMORY_DUMP_FILE = "omega_v15_memory_dump.json"
CHECKPOINT_FILE = "omega_v15_checkpoint.json"

BRAINS = ["brain_0", "brain_1", "brain_2", "brain_3"]


# -----------------------------
# LOGGING
# -----------------------------
def log(msg):
    line = f"[{datetime.now().isoformat()}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# -----------------------------
# MEMORY SAVE
# -----------------------------
def save_memory(core):
    try:
        data = {
            "step": core.step_count,
            "scores": core.scores,
            "memory": core.memory[-50:]  # last 50 only (safe)
        }
        with open(MEMORY_DUMP_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log(f"[MEMORY ERROR] {e}")


# -----------------------------
# CHECKPOINT SAVE
# -----------------------------
def save_checkpoint(core):
    try:
        data = {
            "step": core.step_count,
            "scores": core.scores
        }
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log(f"[CHECKPOINT ERROR] {e}")


# -----------------------------
# MAIN DAEMON LOOP
# -----------------------------
def run_daemon():
    log("======================================")
    log("OMEGA v15 DAEMON STARTING")
    log("======================================")

    core = OmegaAdaptiveConvergenceV15(BRAINS)

    last_save = time.time()
    last_checkpoint = time.time()

    restart_count = 0

    while True:
        try:
            state = core.step()

            log(f"STEP {state['step']} | TOP: {state['top']} | SIZE: {state['memory_size']}")

            # periodic memory dump (every 10 sec)
            if time.time() - last_save > 10:
                save_memory(core)
                last_save = time.time()

            # checkpoint save (every 30 sec)
            if time.time() - last_checkpoint > 30:
                save_checkpoint(core)
                last_checkpoint = time.time()

            time.sleep(0.2)  # prevents CPU freeze

        except KeyboardInterrupt:
            log("SHUTDOWN REQUESTED")
            save_memory(core)
            save_checkpoint(core)
            break

        except Exception as e:
            restart_count += 1

            log("======================================")
            log(f"[CRASH DETECTED] Restart #{restart_count}")
            log(str(e))
            log(traceback.format_exc())
            log("RECOVERING SYSTEM...")
            log("======================================")

            time.sleep(1.5)

            # hard recovery (reinitialize core safely)
            try:
                core = OmegaAdaptiveConvergenceV15(BRAINS)
            except Exception as e2:
                log(f"[FATAL REINIT FAILURE] {e2}")
                time.sleep(5)


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_daemon()

# OPTIMIZED BY v29 ENGINE
