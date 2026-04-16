import os
import time
import subprocess
import traceback

ORCH = "system/omega_orchestrator_v11.py"

def kill_existing():
    print("[Ω-V11] Killing existing Omega processes...")
    os.system("pkill -f omega || true")

def launch():
    print("\n======================================")
    print("OMEGA UNIFIED KERNEL v11 (STABLE GOV)")
    print("======================================\n")

    while True:
        try:
            print(f"[UNIFIED-V11] launching {ORCH}")
            p = subprocess.Popen(["python", ORCH])
            p.wait()

            print("[UNIFIED-V11] orchestrator stopped. Restarting in 2s...")
            time.sleep(2)

        except Exception as e:
            print("[UNIFIED-V11 ERROR]", e)
            print(traceback.format_exc())
            time.sleep(3)

if __name__ == "__main__":
    kill_existing()
    launch()
