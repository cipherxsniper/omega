import os
import json
import subprocess
import time

from omega_manifest_builder_v3 import OmegaManifestBuilderV3
from omega_dag_engine_v3 import OmegaDAGEngineV3

class OmegaOSBrainV3:
    def __init__(self):
        self.base = os.path.expanduser("~/Omega/OmegaV6")
        self.manifest_builder = OmegaManifestBuilderV3()
        self.dag = OmegaDAGEngineV3()
        self.processes = {}

    def boot(self):
        print("\n🧠 OMEGA OS BRAIN v3 (TRUE SYSTEMD)\n")

        manifest = self.manifest_builder.build(self.base)

        print("📦 CLASSIFICATION COMPLETE")
        print(f"   Kernel: {len(manifest['kernel'])}")
        print(f"   Services: {len(manifest['service'])}")
        print(f"   Libraries (NOT RUNNABLE): {len(manifest['library'])}")
        print(f"   Tools: {len(manifest['tool'])}")
        print(f"   Data: {len(manifest['data'])}")

        # ONLY LOAD SERVICE MANIFEST
        with open("omega_service_manifest_v3.json") as f:
            service_manifest = json.load(f)["services"]

        order = self.dag.resolve(service_manifest)

        print("\n🧩 BOOT ORDER (SERVICES ONLY):")
        for o in order:
            print(" →", o)

        self.launch(service_manifest, order)

        self.monitor_loop()

    def launch(self, services, order):
        for name in order:
            svc = next((s for s in services if s["name"] == name), None)
            if not svc:
                continue

            path = os.path.join(self.base, svc["exec"])

            if not os.path.exists(path):
                print(f"❌ MISSING SERVICE: {svc['exec']}")
                continue

            p = subprocess.Popen(["python", path])
            self.processes[name] = p

            print(f"🚀 STARTED SERVICE: {name} PID={p.pid}")

    def monitor_loop(self):
        while True:
            time.sleep(5)

            for name, proc in list(self.processes.items()):
                if proc.poll() is not None:
                    print(f"⚠️ SERVICE DEAD: {name}")
                    print(f"♻️ RESTARTING: {name}")

                    # simple restart (v3 upgrade will add backoff intelligence)
                    self.processes.pop(name)
                    self.launch([{"name": name, "exec": "", "requires": []}], [name])

if __name__ == "__main__":
    OmegaOSBrainV3().boot()
