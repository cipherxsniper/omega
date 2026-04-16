import subprocess
import time
import os

class Service:
    def __init__(self, name, cmd, depends=None):
        self.name = name
        self.cmd = cmd
        self.depends = depends or []
        self.process = None
        self.restarts = 0

class NexusKernelV94:
    def __init__(self):
        self.services = {}

    def register(self, name, cmd, depends=None):
        self.services[name] = Service(name, cmd, depends)

    def start_service(self, name):
        svc = self.services[name]

        for dep in svc.depends:
            if self.services[dep].process is None:
                self.start_service(dep)

        print(f"[Ω START] {name}")

        svc.process = subprocess.Popen(
            svc.cmd,
            shell=True,
            stdout=open(f"logs/{name}.log", "a"),
            stderr=subprocess.STDOUT
        )

    def start_all(self):
        for name in self.services:
            self.start_service(name)

    def monitor(self):
        while True:
            for name, svc in self.services.items():
                if svc.process and svc.process.poll() is not None:
                    svc.restarts += 1
                    print(f"[Ω RESTART] {name} ({svc.restarts})")

                    if svc.restarts <= 5:
                        self.start_service(name)
                    else:
                        print(f"[Ω KILL] {name} unstable")

            time.sleep(2)


if __name__ == "__main__":
    kernel = NexusKernelV94()

    kernel.register("bus", "python3 core/omega_neural_bus_v9_4.py")
    kernel.register("mesh", "python3 services/mesh.service.py", ["bus"])
    kernel.register("balancer", "python3 services/balancer.service.py", ["bus"])
    kernel.register("runtime", "python3 services/runtime.service.py", ["bus"])
    kernel.register("chat", "python3 services/chat.service.py", ["bus"])

    kernel.start_all()
    kernel.monitor()
