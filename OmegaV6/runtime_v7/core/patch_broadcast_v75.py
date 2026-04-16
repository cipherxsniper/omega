import json
import time

def broadcast(self):
    while self.running:
        try:
            payload = self.identity.get_payload()
            data = json.dumps(payload).encode()

            # local + future LAN expansion
            targets = ["127.0.0.1"]

            for ip in targets:
                self.sock.sendto(data, (ip, self.broadcast_port))

            # FORCE SELF REGISTER
            self.registry.update(self.identity.node_id)

            print({
                "node": self.identity.node_id[:12],
                "peers": self.registry.count()
            })

        except Exception as e:
            print("[BROADCAST ERROR]", e)

        time.sleep(2)
