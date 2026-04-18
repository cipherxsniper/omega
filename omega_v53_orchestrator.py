import os
import time
import subprocess

def start():
    print("🧠 OMEGA v53 ORCHESTRATOR STARTING")

    subprocess.Popen(["python", "omega_v53_graph_builder.py"])
    subprocess.Popen(["python", "omega_v53_agent_runtime.py"])

    print("✔ Graph + Agents launched")

if __name__ == "__main__":
    start()
