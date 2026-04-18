    # -----------------------------
    # SAVE / LOAD
    # -----------------------------
    def save_model(self):
        data = {
            "w1": self.w1,
            "w2": self.w2,
            "b1": self.b1,
            "b2": self.b2,
            "brain_influence": dict(self.brain_influence)
        }

        with open(MODEL_FILE, "w") as f:
            json.dump(data, f)

    def load_model(self):
        if os.path.exists(MODEL_FILE):
            try:
                with open(MODEL_FILE, "r") as f:
                    data = json.load(f)

                self.w1 = data["w1"]
                self.w2 = data["w2"]
                self.b1 = data["b1"]
                self.b2 = data["b2"]
                self.brain_influence.update(data.get("brain_influence", {}))

                print("[ML V12] Loaded")
            except Exception as e:
                print("[ML V12] Load failed:", e)
