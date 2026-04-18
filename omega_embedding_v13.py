import hashlib
import time

def embed(text):
    """
    Simulated embedding:
    converts raw event → numeric semantic vector
    """
    h = hashlib.sha256(text.encode()).hexdigest()

    vec = [
        int(h[i:i+4], 16) / 65535.0
        for i in range(0, 32, 4)
    ]

    return {
        "raw": text,
        "vector": vec,
        "timestamp": time.time()
    }
