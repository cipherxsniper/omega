import os
from obs.logger import log_event

OMEGA_ROOT = os.path.expanduser("~/Omega")

def scan_omega():
    files = []

    for root, dirs, filenames in os.walk(OMEGA_ROOT):
        for f in filenames:
            path = os.path.join(root, f)
            try:
                size = os.path.getsize(path)
                files.append({
                    "path": path,
                    "size": size
                })
            except:
                continue

    log_event("omega_scan", {
        "file_count": len(files),
        "total_size_bytes": sum(f["size"] for f in files)
    })

    return files
