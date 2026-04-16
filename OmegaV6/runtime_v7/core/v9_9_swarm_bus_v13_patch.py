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
                "timestamp": event.get("timestamp", time.time())
            }

            if not hasattr(self, "event_queue"):
                from collections import deque
                self.event_queue = deque()

            self.event_queue.append(event)

        except Exception as e:
            print("[LISTEN ERROR]", e)


def processor_loop(self):
    while self.running:
        try:
            if not hasattr(self, "event_queue"):
                from collections import deque
                self.event_queue = deque()

            if self.event_queue:
                event = self.event_queue.popleft()

                self.event_count += 1

                # 🔥 FORCE MEMORY WRITE (CRDT SAFE)
                try:
                    self.memory.store(event)
                except Exception:
                    try:
                        self.memory.apply(event)
                    except Exception as e:
                        print("[MEMORY WRITE FAILED]", e)

                print(f"[V13 RECEIVED] {event}")

            time.sleep(0.01)

        except Exception as e:
            print("[PROCESS ERROR]", e)
