import sqlite3
import pandas as pd
from src.config import DB_PATH


def get_worst_anomalies(limit=5):
    conn = sqlite3.connect(DB_PATH)

    query = """
       SELECT m.sample_id,
              m.ts_readable,
              m.CPU_perc,
              m.Mem_perc,
              m.disk_read_MBps,
              m.disk_write_MBps,
              m.net_sent_MBps,
              m.net_recv_MBps,
              a.anomaly_score,
              a.anomaly_label,
              m.trigger_ctx

    FROM metrics_raw m
    JOIN anomaly_scores a
        ON m.sample_id = a.sample_id
    WHERE a.model = 'isolation_forest'
    ORDER BY a.anomaly_score ASC
    LIMIT ?
    """

    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

def get_anomaly_by_sample_id(sample_id):
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT m.sample_id,
           m.ts_readable,
           m.CPU_perc,
           m.Mem_perc,
           m.disk_read_MBps,
           m.disk_write_MBps,
           m.net_sent_MBps,
           m.net_recv_MBps,
           a.anomaly_score,
           a.anomaly_label,
           m.trigger_ctx
    FROM metrics_raw m
    JOIN anomaly_scores a
        ON m.sample_id = a.sample_id
    WHERE a.model = 'isolation_forest'
      AND m.sample_id = ?
    LIMIT 1
    """

    df = pd.read_sql_query(query, conn, params=(sample_id,))
    conn.close()
    return df

def get_window_around_sample(sample_id, window_size=20):
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT m.sample_id,
           m.ts_readable,
           m.CPU_perc,
           m.Mem_perc,
           m.disk_read_MBps,
           m.disk_write_MBps,
           m.net_sent_MBps,
           m.net_recv_MBps,
           a.anomaly_score,
           a.anomaly_label,
           m.trigger_ctx
    FROM metrics_raw m
    LEFT JOIN anomaly_scores a
        ON m.sample_id = a.sample_id
       AND a.model = 'isolation_forest'
    WHERE m.sample_id BETWEEN ? AND ?
    ORDER BY m.sample_id ASC
    """

    start_id = max(0, sample_id - window_size)
    end_id = sample_id + window_size

    df = pd.read_sql_query(query, conn, params=(start_id, end_id))
    conn.close()
    return df
