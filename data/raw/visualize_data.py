import pandas as pd, matplotlib.pyplot as plt

df = pd.read_csv("data/raw/system_metrics.csv")

df.plot(
    x="Time-(numerical)", 
    y=["CPU_perc", "Mem_perc"], 
    figsize=(10,5), 
    title="CPU and Memory Usage Over Time"
)
plt.xlabel("Time")
plt.ylabel("Percent (%)")
plt.grid(True)
plt.show()

