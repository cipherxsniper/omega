# ============================================================
# OMEGA SWARM MEMORY BRIDGE v9
# CONNECTS SWARM NODES TO GLOBAL MEMORY CLOUD
# ============================================================

class OmegaSwarmMemoryBridge:
    def __init__(self, node_id, cloud, mesh):
        self.node_id = node_id
        self.cloud = cloud
        self.mesh = mesh

        self._bind()

    # --------------------------------------------------------
    # LISTEN TO SWARM EVENTS
    # --------------------------------------------------------

    def _bind(self):
        self.mesh.subscribe("brain_thought", self.on_event)
        self.mesh.subscribe("system_decision", self.on_event)
        self.mesh.subscribe("execution_result", self.on_event)
        self.mesh.subscribe("data_stream", self.on_event)

    # --------------------------------------------------------
    # STORE EVERYTHING INTO GLOBAL MEMORY
    # --------------------------------------------------------

    def on_event(self, event):
        self.cloud.write_episode(
            node_id=self.node_id,
            event_type=event["type"],
            data=event["data"]
        )

    # --------------------------------------------------------
    # SYNC BACK INTO SWARM
    # --------------------------------------------------------

    def sync_insights(self):
        patterns = self.cloud.extract_patterns()

        self.mesh.publish(
            "global_memory_update",
            data=patterns,
            source=self.node_id
        )
