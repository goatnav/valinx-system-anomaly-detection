import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("data/raw/system_metrics.csv")

# Step 1: Look at the data
print(df.info())
print(df.head())

#saving the trigger data, because it is not a useful feature for training
trigger = df["trigger_ctx"]

#drop unecessary columns
df = df.drop(columns=['Time-(numerical)', 'Time-(readable)','trigger_ctx','index'], errors='ignore')

#we don't need duplicates. More data points of the same state do not affect the IsolationForest. 
df = df.drop_duplicates()

#replaces NaN or None values with the average of that column (for numeric values)
df = df.fillna(df.median(numeric_only=True))

#scales values to be centered around 0
scaler = StandardScaler()
X = scaler.fit_transform(df)

#convert back to csv
X = pd.DataFrame(X, columns=df.columns)

#output to the cleaned data folder
X.to_csv("data/cleaned/cleaned.csv", index=False)
print("outputted to cleaned.csv")

#maybe later output the triggered column
