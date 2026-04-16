import random


class EnvironmentSensor:

    def read(self):
        # SAFE SIMULATION LAYER (replace with real IoT APIs later)
        return {
            "temperature": 20 + random.random() * 10,
            "motion": random.choice([0, 1]),
            "light": random.random(),
            "sound": random.random()
        }
