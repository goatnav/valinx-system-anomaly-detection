import sqlite3
import pandas as pd

DB_PATH = "data/valinx.db"

def get_worst_anomalies(limit=5):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT m.sample_id, m.ts_readable, m.CPU_perc, m.Mem_perc,
           a.anomaly_score, a.anomaly_label, m.trigger_ctx
    FROM metrics_raw m
    JOIN anomaly_scores a ON m.sample_id = a.sample_id
    WHERE a.model = 'isolation_forest'
    ORDER BY a.anomaly_score ASC
    LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

def get_anomalies_in_range(start_ts, end_ts):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT m.sample_id, m.ts_readable, m.CPU_perc, m.Mem_perc,
           m.disk_read_MBps, m.disk_write_MBps,
           m.net_sent_MBps, m.net_recv_MBps,
           a.anomaly_score, m.trigger_ctx
    FROM metrics_raw m
    JOIN anomaly_scores a ON m.sample_id = a.sample_id
    WHERE m.ts_numerical BETWEEN ? AND ?
    ORDER BY m.ts_numerical ASC
    """
    df = pd.read_sql_query(query, conn, params=(start_ts, end_ts))
    conn.close()
    return df