sed -i '/if __name__ == "__main__"/d' omega_process_supervisor_v3.py

echo '
if __name__ == "__main__":
    print("[Ω] ENTRYPOINT ACTIVE")
    main()
' >> omega_process_supervisor_v3.py
