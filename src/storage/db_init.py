import sqlite3

conn = sqlite3.connect("data/valinx.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS metrics_raw (
    sample_id INTEGER PRIMARY KEY,
    ts_unix REAL,
    ts_readable TEXT,

    CPU_perc REAL,
    Mem_perc REAL,
    cpu_freq_MHz REAL,
    disk_read_MBps REAL,
    disk_write_MBps REAL,
    net_sent_MBps REAL,
    net_recv_MBps REAL,

    trigger_ctx TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS anomaly_scores (
    sample_id INTEGER,
    model TEXT,
    anomaly_label INTEGER,
    anomaly_score REAL,
    PRIMARY KEY (sample_id, model)
);
""")

cur.execute("CREATE INDEX IF NOT EXISTS idx_metrics_time ON metrics_raw(ts_unix);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_anomaly_label ON anomaly_scores(anomaly_label);")

conn.commit()
conn.close()

print("✅ Database initialized")
