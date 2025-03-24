import pandas as pd

df = pd.read_csv("./raw_data/data/rawdata.csv")

label_counts = df["label"].value_counts()

print(label_counts)
