import json
import time

def secure_broadcast(self):
    while self.running:
        try:
            payload = self.identity.get_payload()
            sig = self.handshake.sign_payload(payload)

            packet = {
                "payload": payload,
                "sig": sig
            }

            data = json.dumps(packet).encode()

            # ONLY trusted/local targets
            targets = ["127.0.0.1"]

            for ip in targets:
                self.sock.sendto(data, (ip, self.broadcast_port))

            print({
                "node": payload["node_id"][:12],
                "peers": len(self.registry.snapshot())
            })

        except Exception as e:
            print("[BROADCAST ERROR]", e)

        time.sleep(2)


def secure_receive(self, data):
    try:
        packet = json.loads(data.decode())
        payload = packet["payload"]
        sig = packet["sig"]

        node_id = payload["node_id"]

        if self.handshake.verify(payload, sig):
            self.registry.register(node_id, sig)
            self.registry.heartbeat(node_id)

            print("[V7.5 RX VERIFIED]", node_id[:12])
        else:
            print("[V7.5 RX REJECTED] invalid signature")

    except Exception as e:
        print("[RX ERROR]", e)
