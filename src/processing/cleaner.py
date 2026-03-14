import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

RAW_PATH = "data/raw/system_metrics.csv"
OUT_PATH = "data/cleaned/cleaned.csv"

df = pd.read_csv(RAW_PATH)

# Rename to match DB + model pipeline conventions
df = df.rename(columns={
    "Time-(numerical)": "ts_unix",
    "Time-(readable)": "ts_readable"
})

# Ensure sample_id exists (log_metrics should write it; this is a fallback)
if "sample_id" not in df.columns:
    df.insert(0, "sample_id", range(len(df)))

# Columns you want to keep for traceability (but NOT train on)
NON_FEATURE_COLS = ["sample_id", "ts_unix", "ts_readable", "trigger_ctx"]

FEATURE_COLS = [c for c in df.columns if c not in NON_FEATURE_COLS]

# IMPORTANT: if you drop duplicates, you break 1:1 mapping to raw rows
# df = df.drop_duplicates()

# Fill NaNs in FEATURES only
df[FEATURE_COLS] = df[FEATURE_COLS].fillna(df[FEATURE_COLS].median(numeric_only=True))

# Scale FEATURES only (do not touch IDs/timestamps/trigger strings)
scaler = StandardScaler()
df[FEATURE_COLS] = scaler.fit_transform(df[FEATURE_COLS])

os.makedirs("data/cleaned", exist_ok=True)
df.to_csv(OUT_PATH, index=False)
print("✅ outputted to data/cleaned/cleaned.csv")
