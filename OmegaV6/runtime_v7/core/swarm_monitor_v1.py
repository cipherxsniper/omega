def monitor():
    while True:
        for name, info in PROCESS_MAP.items():
            p = info["proc"]

            # only treat REAL crash as failure
            if p.poll() is not None:
                code = p.returncode

                print("\n" + "=" * 60)
                print(f"[CRASH REPORT] {name}")
                print(f"[EXIT CODE] {code}")
                print(f"[LOG FILE] {info['log']}")
                print("=" * 60 + "\n")

                # only restart if NOT clean shutdown
                if code != 0:
                    time.sleep(3)
                    restart_layer(name)
                else:
                    print(f"[INFO] {name} exited cleanly (ignored)")

        time.sleep(5)
