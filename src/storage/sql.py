import pandas as pd
import sqlite3

DB_PATH = "data/valinx.db"

METRICS_COLS = [
    "sample_id", "ts_unix", "ts_readable",
    "CPU_perc", "Mem_perc", "cpu_freq_MHz",
    "disk_read_MBps", "disk_write_MBps",
    "net_sent_MBps", "net_recv_MBps",
    "trigger_ctx"
]

def insert_raw_metrics(csv_path="data/raw/system_metrics.csv"):
    df = pd.read_csv(csv_path)

    df = df.rename(columns={
        "Time-(numerical)": "ts_unix",
        "Time-(readable)": "ts_readable"
    })

    if "sample_id" not in df.columns:
        # fallback only (should exist from log_metrics)
        df.insert(0, "sample_id", range(len(df)))

    # Keep only columns that exist in table schema
    df = df[[c for c in METRICS_COLS if c in df.columns]]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    placeholders = ",".join(["?"] * len(df.columns))
    cols_sql = ",".join(df.columns)

    # INSERT OR IGNORE prevents duplicate sample_id crashes if you import same CSV twice
    cur.executemany(
        f"INSERT OR IGNORE INTO metrics_raw ({cols_sql}) VALUES ({placeholders})",
        df.itertuples(index=False, name=None)
    )

    conn.commit()
    conn.close()
    print("✅ Raw metrics stored")

def insert_anomaly_scores(df, overwrite_model=True):
    """
    df must have: sample_id, model, anomaly_label, anomaly_score
    overwrite_model=True will replace prior scores for that model.
    """
    required = {"sample_id", "model", "anomaly_label", "anomaly_score"}
    if not required.issubset(df.columns):
        raise ValueError(f"insert_anomaly_scores missing columns: {required - set(df.columns)}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if overwrite_model:
        models = sorted(set(df["model"].tolist()))
        for m in models:
            cur.execute("DELETE FROM anomaly_scores WHERE model = ?", (m,))

    cur.executemany(
        "INSERT OR REPLACE INTO anomaly_scores (sample_id, model, anomaly_label, anomaly_score) VALUES (?,?,?,?)",
        df[["sample_id", "model", "anomaly_label", "anomaly_score"]].itertuples(index=False, name=None)
    )

    conn.commit()
    conn.close()
    print("✅ Anomaly scores inserted")

if __name__ == "__main__":
    insert_raw_metrics()
