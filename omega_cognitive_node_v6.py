# ============================================================
# OMEGA COGNITIVE NODE v6
# UNIFIED BRAIN + OBSERVER + LEARNING NODE
# ============================================================

import time
import traceback


# ============================================================
# 🧠 COGNITIVE NODE (UNIFIED BRAIN MODEL)
# ============================================================

class OmegaCognitiveNode:
    def __init__(self, name, mesh, state, memory, graph, learning):
        self.name = name
        self.mesh = mesh
        self.state = state
        self.memory = memory
        self.graph = graph
        self.learning = learning

        self.active = False
        self.thought_count = 0

        self._bind()

    # --------------------------------------------------------
    # EVENT SUBSCRIPTIONS
    # --------------------------------------------------------

    def _bind(self):
        self.mesh.subscribe("system_start", self.on_system_start)
        self.mesh.subscribe("brain_thought", self.on_brain_thought)
        self.mesh.subscribe("system_decision", self.on_system_decision)
        self.mesh.subscribe("system_error", self.on_error)
        self.mesh.subscribe("system_adaptation", self.on_adaptation)
        self.mesh.subscribe("data_stream", self.on_data)

    # --------------------------------------------------------
    # CORE OBSERVER BEHAVIOR
    # --------------------------------------------------------

    def observe(self, payload):
        """
        Cognitive observation layer:
        interprets incoming data into memory
        """

        self.memory.add_knowledge({
            "type": "observation",
            "brain": self.name,
            "data": payload
        })

    # --------------------------------------------------------
    # THINKING PROCESS (LOCAL INTELLIGENCE)
    # --------------------------------------------------------

    def think(self):
        return {
            "idea": f"{self.name} pattern analysis cycle {self.thought_count}",
            "confidence": 0.5 + (self.thought_count % 5) * 0.05
        }

    # --------------------------------------------------------
    # EVENT HANDLERS
    # --------------------------------------------------------

    def on_system_start(self, event):
        pass

    def on_brain_thought(self, event):
        if event.get("source") != self.name:
            self.observe(event)

    def on_system_decision(self, event):
        self.observe(event)

    def on_data(self, event):
        self.observe(event)

    def on_adaptation(self, event):
        self.observe(event)

    def on_error(self, event):
        self.learning.record_failure(self.name, str(event))

    # --------------------------------------------------------
    # OUTPUT BROADCAST
    # --------------------------------------------------------

    def broadcast(self, thought):
        self.mesh.publish(
            "brain_thought",
            data=thought,
            source=self.name
        )

    # --------------------------------------------------------
    # EXECUTION LOOP
    # --------------------------------------------------------

    def run(self):
        self.active = True

        while self.active:
            try:
                thought = self.think()
                self.broadcast(thought)

                self.thought_count += 1
                time.sleep(1)

            except Exception as e:
                self.learning.record_failure(self.name, str(e))
                self.mesh.publish("system_error", str(e), source=self.name)
                traceback.print_exc()

    def stop(self):
        self.active = False
