def is_leader(r, node_id):
    try:
        current = r.get("omega.leader")

        # 1. No leader → claim it
        if current is None:
            if r.set("omega.leader", node_id, nx=True, ex=3):
                return True

        # 2. I'm already leader → refresh heartbeat
        if current == node_id:
            r.expire("omega.leader", 3)
            return True

        # 3. Leader exists but check if it's stale
        ttl = r.ttl("omega.leader")
        if ttl == -1 or ttl == -2:
            # stale or broken key → force takeover
            if r.set("omega.leader", node_id, ex=3):
                return True

        return False

    except Exception as e:
        print("⚠️ leader error:", e)
        return False
