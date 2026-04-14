import subprocess
import json


class OmegaV20Bridge:

    def run(self):
        print("[Ω-BRIDGE] v20 → Mesh bridge ONLINE")

        process = subprocess.Popen(
            ["python", "omega_recursive_improvement_v20.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            try:
                event = json.loads(line.strip())

                if event.get("type") == "v20_meta":

                    mesh_event = {
                        "event_type": "cognitive_update",
                        "source": "v20_core",
                        "strategy": event["data"]["strategy"],
                        "ideas": event["data"]["state"]["ideas"],
                        "strength": event["data"]["state"]["strength"],
                        "timestamp": event["timestamp"]
                    }

                    print("[Ω-MESH INJECT]", json.dumps(mesh_event))

            except Exception:
                continue


if __name__ == "__main__":
    OmegaV20Bridge().run()
