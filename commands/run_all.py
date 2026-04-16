import os

def register():
    def run_all(parts):
        print("[Ω] launching swarm batch...")

        os.system("bash omega_launch_all.sh")

    return run_all
