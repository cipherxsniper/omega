import json
import hashlib
import time

class SecureHandshakeV75:
    def create_challenge(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()

    def sign_payload(self, payload):
        raw = json.dumps(payload, sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()

    def verify(self, payload, signature):
        expected = self.sign_payload(payload)
        return expected == signature
