import os
import pandas as pd

print("=" * 60)
print("Building Fusion Dataset")
print("=" * 60)

# ------------------------------------------------
# Load embeddings
# ------------------------------------------------

graph = pd.read_csv(
    "models/wallet_embeddings.csv"
)

lstm = pd.read_csv(
    "models/lstm_embeddings.csv"
)

print("Graph Wallets :", len(graph))
print("LSTM Wallets  :", len(lstm))

# ------------------------------------------------
# Merge on wallet address
# ------------------------------------------------

fusion = pd.merge(
    graph,
    lstm,
    on="wallet",
    how="inner",
    suffixes=("_graph", "_lstm")
)

print()

print("Merged Wallets :", len(fusion))

print()

print("Columns:", fusion.shape[1])

# ------------------------------------------------
# Save
# ------------------------------------------------

os.makedirs(
    "models",
    exist_ok=True
)

fusion.to_csv(
    "models/fusion_dataset.csv",
    index=False
)

print()

print("Saved:")
print("models/fusion_dataset.csv")

print("=" * 60)