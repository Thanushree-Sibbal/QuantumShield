import torch

from model import WalletLSTM

model = WalletLSTM()

print("=" * 60)
print("Wallet LSTM")
print("=" * 60)

print(model)

dummy = torch.randn(
    16,
    20,
    4
)

output = model(dummy)

print()

print("Input Shape :", dummy.shape)

print("Output Shape:", output.shape)

params = sum(
    p.numel()
    for p in model.parameters()
)

print()

print("Total Parameters:", params)