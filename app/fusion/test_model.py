import torch

from model import FusionNetwork

model = FusionNetwork()

print("=" * 60)
print("Fusion Network")
print("=" * 60)

print(model)

dummy = torch.randn(16, 64)

output = model(dummy)

print()
print("Input Shape :", dummy.shape)
print("Output Shape:", output.shape)

params = sum(p.numel() for p in model.parameters())

print()
print("Total Parameters:", params)