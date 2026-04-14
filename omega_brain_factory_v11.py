# ============================================================
# OMEGA BRAIN FACTORY v11
# DYNAMIC COGNITIVE NODE GENERATION SYSTEM
# ============================================================

import uuid


class OmegaBrainFactory:
    def __init__(self, mesh, memory, learning):
        self.mesh = mesh
        self.memory = memory
        self.learning = learning
        self.created_brains = {}

    # --------------------------------------------------------
    # CREATE NEW BRAIN NODE
    # --------------------------------------------------------

    def spawn_brain(self, purpose="general_analysis"):
        brain_id = f"Brain_{uuid.uuid4().hex[:6]}"

        brain = {
            "id": brain_id,
            "purpose": purpose,
            "knowledge_bias": 0.5,
            "created_at": __import__("time").time(),
            "performance_score": 1.0
        }

        self.created_brains[brain_id] = brain

        self.memory.add_knowledge({
            "type": "brain_spawned",
            "brain": brain
        })

        self.mesh.publish(
            "brain_spawned",
            data=brain,
            source="brain_factory"
        )

        return brain
