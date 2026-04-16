import time

class HandshakeV85:
    def __init__(self, identity, registry):
        self.identity = identity
        self.registry = registry

    def create_handshake(self):
        payload = {
            "node_id": self.identity.node_id,
            "timestamp": time.time()
        }

        signature = self.identity.sign(payload)

        return {
            "payload": payload,
            "signature": signature
        }

    def verify_handshake(self, handshake, peer_secret):
        payload = handshake["payload"]
        signature = handshake["signature"]

        valid = self.identity.verify(payload, signature, peer_secret)

        if valid:
            self.registry.validate_peer(payload["node_id"])

        return valid
