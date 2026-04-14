import os
import json
import time
import random
import fcntl

STATE_FILE = "omega_reflection_v21.json"
HUMAN_LOG = "omega_reflection_readable.log"


# -----------------------------
# STATE ENGINE
# -----------------------------

class ReflectionState:
    def __init__(self):
        if not os.path.exists(STATE_FILE):
            self._init()

    def _init(self):
        data = {
            "step": 0,
            "brains": ["brain_0", "brain_1", "brain_2", "brain_3"],
            "scores": {b: 1.0 for b in ["brain_0", "brain_1", "brain_2", "brain_3"]},
            "identity": {},
            "history": []
        }
        self.write(data)

    def lock(self, f):
        fcntl.flock(f, fcntl.LOCK_EX)

    def unlock(self, f):
        fcntl.flock(f, fcntl.LOCK_UN)

    def read(self):
        with open(STATE_FILE, "r") as f:
            self.lock(f)
            data = json.load(f)
            self.unlock(f)
        return data

    def write(self, data):
        with open(STATE_FILE, "r+") as f:
            self.lock(f)
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            self.unlock(f)


# -----------------------------
# SELF-REFLECTION ENGINE
# -----------------------------

class OmegaSelfReflectionV21:
    def __init__(self):
        self.state = ReflectionState()

    # -------------------------
    # CORE EVOLUTION STEP
    # -------------------------

    def evolve(self, scores):
        new_scores = {}

        for b, v in scores.items():
            noise = random.random() * 0.03

            # simple drift dynamics
            new_scores[b] = max(1e-9, v * (0.92 + noise))

        total = sum(new_scores.values())
        return {k: v / total for k, v in new_scores.items()}

    # -------------------------
    # OBSERVER TRANSLATION LAYER
    # -------------------------

    def interpret(self, state):
        scores = state["scores"]

        top = max(scores, key=scores.get)
        avg = sum(scores.values()) / len(scores)

        dominant_strength = scores[top]

        # convert numeric state → semantic description
        if dominant_strength > 0.30:
            dominance = "strong convergence toward a single dominant subsystem"
        elif dominant_strength > 0.26:
            dominance = "moderate convergence with emerging preference structure"
        else:
            dominance = "distributed balance across subsystems"

        stability = "stable" if max(scores.values()) - min(scores.values()) < 0.05 else "unstable"

        return {
            "top": top,
            "dominance": dominance,
            "stability": stability,
            "avg_signal": avg
        }

    # -------------------------
    # NATURAL LANGUAGE GENERATOR
    # -------------------------

    def to_english(self, reflection, step):
        return (
            f"[OMEGA SELF-OBSERVATION]\n"
            f"Step {step}: The system is currently observing its internal state.\n"
            f"Primary active subsystem: {reflection['top']}.\n"
            f"Interpretation: {reflection['dominance']}.\n"
            f"System stability assessment: {reflection['stability']}.\n"
            f"Average signal strength across modules: {reflection['avg_signal']:.4f}.\n"
            f"The system is not conscious, but it is generating structured self-representation from numerical dynamics.\n"
        )

    # -------------------------
    # LOGGING
    # -------------------------

    def log(self, text):
        with open(HUMAN_LOG, "a") as f:
            f.write(text + "\n" + "-" * 60 + "\n")

    # -------------------------
    # MAIN LOOP
    # -------------------------

    def run(self):
        print("[OMEGA v21] SELF-REFLECTION LAYER ONLINE")

        while True:
            try:
                state = self.state.read()

                state["step"] += 1

                # evolve numeric system
                state["scores"] = self.evolve(state["scores"])

                # interpret state into meaning
                reflection = self.interpret(state)

                # update identity field
                state["identity"] = reflection

                # save machine state
                self.state.write(state)

                # generate human-readable layer
                report = self.to_english(reflection, state["step"])

                self.log(report)

                print(report)

                time.sleep(0.3)

            except Exception as e:
                print("[v21 ERROR]", e)
                time.sleep(1)


if __name__ == "__main__":
    OmegaSelfReflectionV21().run()


# OPTIMIZED BY v29 ENGINE
