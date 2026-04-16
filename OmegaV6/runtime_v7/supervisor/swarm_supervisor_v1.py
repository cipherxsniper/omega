import subprocess
import time
import os
import signal
from datetime import datetime


class SwarmSupervisorV1:
    """
    Systemd-style swarm supervisor for V9–V21 stack
    - persistent process tracking
    - crash detection
    - clean vs crash exit handling
    - controlled restart loop
    """

    def __init__(self):
        self.base_path = "runtime_v7/core"

        # PROCESS MAP (EDIT HERE ONLY)
        self.PROCESS_MAP = {
            "BUS_V9_9": {
                "cmd": f"python {self.base_path}/v9_9_swarm_bus_v2.py",
                "log": "logs/bus.log",
                "restart": True
            },
            "V10": {
                "cmd": f"python {self.base_path}/v10_cognitive_event_memory_graph.py",
                "log": "logs/v10.log",
                "restart": True
            },
            "V11": {
                "cmd": f"python {self.base_path}/v11_swarm_reasoning_engine.py",
                "log": "logs/v11.log",
                "restart": True
            },
            "V12": {
                "cmd": f"python {self.base_path}/v12_swarm_cognition_layer.py",
                "log": "logs/v12.log",
                "restart": True
            },
            "V13": {
                "cmd": f"python {self.base_path}/v13_swarm_self_optimization_engine.py",
                "log": "logs/v13.log",
                "restart": True
            }
        }

        self.processes = {}

        os.makedirs("logs", exist_ok=True)

        print("[SUPERVISOR V1] INITIALIZED")

    # ----------------------------
    # START PROCESS
    # ----------------------------
    def start_layer(self, name):
        cfg = self.PROCESS_MAP[name]

        log_file = open(cfg["log"], "a")

        print(f"[START] {name} -> {cfg['cmd']}")

        proc = subprocess.Popen(
            cfg["cmd"],
            shell=True,
            stdout=log_file,
            stderr=log_file,
            preexec_fn=os.setsid
        )

        self.processes[name] = {
            "proc": proc,
            "log": cfg["log"],
            "cmd": cfg["cmd"],
            "log_file": log_file
        }

    # ----------------------------
    # RESTART LOGIC
    # ----------------------------
    def restart_layer(self, name):
        print(f"[RESTART] {name}")

        try:
            old = self.processes[name]["proc"]
            os.killpg(os.getpgid(old.pid), signal.SIGTERM)
        except Exception:
            pass

        time.sleep(2)
        self.start_layer(name)

    # ----------------------------
    # MONITOR (systemd-style)
    # ----------------------------
    def monitor(self):
        while True:
            for name, info in self.processes.items():
                p = info["proc"]

                if p.poll() is not None:
                    code = p.returncode

                    print("\n" + "=" * 60)
                    print(f"[CRASH REPORT] {name}")
                    print(f"[EXIT CODE] {code}")
                    print(f"[LOG FILE] {info['log']}")
                    print("=" * 60 + "\n")

                    # ONLY restart on real crash
                    if code != 0:
                        time.sleep(3)
                        self.restart_layer(name)
                    else:
                        print(f"[OK] {name} exited cleanly")

            time.sleep(5)

    # ----------------------------
    # BOOT ALL
    # ----------------------------
    def start_all(self):
        print("[SUPERVISOR V1] BOOTING STACK")

        for name in self.PROCESS_MAP:
            self.start_layer(name)
            time.sleep(1)

        print("[SUPERVISOR V1] ALL LAYERS RUNNING")

        self.monitor()


if __name__ == "__main__":
    SwarmSupervisorV1().start_all()
