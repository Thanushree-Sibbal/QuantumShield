import os
import torch
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("Normalizing LSTM Sequences")
print("=" * 60)

# ---------------------------------------
# Load tensor
# ---------------------------------------

tensor = torch.load(
    "models/lstm_sequences.pt",
    weights_only=False
)

print("Original Shape:", tensor.shape)

# ---------------------------------------
# Flatten for scaling
# ---------------------------------------

samples, seq_len, features = tensor.shape

flat = tensor.reshape(-1, features).numpy()

# ---------------------------------------
# Normalize
# ---------------------------------------

scaler = StandardScaler()

flat_scaled = scaler.fit_transform(flat)

normalized = torch.tensor(
    flat_scaled,
    dtype=torch.float32
).reshape(samples, seq_len, features)

print("Normalized Shape:", normalized.shape)

# ---------------------------------------
# Save
# ---------------------------------------

torch.save(
    normalized,
    "models/lstm_sequences_normalized.pt"
)

os.makedirs("models", exist_ok=True)

torch.save(
    scaler,
    "models/lstm_scaler.pt"
)

print()
print("Saved:")
print("models/lstm_sequences_normalized.pt")
print("models/lstm_scaler.pt")

print("=" * 60)