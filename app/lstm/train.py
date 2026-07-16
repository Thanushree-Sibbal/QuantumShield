import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from model import WalletLSTMAutoEncoder

print("=" * 60)
print("Training Wallet LSTM AutoEncoder")
print("=" * 60)

# --------------------------------------------------
# Device
# --------------------------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Device:", device)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

data = torch.load(
    "models/lstm_sequences_normalized.pt",
    weights_only=False
)

dataset = TensorDataset(data)

loader = DataLoader(
    dataset,
    batch_size=256,
    shuffle=True
)

print("Wallet Sequences:", len(dataset))

# --------------------------------------------------
# Model
# --------------------------------------------------

model = WalletLSTMAutoEncoder().to(device)

criterion = nn.MSELoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

# --------------------------------------------------
# Training
# --------------------------------------------------

epochs = 20

print()
print("Starting Training...")
print()

for epoch in range(epochs):

    model.train()

    total_loss = 0

    for (batch,) in loader:

        batch = batch.to(device)

        reconstruction, embedding = model(batch)

        loss = criterion(
            reconstruction,
            batch
        )

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(loader)

    print(
        f"Epoch {epoch+1:02d}/{epochs} | Loss: {avg_loss:.6f}"
    )

# --------------------------------------------------
# Save
# --------------------------------------------------

os.makedirs("models", exist_ok=True)

torch.save(
    model.state_dict(),
    "models/lstm_autoencoder.pt"
)

print()
print("=" * 60)
print("Training Complete")
print("=" * 60)

print("Saved:")
print("models/lstm_autoencoder.pt")