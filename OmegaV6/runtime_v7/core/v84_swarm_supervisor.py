import subprocess
import time
import os
import signal

class SwarmSupervisorV84:
    def __init__(self):
        self.processes = []
        self.running = True

    def start_node(self, module, port):
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        p = subprocess.Popen(
            ["python", "-m", module, str(port)],
            env=env
        )

        self.processes.append((p, module, port))
        return p

    def monitor(self):
        while self.running:
            for i, (p, module, port) in enumerate(self.processes):
                if p.poll() is not None:
                    print(f"[V8.4] NODE DEAD → RESTARTING {module}:{port}")

                    new_p = self.start_node(module, port)
                    self.processes[i] = (new_p, module, port)

            time.sleep(2)

    def run(self):
        print("[V8.4] SWARM SUPERVISOR ONLINE")

        self.start_node("runtime_v7.core.v8_3_launch_swarm", 6001)
        self.start_node("runtime_v7.core.v8_3_launch_swarm", 6002)

        self.monitor()
