import os
import torch
from torch_geometric.nn import GAE

from graphsage import GraphSAGEEncoder

print("=" * 60)
print("Loading Graph Dataset")
print("=" * 60)

data = torch.load(
    "models/graph_data.pt",
    weights_only=False
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(data)
print("Device:", device)

encoder = GraphSAGEEncoder(
    input_dim=data.num_node_features,
    hidden_dim=64,
    embedding_dim=32
)

model = GAE(encoder).to(device)

data = data.to(device)

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

print("=" * 60)
print("Starting Training")
print("=" * 60)

EPOCHS = 30

for epoch in range(EPOCHS):

    model.train()

    optimizer.zero_grad()

    z = model.encode(
        data.x,
        data.edge_index
    )

    loss = model.recon_loss(
        z,
        data.edge_index
    )

    loss.backward()

    optimizer.step()

    print(
        f"Epoch {epoch+1:02d}/{EPOCHS} | Loss: {loss:.4f}"
    )

print("=" * 60)
print("Training Complete")
print("=" * 60)
# -----------------------------
# Save trained model
# -----------------------------
os.makedirs("models", exist_ok=True)

torch.save(
    model.state_dict(),
    "models/graphsage_model.pt"
)

print("Model saved successfully!")
print("Saved to: models/graphsage_model.pt")