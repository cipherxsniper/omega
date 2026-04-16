# ============================================================
# OMEGA DATA STREAM ENGINE v5
# BIG DATA + REALTIME INGESTION + EVENT BROADCAST SYSTEM
# ============================================================

import time
import random
import traceback


# ============================================================
# 🌐 DATA STREAM ENGINE
# ============================================================

class OmegaDataStreamEngine:
    def __init__(self, mesh, memory, state, graph, learning):
        self.mesh = mesh
        self.memory = memory
        self.state = state
        self.graph = graph
        self.learning = learning

        self.running = False
        self.sources = []

    # --------------------------------------------------------
    # REGISTER DATA SOURCE
    # --------------------------------------------------------

    def register_source(self, name, generator_func):
        self.sources.append({
            "name": name,
            "generator": generator_func
        })

    # --------------------------------------------------------
    # PROCESS DATA EVENT
    # --------------------------------------------------------

    def process(self, source_name, data):
        event = {
            "source": source_name,
            "data": data,
            "timestamp": time.time()
        }

        # 1. STORE IN GLOBAL STATE
        self.state.log_event(event)

        # 2. BROADCAST TO EVENT MESH
        self.mesh.publish(
            "data_stream",
            data=event,
            source=source_name
        )

        # 3. MEMORY UPDATE
        self.memory.add_knowledge({
            "type": "data_ingestion",
            "source": source_name,
            "data": data
        })

        # 4. KNOWLEDGE GRAPH LINK
        self.graph.link(source_name, "omega_core", "ingested_data")

    # --------------------------------------------------------
    # STREAM LOOP
    # --------------------------------------------------------

    def start(self):
        self.running = True

        print("[DATA STREAM] Engine started")

        while self.running:
            try:
                for source in self.sources:
                    name = source["name"]
                    func = source["generator"]

                    data = func()
                    self.process(name, data)

                time.sleep(1.5)

            except Exception as e:
                self.learning.record_failure("data_stream", str(e))
                self.mesh.publish("system_error", str(e), source="data_stream")
                traceback.print_exc()

    def stop(self):
        self.running = False


# ============================================================
# 🧪 MOCK DATA SOURCES (REPLACE WITH REAL LATER)
# ============================================================

def market_data_feed():
    return {
        "symbol": "OMEGA_ASSET",
        "price": round(random.uniform(90, 110), 2),
        "volume": random.randint(1000, 5000)
    }


def system_metrics_feed():
    return {
        "cpu": random.randint(10, 90),
        "ram": random.randint(20, 95),
        "latency": random.randint(1, 200)
    }


def signal_noise_feed():
    return {
        "signal_strength": random.random(),
        "noise_level": random.random()
    }
