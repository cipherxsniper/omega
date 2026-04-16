# REPLACE ENTIRE restart METHOD

def restart(self, s):
    if s in self.dead_services:
        return

    meta = self.processes.get(s)
    if not meta:
        return

    if meta["r"] > 2:
        print(f"❌ PERMANENTLY DISABLED: {s}")
        self.dead_services.add(s)
        return

    print(f"🔁 Restarting: {s}")

    meta["p"].terminate()
    time.sleep(1)

    from omega_launch_guard import safe_launch
    meta["p"] = safe_launch(s)
    meta["r"] += 1
