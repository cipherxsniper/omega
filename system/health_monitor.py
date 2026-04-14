# system/health_monitor.py

import os

class HealthMonitor:
    def check(self):
        return {
            "status": "OK",
            "files": os.listdir("."),
        }
