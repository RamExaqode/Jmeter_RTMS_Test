import psutil
import time
import csv
import GPUtil

csv_path = r"F:\PerfTesting\system_metrics.csv"

with open(csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "timestamp", "cpu_percent", "memory_percent", "disk_read",
        "disk_write", "net_sent", "net_recv", "gpu_percent", "gpu_memory_used", "gpu_memory_total"
    ])
    csvfile.flush()

    try:
        while True:
            timestamp = time.time()
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_io_counters()
            net = psutil.net_io_counters()

            # Get GPU info (first GPU only, can extend for multiple)
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                gpu_percent = gpu.load * 100
                gpu_mem_used = gpu.memoryUsed
                gpu_mem_total = gpu.memoryTotal
            else:
                gpu_percent = 0
                gpu_mem_used = 0
                gpu_mem_total = 0

            row = [
                timestamp,
                cpu,
                mem,
                disk.read_bytes,
                disk.write_bytes,
                net.bytes_sent,
                net.bytes_recv,
                gpu_percent,
                gpu_mem_used,
                gpu_mem_total
            ]

            writer.writerow(row)
            csvfile.flush()
            print(f"CPU={cpu}%, RAM={mem}%, GPU={gpu_percent}%")

    except KeyboardInterrupt:
        print("Monitoring stopped.")
