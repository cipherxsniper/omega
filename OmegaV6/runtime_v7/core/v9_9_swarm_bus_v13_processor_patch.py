def processor_loop(self):
    while self.running:
        try:
            if self.event_queue:
                event = self.event_queue.popleft()

                self.event_count += 1

                # 🔥 CRDT SAFE WRITE
                try:
                    self.memory.store(event)
                except Exception:
                    self.memory.apply(event)

                print(f"[V14 RECEIVED] {event}")

            __import__("time").sleep(0.01)

        except Exception as e:
            print("[PROCESS ERROR]", e)
