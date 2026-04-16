import json
import time

def safe_handle_rx(self, data):
    try:
        payload = json.loads(data.decode())

        node_id = payload.get("node_id")
        if not node_id:
            return

        # register peer
        self.registry.update(node_id)

        # optional debug
        print("[V7.5 RX]", payload)

    except Exception as e:
        print("[RX ERROR]", e)
