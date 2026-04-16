import subprocess
import time
import os
import signal


class SwarmSupervisorV2:
    """
    V2 DAG Swarm Supervisor
    - process dependency graph (DAG)
    - crash-aware monitoring
    - clean restart logic
    - prevents exit-0 false crash loops
    """

    def __init__(self):
        self.base = os.getcwd()

        # -----------------------------
        # PROCESS DAG (ORDER MATTERS)
        # -----------------------------
        self.dag = {
            "bus": {
                "cmd": "python runtime_v7/core/v9_9_swarm_bus_v2.py",
                "log": "logs/bus.log",
                "deps": []
            },
            "v10": {
                "cmd": "python runtime_v7/core/v10_cognitive_event_memory_graph.py",
                "log": "logs/v10.log",
                "deps": ["bus"]
            },
            "v11": {
                "cmd": "python runtime_v7/core/v11_swarm_reasoning_engine.py",
                "log": "logs/v11.log",
                "deps": ["bus"]
            },
            "v12": {
                "cmd": "python runtime_v7/core/v12_swarm_cognition_layer.py",
                "log": "logs/v12.log",
                "deps": ["bus"]
            },
            "v13": {
                "cmd": "python runtime_v7/core/v13_swarm_self_optimization_engine.py",
                "log": "logs/v13.log",
                "deps": ["bus"]
            },
            "v14": {
                "cmd": "python runtime_v7/core/v14_distributed_swarm_sync.py",
                "log": "logs/v14.log",
                "deps": ["bus", "v10"]
            },
            "v15": {
                "cmd": "python runtime_v7/core/v15_crypto_swarm_identity.py",
                "log": "logs/v15.log",
                "deps": ["bus", "v14"]
            },
            "v16": {
                "cmd": "python runtime_v7/core/v16_swarm_federation_layer.py",
                "log": "logs/v16.log",
                "deps": ["v15"]
            },
            "v17": {
                "cmd": "python runtime_v7/core/v17_swarm_governance_layer.py",
                "log": "logs/v17.log",
                "deps": ["v16"]
            },
            "v18": {
                "cmd": "python runtime_v7/core/v18_swarm_cognition_layer.py",
                "log": "logs/v18.log",
                "deps": ["v17"]
            },
            "v19": {
                "cmd": "python runtime_v7/core/v19_swarm_prediction_engine.py",
                "log": "logs/v19.log",
                "deps": ["v18"]
            },
            "v20": {
                "cmd": "python runtime_v7/core/v20_swarm_self_optimization_engine.py",
                "log": "logs/v20.log",
                "deps": ["v19"]
            },
            "v21": {
                "cmd": "python runtime_v7/core/v21_swarm_coordination_layer.py",
                "log": "logs/v21.log",
                "deps": ["v20"]
            },
        }

        self.processes = {}
        self.restart_count = {}

        os.makedirs("logs", exist_ok=True)

    # -----------------------------
    # START PROCESS
    # -----------------------------
    def start_process(self, name):
        if name in self.processes:
            return

        info = self.dag[name]
        log_file = open(info["log"], "a")

        print(f"[START] {name} -> {info['cmd']}")

        proc = subprocess.Popen(
            info["cmd"],
            shell=True,
            stdout=log_file,
            stderr=log_file,
            preexec_fn=os.setsid
        )

        self.processes[name] = {
            "proc": proc,
            "log": info["log"]
        }

        self.restart_count[name] = 0

    # -----------------------------
    # START DEPENDENCIES FIRST
    # -----------------------------
    def can_start(self, name):
        for dep in self.dag[name]["deps"]:
            if dep not in self.processes:
                return False
            if self.processes[dep]["proc"].poll() is not None:
                return False
        return True

    # -----------------------------
    # MONITOR LOOP (V2 DAG FIXED)
    # -----------------------------
    def monitor(self):
        while True:
            for name in list(self.dag.keys()):

                if name not in self.processes:
                    if self.can_start(name):
                        self.start_process(name)
                    continue

                proc = self.processes[name]["proc"]
                code = proc.poll()

                if code is not None:

                    print("\n" + "=" * 60)
                    print(f"[CRASH DETECTED] {name}")
                    print(f"[EXIT CODE] {code}")
                    print(f"[LOG FILE] {self.processes[name]['log']}")
                    print("=" * 60 + "\n")

                    # 🔥 FIX: EXIT-0 IS NOT CRASH
                    if code == 0:
                        print(f"[INFO] {name} exited cleanly — NOT restarting")
                        del self.processes[name]
                        continue

                    # backoff restart
                    self.restart_count[name] += 1
                    delay = min(10, self.restart_count[name] * 2)

                    print(f"[RESTART] {name} in {delay}s")
                    time.sleep(delay)

                    self.start_process(name)

            time.sleep(5)

    # -----------------------------
    # START SUPERVISOR
    # -----------------------------
    def start(self):
        print("[SUPERVISOR V2] DAG ENGINE ONLINE")
        self.monitor()


if __name__ == "__main__":
    SwarmSupervisorV2().start()

