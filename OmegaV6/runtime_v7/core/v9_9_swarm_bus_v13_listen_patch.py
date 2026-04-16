def listen_loop(self):
    print("[SWARM BUS V13] LISTENING...\n")

    while self.running:
        try:
            data, addr = self.sock.recvfrom(65535)

            try:
                event = json.loads(data.decode("utf-8"))
            except Exception:
                print("[DROP] invalid json from", addr)
                continue

            # FORCE normalize safe structure
            event = {
                "type": event.get("type", "unknown"),
                "content": event.get("content", ""),
                "node_id": event.get("node_id", str(addr)),
                "timestamp": event.get("timestamp", __import__("time").time())
            }

            # 🚀 CRITICAL FIX: ENSURE MEMORY WRITE PATH EXISTS
            try:
                self.memory.store(event)
            except Exception:
                self.memory.apply(event)

            # optional queue push if you use processor loop
            if hasattr(self, "event_queue"):
                self.event_queue.append(event)

        except Exception as e:
            print("[LISTEN ERROR]", e)
