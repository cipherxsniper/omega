# Ω NODE AGENT v9.6 — EXECUTES SERVICES LOCALLY

import subprocess
import time

class NodeAgent:
    def __init__(self, node_id):
        self.node_id = node_id
        self.processes = {}

    def start(self, service_name, cmd):
        print(f"[NODE {self.node_id}] starting {service_name}")

        proc = subprocess.Popen(cmd, shell=True)

        self.processes[service_name] = {
            "proc": proc,
            "cmd": cmd
        }

    def is_alive(self, service_name):
        proc = self.processes[service_name]["proc"]
        return proc.poll() is None

    def restart(self, service_name):
        cmd = self.processes[service_name]["cmd"]
        print(f"[NODE {self.node_id}] restarting {service_name}")
        self.start(service_name, cmd)
