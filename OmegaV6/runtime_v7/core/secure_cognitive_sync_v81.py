import time
import json
import hashlib
import base64

class SecureCognitiveSyncV81:
    def __init__(self, node_id):
        self.node_id = node_id
        self.secret = hashlib.sha256(node_id.encode()).digest()

    def encrypt(self, payload: dict):
        raw = json.dumps(payload).encode()
        encoded = base64.b64encode(raw)

        signature = hashlib.sha256(encoded + self.secret).hexdigest()

        return {
            "data": encoded.decode(),
            "sig": signature,
            "node_id": self.node_id,
            "ts": time.time()
        }

    def verify(self, packet: dict):
        try:
            encoded = packet["data"].encode()
            sig = packet["sig"]

            expected = hashlib.sha256(encoded + self.secret).hexdigest()
            return sig == expected
        except:
            return False

    def decrypt(self, packet: dict):
        if not self.verify(packet):
            return None

        raw = base64.b64decode(packet["data"].encode())
        return json.loads(raw.decode())
