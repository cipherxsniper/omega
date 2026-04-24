from dkf_runtime import DKF

dkf = DKF()

print("""
🧠 DKF v13 SERVICE CONTROLLER ONLINE
⚡ Ollama Auto-Control | Memory Enabled
------------------------------------------------
""")

while True:
    try:
        q = input("DKF > ").strip()

        if q in ["exit", "quit"]:
            break

        out = dkf.chat(q)

        print("\n🧠", out, "\n")

    except KeyboardInterrupt:
        print("\n🧠 shutdown")
        break
