def broadcast(self):
    while self.running:
        try:
            import json, time

            payload = self.identity.get_payload()
            data = json.dumps(payload).encode()

            targets = ["127.0.0.1"]

            for ip in targets:
                self.sock.sendto(data, (ip, self.broadcast_port))

            # FORCE SELF PEER REGISTRATION (TERMUX MESH FIX)
            self.peers[self.identity.node_id] = time.time()

        except Exception as e:
            print("[BROADCAST ERROR]", e)

        time.sleep(3)
