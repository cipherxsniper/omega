from omega_supervisor_v42 import supervisor
# OMEGA INTEGRATION BRIDGE v4.1 (v2 INTELLIGENT FEED ENGINE)
# Log → Structured System Intelligence + Narrative State Layer

import time
import re
from pathlib import Path
from collections import deque, Counter, defaultdict
from datetime import datetime
from omega_cat_patch_v41 import repair_action
from omega_repair_gate_v41 import approve_repair
OMEGA_ROOT = Path(__file__).resolve().parents[0]
LOG_DIR = OMEGA_ROOT / "logs"
OUT_FILE = LOG_DIR / "omega_brain_stream.log"

LOG_DIR.mkdir(exist_ok=True)


# =========================================================
# SYSTEM STATE MODEL (REAL ENGINEERING METRICS)
# =========================================================

class SystemState:
    def __init__(self):
        self.event_counts = Counter()
        self.error_counts = Counter()
        self.worker_status = defaultdict(lambda: "unknown")
        self.last_seen = {}
        self.stability = 1.0
        self.activity = 0.0
        self.failure_pressure = 0.0

    def update(self, event_type, line):
        self.event_counts[event_type] += 1
        self.last_seen[event_type] = time.time()

        if "error" in event_type or "missing" in event_type:
            self.error_counts[event_type] += 1

        self._recalculate()

    def _recalculate(self):
        total = sum(self.event_counts.values()) + 1
        errors = sum(self.error_counts.values())

        self.activity = min(1.0, total / 200)
        self.failure_pressure = min(1.0, errors / total)
        self.stability = max(0.0, 1.0 - self.failure_pressure)


# =========================================================
# EVENT CLASSIFIER
# =========================================================

class EventClassifier:

    def classify(self, line: str):

        if "ModuleNotFoundError" in line:
            return "dependency_failure"

        if "No module named" in line:
            return "missing_module"

        if "online" in line or "ONLINE" in line:
            return "node_online"

        if "heartbeat" in line:
            return "heartbeat"

        if "Duplicate" in line or "already_active" in line:
            return "duplicate_block"

        if "restart" in line:
            return "restart_event"

        if "event backbone ONLINE" in line:
            return "bus_online"

        if "tick=" in line:
            return "runtime_tick"

        if "shutdown" in line:
            return "shutdown_event"

        return "raw"


# =========================================================
# GOAL INFERENCE ENGINE (BASED ON LOG BEHAVIOR)
# =========================================================

class GoalInference:

    def infer(self, state: SystemState):

        if state.failure_pressure > 0.3:
            return "stabilize_system"

        if state.activity > 0.7 and state.stability > 0.8:
            return "expand_throughput"

        if state.error_counts.get("dependency_failure", 0) > 3:
            return "repair_dependencies"

        return "maintain_balance"


# =========================================================
# NATURAL LANGUAGE SYSTEM TRANSLATOR
# =========================================================

class NLTranslator:

    def translate(self, event_type, line, state: SystemState, goal: str):

        stability = state.stability
        pressure = state.failure_pressure

        base = ""

        if event_type == "dependency_failure":
            base = "Critical dependency failure detected in system runtime"

        elif event_type == "missing_module":
            mod = re.findall(r"No module named '([^']+)'", line)
            base = f"Missing module detected: {mod[0] if mod else 'unknown'}"

        elif event_type == "node_online":
            base = "Node initialized and reporting healthy status"

        elif event_type == "heartbeat":
            base = "Worker heartbeat confirmed (node alive)"

        elif event_type == "duplicate_block":
            base = "Duplicate process blocked by safety layer"

        elif event_type == "restart_event":
            base = "System component restart triggered"

        elif event_type == "bus_online":
            base = "Event bus backbone operational"

        elif event_type == "runtime_tick":
            base = "Runtime cycle tick observed"

        elif event_type == "shutdown_event":
            base = "System shutdown signal detected"

        else:
            base = "Unclassified system signal observed"

        return (
            f"[Ω STATE FEED] {base} "
            f"| stability={stability:.2f} "
            f"| pressure={pressure:.2f} "
            f"| goal={goal}"
        )


# =========================================================
# BRAIN STREAM WRITER
# =========================================================

class BrainStreamWriter:

    def write(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        with open(OUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")


# =========================================================
# INTEGRATION BRIDGE CORE
# =========================================================

class OmegaIntegrationBridgeV41v2:

    def __init__(self):
        self.state = SystemState()
        self.classifier = EventClassifier()
        self.goal_engine = GoalInference()
        self.translator = NLTranslator()
        self.writer = BrainStreamWriter()
        self.buffer = deque(maxlen=3000)

    def scan_logs(self):

        while True:

            for log_file in LOG_DIR.glob("*.log"):

                try:
                    lines = log_file.read_text(errors="ignore").splitlines()

                    for line in lines[-40:]:

                        if line in self.buffer:
                            continue

                        self.buffer.append(line)

                        event_type = self.classifier.classify(line)

                        self.state.update(event_type, line)

                        goal = self.goal_engine.infer(self.state)

                        message = self.translator.translate(
                            event_type,
                            line,
                            self.state,
                            goal
                        )

                        print(message)
                        self.writer.write(message)

                except Exception as e:
                    err = f"[Ω ERROR] bridge failure: {e}"
                    print(err)
                    self.writer.write(err)

            time.sleep(1)


# =========================================================
# BOOT
# =========================================================

if __name__ == "__main__":
    print("[Ω NARRATOR] Integration Bridge v4.1 v2 ONLINE (INTELLIGENT FEED ACTIVE)")

    bridge = OmegaIntegrationBridgeV41v2()
    bridge.scan_logs()
