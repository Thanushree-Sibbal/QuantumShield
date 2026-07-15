import os
import pandas as pd

# -----------------------------
# Load data
# -----------------------------
graph = pd.read_csv("data/graph/graph_nodes.csv")
labels = pd.read_csv("data/external_data/labelled_addresses/eth_addresses.csv")

# -----------------------------
# Standardize addresses
# -----------------------------
graph["wallet"] = graph["wallet"].astype(str).str.lower().str.strip()
labels["Address"] = labels["Address"].astype(str).str.lower().str.strip()

# Keep required columns
labels = labels[["Address", "Label"]]

# Merge
merged = graph.merge(
    labels,
    left_on="wallet",
    right_on="Address",
    how="left"
)

# -----------------------------
# Assign labels
# -----------------------------
def assign_label(x):
    if pd.isna(x):
        return -1          # Unknown
    elif str(x).lower() == "legit":
        return 0           # Legit
    else:
        return 1           # Malicious

merged["label"] = merged["Label"].apply(assign_label)
merged["attack_type"] = merged["Label"].fillna("Unknown")

final = merged[["wallet", "label", "attack_type"]]

os.makedirs("data/labels", exist_ok=True)

final.to_csv(
    "data/labels/exploit_labels.csv",
    index=False
)

print("=" * 60)
print("Labels Created Successfully")
print("=" * 60)
print("Known Legit     :", (final["label"] == 0).sum())
print("Known Malicious :", (final["label"] == 1).sum())
print("Unknown         :", (final["label"] == -1).sum())
print("=" * 60)