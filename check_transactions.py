import pandas as pd

file_path = "data/raw/transactions.csv"

df = pd.read_csv(file_path)

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

print("\n===== TOTAL ROWS =====")
print(len(df))

print("\n===== FIRST 5 ROWS =====")
print(df.head())