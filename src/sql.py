import pandas as pd
import sqlite3

DB_PATH = "data/valinx.db"

def insert_raw_metrics(csv_path="data/raw/system_metrics.csv"):
    df = pd.read_csv(csv_path)

    # Rename CSV columns → DB schema columns
    df = df.rename(columns={
        "Time-(numerical)": "ts_unix",
        "Time-(readable)": "ts_readable"
    })

    # Add stable key
    df.insert(0, "sample_id", range(len(df)))

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("metrics_raw", conn, if_exists="append", index=False)
    conn.close()

    print("✅ Raw metrics stored")

def insert_anomaly_scores(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("anomaly_scores", conn, if_exists="append", index=False)
    conn.close()

    print("✅ Anomaly scores inserted")



if __name__ == "__main__":
    insert_raw_metrics()
    insert_anomaly_scores()
