import torch

data = torch.load(
    "models/lstm_sequences_normalized.pt",
    weights_only=False
)

print("=" * 60)
print("Dataset Shape")
print("=" * 60)

print(data.shape)

print()

print("First Wallet Sequence:")

print(data[0])

print()

print("Contains NaN:", torch.isnan(data).any().item())

print("Contains Inf:", torch.isinf(data).any().item())

print()

print("Min:", data.min().item())

print("Max:", data.max().item())

print("Mean:", data.mean().item())

print("Std:", data.std().item())