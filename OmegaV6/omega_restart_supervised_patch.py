def restart(self, s):
    if hasattr(self.supervisor, "is_blacklisted") and self.supervisor.is_blacklisted(s):
        print(f"⛔ BLOCKED BY SUPERVISOR: {s}")
        return

    meta = self.processes.get(s)
    if not meta:
        return

    if meta["r"] > 2:
        print(f"❌ SUPERVISOR REGISTER DEAD: {s}")

        # register failure
        allowed = self.supervisor.register_dead(s)

        if not allowed:
            self.dead_services.add(s)
            return

        return

    print(f"🔁 Restarting: {s}")

    meta["p"].terminate()
    time.sleep(1)

    from omega_launch_guard import safe_launch
    meta["p"] = safe_launch(s)
    meta["r"] += 1
