import time

def safe_xadd(r, stream, data, maxlen=10000):
    """
    Production-safe XADD wrapper
    """

    try:
        # 🔒 HARD VALIDATION
        if not isinstance(data, dict) or not data:
            raise ValueError("XADD fields must be a non-empty dict")

        # 🔒 FORCE STRING VALUES (Redis requirement)
        safe_data = {str(k): str(v) for k, v in data.items()}

        # 🚀 ADD TO STREAM
        return r.xadd(stream, safe_data, maxlen=maxlen, approximate=True)

    except Exception as e:
        print("⚠️ SAFE_XADD ERROR:", e)
        time.sleep(0.2)
        return None
