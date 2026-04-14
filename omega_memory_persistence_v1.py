import json
import os

class OmegaMemoryField:
    def __init__(self, path="omega_memory.json"):
        self.path = path
        self.state = self.load()

    def load(self):
        default_state = {
            "tick": 0,
            "history": [],
            "entropy_trace": [],
            "idea_evolution": {}
        }

        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    loaded = json.load(f)

                # SAFE MERGE (schema repair)
                for k, v in default_state.items():
                    if k not in loaded:
                        loaded[k] = v

                return loaded

            except Exception:
                print("[Ω-MEM] Corrupted memory file. Resetting.")
                return default_state

        return default_state

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)

    def step(self, ideas, agents, entropy_delta):
        self.state["tick"] = self.state.get("tick", 0) + 1

        self.state["history"].append({
            "ideas": len(ideas),
            "agents": len(agents),
            "entropy_delta": entropy_delta
        })

        self.state["entropy_trace"].append(entropy_delta)

        drift = sum(self.state["entropy_trace"][-50:]) / max(len(self.state["entropy_trace"][-50:]), 1)

        self.state["idea_evolution"]["drift"] = drift

        self.save()

        return self.state
