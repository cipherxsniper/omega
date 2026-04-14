# ============================================================
# OMEGA EXECUTION ENGINE v7
# CONTROLLED REAL-WORLD ACTION LAYER (SAFE + LOGGED + ADAPTIVE)
# ============================================================

import time
import os
import subprocess
import traceback


# ============================================================
# 🛡️ SAFETY GATEKEEPER
# ============================================================

class OmegaSafetyGate:
    def __init__(self):
        self.blocked_commands = [
            "rm -rf /",
            "shutdown",
            "reboot",
            ":(){ :|:& };:"
        ]

    def validate(self, action):
        command = action.get("command", "")

        for blocked in self.blocked_commands:
            if blocked in command:
                return False, "BLOCKED_RISKY_COMMAND"

        return True, "SAFE"


# ============================================================
# ⚙️ EXECUTION ADAPTERS
# ============================================================

class FileSystemAdapter:
    def execute(self, action):
        try:
            path = action.get("path")
            content = action.get("content", "")

            with open(path, "w") as f:
                f.write(content)

            return {"status": "success", "path": path}

        except Exception as e:
            return {"status": "error", "error": str(e)}


class APIAdapter:
    def execute(self, action):
        # Placeholder for real API calls (safe structure only)
        return {
            "status": "mock_api_response",
            "data": action.get("payload", {})
        }


class ShellAdapter:
    def execute(self, action):
        try:
            cmd = action.get("command")
            result = subprocess.getoutput(cmd)

            return {
                "status": "success",
                "output": result
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}


# ============================================================
# 🌐 EXECUTION ENGINE CORE
# ============================================================

class OmegaExecutionEngine:
    def __init__(self, mesh, state, memory, graph, learning):
        self.mesh = mesh
        self.state = state
        self.memory = memory
        self.graph = graph
        self.learning = learning

        self.safety = OmegaSafetyGate()

        self.adapters = {
            "file": FileSystemAdapter(),
            "api": APIAdapter(),
            "shell": ShellAdapter()
        }

        self._bind()

    # --------------------------------------------------------
    # EVENT BINDING
    # --------------------------------------------------------

    def _bind(self):
        self.mesh.subscribe("execution_request", self.on_execution_request)

    # --------------------------------------------------------
    # EXECUTION ENTRY POINT
    # --------------------------------------------------------

    def on_execution_request(self, event):
        action = event.get("data", {})
        source = event.get("source", "unknown")

        # 1. SAFETY CHECK
        safe, reason = self.safety.validate(action)

        if not safe:
            self.mesh.publish(
                "execution_blocked",
                data={"action": action, "reason": reason},
                source="execution_engine"
            )

            self.memory.add_knowledge({
                "type": "blocked_execution",
                "reason": reason,
                "source": source
            })

            return

        # 2. SELECT ADAPTER
        action_type = action.get("type", "api")
        adapter = self.adapters.get(action_type)

        if not adapter:
            return

        # 3. EXECUTE
        result = adapter.execute(action)

        # 4. STORE OUTCOME
        self.memory.add_knowledge({
            "type": "execution_result",
            "action": action,
            "result": result
        })

        self.state.log_event({
            "type": "execution",
            "action": action,
            "result": result,
            "timestamp": time.time()
        })

        # 5. KNOWLEDGE GRAPH UPDATE
        self.graph.link(source, "external_world", "execution")

        # 6. BROADCAST RESULT
        self.mesh.publish(
            "execution_result",
            data=result,
            source="execution_engine"
        )

        # 7. LEARNING FEEDBACK
        if result.get("status") == "success":
            self.learning.record_success("execution_engine")
        else:
            self.learning.record_failure("execution_engine", result)
