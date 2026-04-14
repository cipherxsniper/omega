import json
import os
import random
import math
from collections import defaultdict

MODEL_FILE = "omega_ml_core_v9_model.json"


class OmegaMLCoreV9:
    """
    Lightweight neural-style reinforcement learning core (v9).

    Upgrades from v8:
    - cleaner model versioning
    - improved feature stability
    - safer weight handling
    - swarm-compatible learning core
    """

    def __init__(self):
        # brain + feature weights
        self.weights = defaultdict(float)

        # learning rate
        self.lr = 0.05

        # load previous model if exists
        self.load_model()

    # -----------------------------
    # FEATURE ENCODING
    # -----------------------------
    def encode_features(self, features):
        """
        Convert raw inputs into stable numeric signals
        """
        encoded = []

        for f in features:
            try:
                encoded.append(float(f) / 100.0)
            except:
                encoded.append(random.random())

        return encoded

    # -----------------------------
    # DECISION ENGINE
    # -----------------------------
    def decide(self, brain, mem):
        """
        Returns: (decision, features)
        """

        features = []

        # extract memory signals
        for m in mem[-5:]:
            if isinstance(m, dict):
                features.append(len(str(m.get("data", ""))))
            else:
                features.append(len(str(m)))

        if not features:
            features = [random.random() * 100]

        features = self.encode_features(features)

        # compute score
        score = self.weights[brain]

        for f in features:
            score += self.weights[str(f)] * f

        if score > 0.5:
            return "optimize", features
        else:
            return "explore", features

    # -----------------------------
    # REWARD UPDATE (LEARNING)
    # -----------------------------
    def reward(self, brain, reward_value):
        """
        Reinforcement update for brain identity
        """

        current = self.weights[brain]

        error = reward_value - current

        self.weights[brain] += self.lr * error

    # -----------------------------
    # TRAIN FEATURE LINKS
    # -----------------------------
    def train(self, features, decision):
        """
        Train feature associations
        """

        target = 1.0 if decision == "optimize" else 0.0

        for f in features:
            key = str(f)

            prediction = self.weights[key]
            error = target - prediction

            self.weights[key] += self.lr * error * 0.1

    # -----------------------------
    # SAVE MODEL
    # -----------------------------
    def save_model(self):
        try:
            with open(MODEL_FILE, "w") as f:
                json.dump(dict(self.weights), f, indent=2)
        except Exception as e:
            print(f"[ML V9] Save error: {e}")

    # -----------------------------
    # LOAD MODEL
    # -----------------------------
    def load_model(self):
        if os.path.exists(MODEL_FILE):
            try:
                with open(MODEL_FILE, "r") as f:
                    data = json.load(f)

                for k, v in data.items():
                    self.weights[k] = v

                print("[ML V9] Model loaded")
            except:
                print("[ML V9] Failed to load model — starting fresh")
        else:
            print("[ML V9] No existing model — starting fresh")
