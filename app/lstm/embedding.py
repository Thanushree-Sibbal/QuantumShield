import torch
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset

from model import WalletLSTMAutoEncoder

print("=" * 60)
print("Generating LSTM Embeddings")
print("=" * 60)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ----------------------------------------
# Load sequences
# ----------------------------------------

data = torch.load(
    "models/lstm_sequences_normalized.pt",
    weights_only=False
)

dataset = TensorDataset(data)

loader = DataLoader(
    dataset,
    batch_size=256,
    shuffle=False
)

# ----------------------------------------
# Load model
# ----------------------------------------

model = WalletLSTMAutoEncoder().to(device)

model.load_state_dict(
    torch.load(
        "models/lstm_autoencoder.pt",
        weights_only=False
    )
)

model.eval()

embeddings = []

print("Generating embeddings...")

with torch.no_grad():

    for (batch,) in loader:

        batch = batch.to(device)

        _, embedding = model(batch)

        embeddings.append(
            embedding.cpu()
        )

embeddings = torch.cat(
    embeddings,
    dim=0
)

print("Embedding Shape:", embeddings.shape)

# ----------------------------------------
# Save tensor
# ----------------------------------------

torch.save(
    embeddings,
    "models/lstm_embeddings.pt"
)

# ----------------------------------------
# Save CSV
# ----------------------------------------

wallets = pd.read_csv(
    "data/lstm/wallet_sequences.csv"
)

embedding_df = pd.DataFrame(
    embeddings.numpy()
)

embedding_df.insert(
    0,
    "wallet",
    wallets["wallet"]
)

embedding_df.to_csv(
    "models/lstm_embeddings.csv",
    index=False
)

print()
print("Saved:")
print("models/lstm_embeddings.pt")
print("models/lstm_embeddings.csv")

print("=" * 60)