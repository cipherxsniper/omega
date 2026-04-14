# ============================================================
# OMEGA SWARM NODE v8
# WRAPS EXISTING OMEGA SYSTEM INTO DISTRIBUTED NODE
# ============================================================

class OmegaSwarmNode:
    def __init__(self, node_id, mesh, orchestrator):
        self.node_id = node_id
        self.mesh = mesh
        self.orchestrator = orchestrator

        self._register()

    # --------------------------------------------------------
    # REGISTER INTO SWARM
    # --------------------------------------------------------

    def _register(self):
        self.mesh.register_node(self.node_id, self)

    # --------------------------------------------------------
    # RECEIVE SWARM EVENTS
    # --------------------------------------------------------

    def receive_swarm_event(self, event):
        # route into local EventMesh if exists
        if hasattr(self.orchestrator, "mesh"):
            self.orchestrator.mesh.publish(
                event["type"],
                event["data"],
                source=f"swarm_{self.node_id}"
            )

    # --------------------------------------------------------
    # LOCAL TO SWARM PROPAGATION
    # --------------------------------------------------------

    def emit(self, event_type, data):
        self.mesh.publish(event_type, data, source=self.node_id)
