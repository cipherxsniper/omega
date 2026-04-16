import os
import json
import time
import subprocess
import threading

STATE_FILE = "omega_registry_state_v6.json"
MAX_RESTARTS = 3
HEARTBEAT_TIMEOUT = 10

# =========================
# 🧠 REGISTRY KERNEL CORE
# =========================

class OmegaRegistryKernelV6:

    def __init__(self):
        self.state = self.load_state()
        self.lock = threading.Lock()

        self.init_core_schema()
        print("\n🧠 OMEGA CONTROL PLANE v6 REGISTRY KERNEL ONLINE\n")

    # -------------------------
    # STATE + SCHEMA SAFETY
    # -------------------------

    def load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    data = json.load(f)
                    return data
            except:
                pass

        return {
            "services": {},
            "dead": {},
            "restarts": {},
            "health": "green",
            "tick": 0
        }

    def init_core_schema(self):
        for key in ["services", "dead", "restarts"]:
            if key not in self.state:
                self.state[key] = {}

    def save_state(self):
        with self.lock:
            with open(STATE_FILE, "w") as f:
                json.dump(self.state, f, indent=2)

    # -------------------------
    # SERVICE REGISTRY
    # -------------------------

    def register_service(self, name, cmd, role="service"):
        self.state["services"][name] = {
            "cmd": cmd,
            "role": role,
            "pid": None,
            "status": "stopped",
            "last_heartbeat": time.time()
        }

    # -------------------------
    # PROCESS CONTROL
    # -------------------------

    def launch(self, name):
        svc = self.state["services"][name]

        try:
            proc = subprocess.Popen(["python", svc["cmd"]])
            svc["pid"] = proc.pid
            svc["status"] = "running"
            svc["last_heartbeat"] = time.time()

            print(f"🚀 LAUNCH [{svc['role']}]: {name} PID={proc.pid}")

        except Exception as e:
            print(f"❌ LAUNCH FAIL: {name} -> {e}")

    def is_alive(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except:
            return False

    # -------------------------
    # HEARTBEAT + HEALTH
    # -------------------------

    def heartbeat(self, name):
        if name in self.state["services"]:
            self.state["services"][name]["last_heartbeat"] = time.time()

    def detect_dead(self):
        now = time.time()
        dead = []

        for name, svc in self.state["services"].items():
            pid = svc.get("pid")

            if pid and not self.is_alive(pid):
                dead.append(name)
                continue

            if now - svc["last_heartbeat"] > HEARTBEAT_TIMEOUT:
                dead.append(name)

        return dead

    # -------------------------
    # RESTART POLICY ENGINE
    # -------------------------

    def handle_dead(self, name):
        svc = self.state["services"][name]

        self.state["dead"][name] = self.state["dead"].get(name, 0) + 1

        if self.state["dead"][name] > MAX_RESTARTS:
            svc["status"] = "quarantined"
            print(f"🛑 QUARANTINED: {name}")
            return

        print(f"⚠️ RESTARTING: {name}")
        self.launch(name)

    # -------------------------
    # INIT BOOT SEQUENCE
    # -------------------------

    def boot(self):

        # CORE 25-MODULE SYSTEM BOOTSTRAP
        bootstrap_services = [
            ("run_omega_v5.py", "task"),
            ("omega_orchestrator_v5.py", "service"),
            ("omega_identity_kernel_v25.py", "kernel"),
            ("omega_execution_engine_v7.py", "engine"),
            ("omega_meta_brain_v10.py", "brain"),
            ("omega_unified_kernel_v15.py", "kernel"),
            ("omega_swarm_memory_bridge_v9.py", "swarm"),
            ("omega_mesh_superintelligence_v12.py", "mesh"),
            ("omega_process_supervisor_v2.py", "service"),
            ("omega_os_runtime_v1.py", "runtime"),
            ("omega_decision_engine_v5.py", "service"),
            ("omega_data_stream_v5.py", "service"),
            ("omega_event_mesh_v5.py", "daemon"),
            ("omega_brain_node_v5.py", "daemon"),
            ("omega_learning_engine_v11.py", "service"),
            ("omega_learning_convergence_v12.py", "service"),
            ("omega_global_memory_cloud_v9.py", "daemon"),
            ("omega_sensor_interface_v11.py", "daemon"),
            ("omega_swarm_evolver_v11.py", "daemon"),
            ("omega_economy_engine_v5.py", "service"),
            ("omega_adaptive_optimizer_v5.py", "service"),
            ("omega_identity_engine_v5.py", "service"),
            ("omega_cognitive_node_v6.py", "service"),
            ("omega_brain_factory_v11.py", "daemon"),
            ("omega_execution_engine_v7.py", "engine"),
        ]

        for cmd, role in bootstrap_services:
            self.register_service(cmd, cmd, role)

        for name in self.state["services"]:
            self.launch(name)

        self.save_state()

    # -------------------------
    # MAIN KERNEL LOOP
    # -------------------------

    def run(self):
        self.boot()

        while True:
            self.state["tick"] += 1

            dead = self.detect_dead()

            if dead:
                print(f"\n⚠️ DEAD SERVICES: {dead}")

            for d in dead:
                self.handle_dead(d)

            self.save_state()
            time.sleep(3)


# =========================
# BOOT ENTRYPOINT
# =========================

if __name__ == "__main__":
    kernel = OmegaRegistryKernelV6()
    kernel.run()
