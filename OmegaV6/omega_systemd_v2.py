import time
import json
import subprocess
import os
import traceback
from collections import defaultdict

# ---------------------------
# STATES
# ---------------------------

STATE_ACTIVE = "ACTIVE"
STATE_FAILED = "FAILED"
STATE_DEGRADED = "DEGRADED"
STATE_BLOCKED = "BLOCKED"

LOG_FILE = "omega_journal.log"

# ---------------------------
# JOURNALD BUS
# ---------------------------

class JournalBus:
    def log(self, level, module, msg):
        line = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "level": level,
            "module": module,
            "msg": msg
        }
        print(f"[JOURNAL:{level}] {module} → {msg}")

        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(line) + "\n")

# ---------------------------
# CRASH FINGERPRINTING
# ---------------------------

class CrashAnalyzer:
    def fingerprint(self, error_text):
        if "ImportError" in error_text:
            return "IMPORT_FAILURE"
        if "SyntaxError" in error_text:
            return "SYNTAX_ERROR"
        if "MemoryError" in error_text:
            return "OOM"
        if "JSONDecodeError" in error_text:
            return "STATE_CORRUPTION"
        return "UNKNOWN_CRASH"

# ---------------------------
# FAKE CGROUPS (SIMULATION)
# ---------------------------

class ResourceLimiter:
    def apply(self, module):
        # simple simulated constraints
        return {
            "cpu": 0.5,
            "memory": 128
        }

# ---------------------------
# SYSTEMD-LIKE KERNEL
# ---------------------------

class OmegaSystemD2:
    def __init__(self, manifest):
        self.manifest = manifest
        self.services = manifest.get("services", [])
        self.graph = defaultdict(list)
        self.state = {}
        self.proc = {}
        self.restarts = defaultdict(int)

        self.journal = JournalBus()
        self.crash = CrashAnalyzer()
        self.limits = ResourceLimiter()

    # -----------------------
    # DEP GRAPH (simple linear fallback)
    # -----------------------
    def build_graph(self):
        for i in range(len(self.services) - 1):
            self.graph[self.services[i]].append(self.services[i + 1])

    # -----------------------
    # LAUNCH SERVICE
    # -----------------------
    def start(self, service):
        if self.state.get(service) == STATE_BLOCKED:
            self.journal.log("BLOCK", service, "Blocked by supervisor")
            return

        self.journal.log("INFO", service, "Starting service")

        try:
            limits = self.limits.apply(service)

            p = subprocess.Popen(
                ["python", service],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.proc[service] = p
            self.state[service] = STATE_ACTIVE

        except Exception as e:
            self.state[service] = STATE_FAILED
            self.journal.log("ERROR", service, str(e))

    # -----------------------
    # STOP SERVICE
    # -----------------------
    def stop(self, service):
        p = self.proc.get(service)
        if p:
            p.terminate()
            self.state[service] = STATE_FAILED

    # -----------------------
    # MONITOR LOOP
    # -----------------------
    def monitor(self):
        while True:
            time.sleep(2)

            for s, p in list(self.proc.items()):

                if p.poll() is not None:
                    err = p.stderr.read().decode() if p.stderr else ""

                    reason = self.crash.fingerprint(err)

                    self.journal.log("WARN", s, f"DEAD → {reason}")

                    self.state[s] = STATE_FAILED

                    self.restarts[s] += 1

                    if self.restarts[s] > 3:
                        self.state[s] = STATE_BLOCKED
                        self.journal.log("BLOCK", s, "Too many restarts")
                        continue

                    self.journal.log("INFO", s, "Restarting service")
                    self.start(s)

    # -----------------------
    # BOOT SEQUENCE
    # -----------------------
    def boot(self):
        self.journal.log("INFO", "SYSTEM", "BOOT START")

        self.build_graph()

        for s in self.services:
            self.start(s)

        self.journal.log("INFO", "SYSTEM", "BOOT COMPLETE")
        self.monitor()


# ---------------------------
# ENTRY
# ---------------------------

if __name__ == "__main__":
    manifest_path = "omega_manifest.json"

    if not os.path.exists(manifest_path):
        print("❌ Missing manifest")
        exit(1)

    manifest = json.load(open(manifest_path))

    kernel = OmegaSystemD2(manifest)
    kernel.boot()
