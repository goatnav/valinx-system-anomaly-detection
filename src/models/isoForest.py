import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from storage.sql import insert_anomaly_scores   # 👈 import DB helper

# ===============================
# Config
# ===============================
CLEANED_PATH = "data/cleaned/cleaned.csv"
MODEL_NAME = "isolation_forest"

# ===============================
# Load cleaned data
# ===============================
df = pd.read_csv(CLEANED_PATH)

# Expect sample_id to exist
if "sample_id" not in df.columns:
    raise ValueError("sample_id missing from cleaned data")

# Columns NOT used for training
NON_FEATURE_COLS = [
    "sample_id",
    "ts_unix",
    "ts_readable",
    "trigger_ctx"
]

FEATURE_COLS = [c for c in df.columns if c not in NON_FEATURE_COLS]

X = df[FEATURE_COLS]

# ===============================
# Train Isolation Forest
# ===============================
iso = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)

iso.fit(X)

anomaly_labels = iso.predict(X)          # 1 = normal, -1 = anomaly
anomaly_scores = iso.decision_function(X)

# ===============================
# Build anomaly results DF
# ===============================
results_df = pd.DataFrame({
    "sample_id": df["sample_id"],
    "model": MODEL_NAME,
    "anomaly_label": anomaly_labels,
    "anomaly_score": anomaly_scores
})

# ===============================
# Persist to SQLite
# ===============================
insert_anomaly_scores(results_df)

print("✅ Isolation Forest anomalies stored in SQLite")
