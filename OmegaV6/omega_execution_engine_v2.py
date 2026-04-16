import subprocess
import os

class OmegaExecutionEngineV2:
    def __init__(self, base_path="~/Omega"):
        self.base_path = os.path.expanduser(base_path)
        self.processes = {}

    def start(self, module):
        path = os.path.join(self.base_path, module)

        if not os.path.exists(path):
            print(f"❌ MISSING: {module}")
            return None

        proc = subprocess.Popen(
            ["python", path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.processes[module] = proc.pid
        print(f"🚀 STARTED: {module} PID={proc.pid}")
        return proc.pid

    def kill(self, module):
        if module in self.processes:
            try:
                os.kill(self.processes[module], 9)
            except:
                pass
