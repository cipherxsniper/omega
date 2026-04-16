sed -i '160,170c\
def heartbeat():\
    while True:\
        print("[OMEGA HEARTBEAT] " + datetime.utcnow().isoformat())\
        time.sleep(10)\
' omega_process_supervisor_v3.py
