import uuid
import time
import hashlib
import hmac

class SecureIdentityV85:
    def __init__(self, secret=None):
        self.secret = secret or uuid.uuid4().hex
        self.node_id = hashlib.sha256(self.secret.encode()).hexdigest()
        self.created = time.time()

    def sign(self, payload: dict):
        raw = str(sorted(payload.items())).encode()
        return hmac.new(
            self.secret.encode(),
            raw,
            hashlib.sha256
        ).hexdigest()

    def verify(self, payload: dict, signature: str, secret: str):
        expected = hmac.new(
            secret.encode(),
            str(sorted(payload.items())).encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected, signature)
