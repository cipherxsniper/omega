import random

class SignalEngine:

    def generate_signal(self):
        signals = ["BUY", "SELL", "HOLD"]
        confidence = round(random.random(), 2)

        return {
            "signal": random.choice(signals),
            "confidence": confidence
        }
