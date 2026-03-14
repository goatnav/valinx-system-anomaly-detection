import sqlite3
import pandas as pd

DB_PATH = "data/valinx.db"
MODEL = "isolation_forest"

conn = sqlite3.connect(DB_PATH)

q = """
SELECT
  m.sample_id,
  m.ts_readable,
  m.CPU_perc,
  m.Mem_perc,
  a.model,
  a.anomaly_label,
  a.anomaly_score,
  m.trigger_ctx
FROM metrics_raw m
JOIN anomaly_scores a
  ON m.sample_id = a.sample_id
WHERE a.model = ?
ORDER BY a.anomaly_score ASC
LIMIT 25;
"""

df = pd.read_sql_query(q, conn, params=(MODEL,))
conn.close()

print(df.to_string(index=False))
