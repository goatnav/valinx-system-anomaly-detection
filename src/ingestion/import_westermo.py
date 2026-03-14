import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

VALINX_COLS = [
    "sample_id",
    "Time-(numerical)",
    "Time-(readable)",
    "CPU_perc",
    "Mem_perc",
    "cpu_freq_MHz",
    "disk_read_MBps",
    "disk_write_MBps",
    "net_sent_MBps",
    "net_recv_MBps",
    "trigger_ctx",
]

def main(in_path: str, out_path: str):
    in_path = Path(in_path)
    out_path = Path(out_path)

    df = pd.read_csv(in_path)

    # Westermo: first column is timestamp in seconds since start. (Often named "timestamp".) :contentReference[oaicite:5]{index=5}
    ts_col = df.columns[0]
    ts_seconds = pd.to_numeric(df[ts_col], errors="coerce").fillna(0)

    # Build VALinX timestamps
    out = pd.DataFrame()
    out["sample_id"] = range(len(df))
    out["Time-(numerical)"] = ts_seconds.astype(float)

    # Make a readable time string (t+Xs)
    out["Time-(readable)"] = ts_seconds.apply(lambda s: f"t+{int(s)}s")

    # ---- CPU signal ----
    # Westermo has load-* metrics, plus cpu-user/system/iowait (rates). :contentReference[oaicite:6]{index=6}
    if "load-1m" in df.columns:
        out["CPU_perc"] = pd.to_numeric(df["load-1m"], errors="coerce")
    elif all(c in df.columns for c in ["cpu-user", "cpu-system", "cpu-iowait"]):
        # Not truly "percent", but a decent combined CPU activity signal.
        cpu = (
            pd.to_numeric(df["cpu-user"], errors="coerce").fillna(0)
            + pd.to_numeric(df["cpu-system"], errors="coerce").fillna(0)
            + pd.to_numeric(df["cpu-iowait"], errors="coerce").fillna(0)
        )
        out["CPU_perc"] = cpu
    else:
        out["CPU_perc"] = 0.0

    # ---- Memory percent ----
    # Westermo memory metrics are in bytes incl. sys-mem-available and sys-mem-total. :contentReference[oaicite:7]{index=7}
    if ("sys-mem-available" in df.columns) and ("sys-mem-total" in df.columns):
        avail = pd.to_numeric(df["sys-mem-available"], errors="coerce")
        total = pd.to_numeric(df["sys-mem-total"], errors="coerce")
        used = (total - avail).clip(lower=0)
        out["Mem_perc"] = (100.0 * used / total.replace(0, pd.NA)).fillna(0.0)
    else:
        out["Mem_perc"] = 0.0

    # ---- Disk IO ----
    # Westermo has disk-bytes-read and disk-bytes-written (rate of change). :contentReference[oaicite:8]{index=8}
    if "disk-bytes-read" in df.columns:
        out["disk_read_MBps"] = pd.to_numeric(df["disk-bytes-read"], errors="coerce").fillna(0) / 1e6
    else:
        out["disk_read_MBps"] = 0.0

    if "disk-bytes-written" in df.columns:
        out["disk_write_MBps"] = pd.to_numeric(df["disk-bytes-written"], errors="coerce").fillna(0) / 1e6
    else:
        out["disk_write_MBps"] = 0.0

    # Westermo dataset doesn’t include your trigger_ctx/process-cause field → leave blank.
    out["trigger_ctx"] = None

    # Not provided in Westermo → set placeholders.
    out["cpu_freq_MHz"] = None
    out["net_sent_MBps"] = 0.0
    out["net_recv_MBps"] = 0.0

    # Ensure column order matches your pipeline expectations
    out = out[VALINX_COLS]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)
    print(f"✅ Wrote VALinX-formatted CSV: {out_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="Path to a Westermo CSV")
    ap.add_argument("--out", dest="out", default="data/raw/system_metrics.csv", help="Output CSV path")
    args = ap.parse_args()
    main(args.inp, args.out)
