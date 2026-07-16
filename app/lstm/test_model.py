import torch

from model import WalletLSTMAutoEncoder

model = WalletLSTMAutoEncoder()

print("=" * 60)
print("Wallet LSTM AutoEncoder")
print("=" * 60)

print(model)

dummy = torch.randn(16, 20, 4)

reconstruction, embedding = model(dummy)

print()

print("Input Shape :", dummy.shape)
print("Reconstruction :", reconstruction.shape)
print("Embedding :", embedding.shape)

params = sum(p.numel() for p in model.parameters())

print()
print("Total Parameters:", params)