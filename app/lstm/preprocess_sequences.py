import os
import ast
import torch
import pandas as pd

print("=" * 60)
print("Preprocessing Wallet Sequences")
print("=" * 60)

SEQUENCE_LENGTH = 20
FEATURES = 4

# --------------------------------------
# Load sequences
# --------------------------------------

df = pd.read_csv(
    "data/lstm/wallet_sequences.csv"
)

print("Wallets Loaded:", len(df))

tensor_data = []

# --------------------------------------
# Convert sequences
# --------------------------------------

for seq in df["sequence"]:

    sequence = ast.literal_eval(seq)

    # Keep last 20 transactions
    sequence = sequence[-SEQUENCE_LENGTH:]

    # Pad if needed
    while len(sequence) < SEQUENCE_LENGTH:
        sequence.insert(
            0,
            [0, 0, 0, 0]
        )

    tensor_data.append(sequence)

# --------------------------------------
# Tensor
# --------------------------------------

tensor = torch.tensor(
    tensor_data,
    dtype=torch.float32
)

print("Tensor Shape:", tensor.shape)

# --------------------------------------
# Save
# --------------------------------------

os.makedirs(
    "models",
    exist_ok=True
)

torch.save(
    tensor,
    "models/lstm_sequences.pt"
)

print()

print("Saved:")
print("models/lstm_sequences.pt")

print("=" * 60)