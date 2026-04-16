# ============================================================
# OMEGA SENSOR INTERFACE v11
# ENVIRONMENT + IoT ABSTRACTION LAYER
# ============================================================

import random
import time


class OmegaSensorInterface:
    def __init__(self, mesh):
        self.mesh = mesh

    # --------------------------------------------------------
    # SIMULATED ENVIRONMENT STREAM
    # --------------------------------------------------------

    def read_environment(self):
        return {
            "temperature": random.uniform(18, 40),
            "cpu_load": random.uniform(0, 100),
            "network_activity": random.uniform(0, 1),
            "motion_signal": random.choice([0, 1]),
            "timestamp": time.time()
        }

    # --------------------------------------------------------
    # PUSH INTO SWARM
    # --------------------------------------------------------

    def stream(self):
        data = self.read_environment()

        self.mesh.publish(
            "environment_signal",
            data=data,
            source="sensor_layer"
        )
