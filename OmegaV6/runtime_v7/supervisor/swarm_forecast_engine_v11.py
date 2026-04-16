import json
import time
import os
from collections import defaultdict, Counter

MEMORY_FILE = "runtime_v7/supervisor/cognitive_memory_graph.json"
FORECAST_FILE = "runtime_v7/supervisor/forecast_memory_v11.json"

os.makedirs("runtime_v7/supervisor", exist_ok=True)


# =========================================================
# LOAD MEMORY
# =========================================================

def load_memory():
    if os.path.exists(MEMORY_FILE):
        return json.load(open(MEMORY_FILE))
    return {"events": []}


def save_forecast(data):
    json.dump(data, open(FORECAST_FILE, "w"), indent=2)


# =========================================================
# 🧠 V11 FORECAST ENGINE
# =========================================================

class ForecastEngineV11:

    def __init__(self):
        # chain counts: (A, B) -> C
        self.chain_map = defaultdict(Counter)

    # -----------------------------
    # BUILD TRANSITION MODEL
    # -----------------------------
    def build_model(self, events):
        types = [e.get("type") for e in events if "type" in e]

        for i in range(len(types) - 2):
            a, b, c = types[i], types[i+1], types[i+2]
            self.chain_map[(a, b)][c] += 1

    # -----------------------------
    # PREDICT NEXT EVENT
    # -----------------------------
    def predict_next(self, a, b):
        options = self.chain_map.get((a, b), None)

        if not options:
            return {"prediction": None, "confidence": 0.0}

        total = sum(options.values())

        best = options.most_common(1)[0]
        prediction = best[0]
        confidence = best[1] / total

        return {
            "prediction": prediction,
            "confidence": round(confidence, 3)
        }

    # -----------------------------
    # FORECAST FULL SYSTEM STATE
    # -----------------------------
    def forecast(self, events):

        self.build_model(events)

        types = [e.get("type") for e in events if "type" in e]

        if len(types) < 2:
            return {}

        a, b = types[-2], types[-1]

        prediction = self.predict_next(a, b)

        return {
            "last_sequence": [a, b],
            "prediction": prediction,
            "model_size": len(self.chain_map)
        }


# =========================================================
# LOOP
# =========================================================

def run():
    engine = ForecastEngineV11()

    while True:
        mem = load_memory()

        forecast = engine.forecast(mem.get("events", []))

        save_forecast(forecast)

        print(
            "[V11 FORECAST] "
            f"state={forecast.get('last_sequence')} "
            f"prediction={forecast.get('prediction')}"
        )

        time.sleep(5)


# =========================================================
# BOOT
# =========================================================

if __name__ == "__main__":
    print("🔮 V11 PREDICTIVE FORECAST ENGINE ONLINE")
    run()
