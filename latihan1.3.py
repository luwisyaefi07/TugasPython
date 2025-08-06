logs = ["ERROR: Disk Full on ServerA", "INFO: User login success", "WARNING: High CPU on ServerB", "ERROR: Database connection lost"]

for log in logs:
    if log.startswith("ERROR"):
        # Pisahkan string berdasarkan ':'
        pisah = log.split(":", 1)  # hanya split sekali, agar pesan tidak terpotong lebih dari 1 bagian
        error_detail = pisah[1].split()  # ambil bagian setelah 'ERROR:' dan hilangkan spasi
        print(f"ERROR : {error_detail}")