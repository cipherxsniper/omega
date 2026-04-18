
# -----------------------------
# BOOT STRAP
# -----------------------------
if __name__ == "__main__":
    print("[ML V12] Starting Omega ML Core...")

    ml = OmegaMLCoreV12()

    import random
    import time

    brain = "brain_00"

    while True:
        mem = [{"data": random.random()} for _ in range(5)]

        decision, features = ml.decide(brain, mem)
        reward = random.random()

        ml.reward(brain, reward)

        # FIXED LINE (match function signature)
        ml.train(brain, features, decision)

        print(f"[ML V12] {brain} → {decision} | reward={reward:.3f}")

        time.sleep(2)
