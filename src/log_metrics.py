import psutil, time, pandas as pd, os
from datetime import datetime

cpuThreshold = 80  # Thresholds capture obvious anomalies
memThreshold = 85

rows = []
prev_disk = psutil.disk_io_counters()
prev_net = psutil.net_io_counters()

# interval = 1
minutes = 60  # 60 seconds in a minute
hours = 60 * 60  # (60*60) seconds in an hour

# 🔹 Create unique timestamped filenames
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
base_dir = "data/raw"
os.makedirs(base_dir, exist_ok=True)
filename_long = os.path.join(base_dir, f"system_metrics_long_{timestamp_str}.csv")
filename_short = os.path.join(base_dir, f"system_metrics_{timestamp_str}.csv")

try:
    for _ in range( hours):  # runs for 4 hours
        time.sleep(1)  # wait one second
        T = time.time()

        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        freq = getattr(psutil.cpu_freq(), "current", None)

        curr_disk = psutil.disk_io_counters()
        curr_net = psutil.net_io_counters()

        # Compute deltas (convert bytes to MB)
        disk_write_MBps = (curr_disk.write_bytes - prev_disk.write_bytes) / 1e6
        disk_read_MBps = (curr_disk.read_bytes - prev_disk.read_bytes) / 1e6
        net_sent_MBps = (curr_net.bytes_sent - prev_net.bytes_sent) / 1e6
        net_recv_MBps = (curr_net.bytes_recv - prev_net.bytes_recv) / 1e6

        prev_disk, prev_net = curr_disk, curr_net  # update previous readings

        # If memory/cpu meets threshold, capture why
        cause = None
        if (cpu is not None and cpu >= cpuThreshold) or (mem is not None and mem >= memThreshold):
            procs = sorted(
                psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                key=lambda p: (p.info.get('cpu_percent') or 0.0),
                reverse=True
            )[:3]

            cause = "; ".join(
                f"{p.info.get('name', '?')} cpu={p.info.get('cpu_percent', 0):.1f}% "
                f"mem={p.info.get('memory_percent', 0):.1f}% (pid={p.info.get('pid')})"
                for p in procs
            )

        rows.append({
            "Time-(numerical)": T,
            "Time-(readable)": datetime.fromtimestamp(T).isoformat(timespec="seconds"),
            "CPU_perc": cpu,
            "Mem_perc": mem,
            "cpu_freq_MHz": None if freq is None else round(freq, 1),
            "disk_read_MBps": round(disk_read_MBps, 3),
            "disk_write_MBps": round(disk_write_MBps, 3),
            "net_sent_MBps": round(net_sent_MBps, 3),
            "net_recv_MBps": round(net_recv_MBps, 3),
            "trigger_ctx": cause
        })

        if _ % 300 == 0:  # every 5 minutes
            pd.DataFrame(rows).to_csv(filename_long, index=False)
            print(f"💾 Autosaved at {time.ctime(T)}")

except KeyboardInterrupt:
    print("Stopped manually!")

finally:
    pd.DataFrame(rows).to_csv("data/raw/system_metrics.csv", index=False)
    print(f"✅ Saved collected data safely to {filename_long}")

print("Finished!")
pd.DataFrame(rows).to_csv(filename_short, index=False)
print(f"✅ Short summary saved to {filename_short}")
