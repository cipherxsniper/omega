# ============================================================
# OMEGA BRAIN NODE v5 — UNIFIED BASE CLASS (FIXED)
# ============================================================

class OmegaBrainNode:

    def __init__(self, mesh, memory, learning_engine):
        self.mesh = mesh
        self.memory = memory
        self.learning_engine = learning_engine

        self.id = self.__class__.__name__
        self.state = {}

    # --------------------------------------------------------
    # RECEIVE DATA FROM SWARM
    # --------------------------------------------------------

    def receive(self, event_type, data):
        self.state[event_type] = data

        # learn from every event
        if self.learning_engine:
            self.learning_engine.ingest({
                "brain": self.id,
                "event": event_type,
                "data": data
            })

    # --------------------------------------------------------
    # BASIC THINKING LOOP
    # --------------------------------------------------------

    def think(self):
        return {
            "brain": self.id,
            "state_size": len(self.state)
        }

    # --------------------------------------------------------
    # BROADCAST TO MESH
    # --------------------------------------------------------

    def broadcast(self, event_type, data):
        if self.mesh:
            self.mesh.publish(event_type, data, source=self.id)
