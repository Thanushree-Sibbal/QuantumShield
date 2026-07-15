import os
import json
import torch
import pandas as pd
from torch_geometric.data import Data

# --------------------------
# Load CSV files
# --------------------------
nodes = pd.read_csv("data/graph/graph_nodes.csv")
edges = pd.read_csv("data/graph/graph_edges.csv")

print("Loading datasets...")

# --------------------------
# Create Wallet -> ID mapping
# --------------------------
wallet_to_id = {
    wallet: idx
    for idx, wallet in enumerate(nodes["wallet"])
}

print("Wallet mapping created.")

# --------------------------
# Convert edge list to IDs
# --------------------------
edge_list = []

missing_edges = 0

for _, row in edges.iterrows():

    src = row["source"]
    dst = row["target"]

    if src in wallet_to_id and dst in wallet_to_id:

        edge_list.append([
            wallet_to_id[src],
            wallet_to_id[dst]
        ])

    else:
        missing_edges += 1

print(f"Missing edges skipped: {missing_edges}")

# --------------------------
# Build edge_index
# --------------------------
edge_index = torch.tensor(
    edge_list,
    dtype=torch.long
).t().contiguous()

print("edge_index shape:", edge_index.shape)

# --------------------------
# Node Feature Matrix
# --------------------------

feature_columns = [
    "sent_count",
    "received_count",
    "total_transactions",
    "eth_sent",
    "eth_received",
    "total_volume",
    "avg_tx_value",
    "unique_neighbors",
    "activity_score",
    "in_degree",
    "out_degree",
    "degree_centrality",
    "pagerank",
    "clustering_coefficient"
]

x = torch.tensor(
    nodes[feature_columns].values,
    dtype=torch.float
)

print("Feature matrix shape:", x.shape)

# --------------------------
# Create PyG Data Object
# --------------------------
data = Data(
    x=x,
    edge_index=edge_index
)

# --------------------------
# Save outputs
# --------------------------
os.makedirs("models", exist_ok=True)

torch.save(
    data,
    "models/graph_data.pt"
)

with open(
    "models/wallet_to_id.json",
    "w"
) as f:

    json.dump(wallet_to_id, f)

print("=" * 50)
print("PyTorch Geometric Dataset Created")
print("=" * 50)
print(data)