class PermissionEngine:
    def allow(self, query):
        blocked = ["rm -rf", "delete system", "self modify kernel"]
        return not any(b in query.lower() for b in blocked)
