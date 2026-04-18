import time

def acquire_lock(r, key, node_id, ttl=5):
    return r.set(key, node_id, nx=True, ex=ttl)

def renew_lock(r, key, node_id, ttl=5):
    if r.get(key) == node_id:
        r.expire(key, ttl)
        return True
    return False
