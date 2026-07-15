import torch
import pandas as pd
from torch_geometric.nn import GAE

from graphsage import GraphSAGEEncoder

print("=" * 60)
print("Loading Graph Dataset")
print("=" * 60)

# ---------------------------------------------------
# Load graph
# ---------------------------------------------------

data = torch.load(
    "models/graph_data.pt",
    weights_only=False
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

data = data.to(device)

# ---------------------------------------------------
# Build model
# ---------------------------------------------------

encoder = GraphSAGEEncoder(
    input_dim=data.num_node_features,
    hidden_dim=64,
    embedding_dim=32
)

model = GAE(encoder).to(device)

# ---------------------------------------------------
# Load trained weights
# ---------------------------------------------------

model.load_state_dict(
    torch.load(
        "models/graphsage_model.pt",
        weights_only=False
    )
)

model.eval()

print("Model Loaded Successfully")

# ---------------------------------------------------
# Generate embeddings
# ---------------------------------------------------

with torch.no_grad():

    embeddings = model.encode(
        data.x,
        data.edge_index
    )

print("Embeddings Generated")

print("Embedding Shape:", embeddings.shape)

# ---------------------------------------------------
# Save tensor
# ---------------------------------------------------

torch.save(
    embeddings.cpu(),
    "models/wallet_embeddings.pt"
)

print("Saved: models/wallet_embeddings.pt")

# ---------------------------------------------------
# Save CSV
# ---------------------------------------------------

wallets = pd.read_csv(
    "data/graph/graph_nodes.csv"
)

embedding_df = pd.DataFrame(
    embeddings.cpu().numpy()
)

embedding_df.insert(
    0,
    "wallet",
    wallets["wallet"]
)

embedding_df.to_csv(
    "models/wallet_embeddings.csv",
    index=False
)

print("Saved: models/wallet_embeddings.csv")

print("=" * 60)
print("Module 8.6 Completed Successfully")
print("=" * 60)