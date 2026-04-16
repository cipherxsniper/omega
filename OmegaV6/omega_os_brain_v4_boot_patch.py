service_manifest, degraded, missing_core = self.normalize_services(
    manifest["service"],
    service_manifest
)

if missing_core:
    print("🛑 BOOT ABORTED: critical core missing")
    return

order = self.dag.resolve(service_manifest)
