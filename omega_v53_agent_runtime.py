import os
import subprocess
import time

ROOT = os.path.expanduser("~/Omega")

AGENTS = {}

def discover_agents():
    agents = {}

    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                name = f.replace(".py", "")

                agents[name] = {
                    "path": path,
                    "status": "idle",
                    "process": None
                }

    return agents

def start_agent(name, agent):
    try:
        print(f"🧠 Starting agent: {name}")
        proc = subprocess.Popen(["python", agent["path"]])
        agent["process"] = proc
        agent["status"] = "running"
    except Exception as e:
        agent["status"] = f"error: {e}"

def run_all():
    global AGENTS
    AGENTS = discover_agents()

    print(f"🧠 Total agents discovered: {len(AGENTS)}")

    for name, agent in AGENTS.items():
        start_agent(name, agent)

if __name__ == "__main__":
    run_all()
