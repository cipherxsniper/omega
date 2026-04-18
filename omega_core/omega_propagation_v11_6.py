# 🧠 Omega v11.6 Propagation Controller (SELF-REACTIVE)

from omega_core.omega_field_engine_v11_6 import FieldEngine

class PropagationSystem:

    def __init__(self):
        self.field = FieldEngine()

    def trigger_cycle(self):

        heat = self.field.get_heatmap()

        # 🔁 SELF-MODULATING EMISSION
        attention_energy = 0.5 + heat.get("node_goal", 0) * 0.9
        self.field.emit("node_attention", attention_energy)

        # 🔥 CROSS-NODE FEEDBACK LOOP
        if heat.get("node_attention", 0) > 0.35:
            self.field.emit("node_goal", 0.65)

        if heat.get("node_goal", 0) > 0.25:
            self.field.emit("node_memory", 0.55)

        if heat.get("node_memory", 0) > 0.2:
            self.field.emit("node_stability", 0.45)

        # decay = system time evolution
        self.field.decay()

        return self.field.get_heatmap()

from omega_flow_engine_v11_7 import FlowEngine

self.flow = FlowEngine()

def cycle(self):

    # 1. compute flow
    flow_updates = self.flow.propagate(self.field.state)

    # 2. apply propagation
    self.field.apply_flow(flow_updates)

    # 3. stabilize system
    self.field.decay()
    self.field.equilibrium_pressure()

    return flow_updates
