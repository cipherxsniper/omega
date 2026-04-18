import subprocess
import time

# order matters
START_ORDER = [
    "omega_bus",
    "node_memory",
    "node_goal",
    "node_attention",
    "node_stability"
]

def start():
    print("🧠 OMEGA v7.2 DEPENDENCY STARTUP\n")

    for node in START_ORDER:
        try:
            subprocess.Popen(["python", f"{node}.py"])
            print(f"🚀 started: {node}")
            time.sleep(1)
        except:
            print(f"❌ failed: {node}")

if __name__ == "__main__":
    start()
