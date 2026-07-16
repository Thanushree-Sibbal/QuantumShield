import pandas as pd

print("=" * 60)
print("Fusion Dataset Summary")
print("=" * 60)

df = pd.read_csv("models/fusion_dataset.csv")

print("Shape:", df.shape)

print("\nColumns:")

print(df.columns.tolist())

print("\nFirst 5 Rows:")

print(df.head())

print("\nMissing Values:")

print(df.isnull().sum().sum())