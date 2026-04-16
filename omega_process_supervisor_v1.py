import os
import time
import subprocess
import psutil

BATCH_SIZE = 10
BATCH_DELAY = 3

OMEGA_DIR = os.path.expanduser("~/Omega")

def discover_modules():
    modules = []
    for root, _, files in os.walk(OMEGA_DIR):
        for f in files:
            if f.endswith(".py") and "omega_process_supervisor" not in f:
                modules.append(os.path.join(root, f))
    return modules

def start_process(script_path):
    try:
        return subprocess.Popen(
            ["python", script_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"❌ Failed: {script_path} -> {e}")
        return None

def boot():
    print("\n🧠 OMEGA PROCESS SUPERVISOR v1 (BATCH MODE 10)\n")

    modules = discover_modules()
    print(f"📦 Modules discovered: {len(modules)}\n")

    batch = []
    batch_count = 0

    for m in modules:
        batch.append(m)

        if len(batch) >= BATCH_SIZE:
            batch_count += 1

            print(f"\n🧩 BATCH {batch_count} STARTING ({len(batch)} modules)\n")

            for script in batch:
                pid = start_process(script)
                if pid:
                    print(f"🚀 STARTED: {os.path.basename(script)}")

                time.sleep(0.2)

            print(f"\n🟢 BATCH {batch_count} COMPLETE")
            print(f"⏳ Cooling down {BATCH_DELAY}s...\n")

            time.sleep(BATCH_DELAY)
            batch = []

    # final batch
    if batch:
        batch_count += 1
        print(f"\n🧩 FINAL BATCH {batch_count} STARTING\n")

        for script in batch:
            pid = start_process(script)
            if pid:
                print(f"🚀 STARTED: {os.path.basename(script)}")
            time.sleep(0.2)

        print("\n🟢 FINAL BATCH COMPLETE")

    print("\n🧠 OMEGA SUPERVISOR ONLINE (10-BATCH MODE ACTIVE)\n")

if __name__ == "__main__":
    boot()
