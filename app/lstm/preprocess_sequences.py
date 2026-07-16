import os
import ast
import torch
import pandas as pd
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("Preprocessing Wallet Sequences")
print("=" * 60)

SEQUENCE_LENGTH = 20

# --------------------------------------
# Load sequences
# --------------------------------------

df = pd.read_csv("data/lstm/wallet_sequences.csv")

print("Wallets Loaded:", len(df))

# --------------------------------------
# Parse all sequences
# --------------------------------------

all_sequences = []
all_transactions = []

for seq in df["sequence"]:
    sequence = ast.literal_eval(seq)

    # Keep last 20 transactions
    sequence = sequence[-SEQUENCE_LENGTH:]

    all_sequences.append(sequence)

    for tx in sequence:
        all_transactions.append(tx)

# --------------------------------------
# Normalize ONLY real transactions
# --------------------------------------

scaler = StandardScaler()

scaler.fit(all_transactions)

# --------------------------------------
# Normalize + Pad
# --------------------------------------

tensor_data = []

for sequence in all_sequences:

    normalized = scaler.transform(sequence).tolist()

    while len(normalized) < SEQUENCE_LENGTH:
        normalized.insert(0, [0.0, 0.0, 0.0, 0.0])

    tensor_data.append(normalized)

tensor = torch.tensor(
    tensor_data,
    dtype=torch.float32
)

print("Tensor Shape:", tensor.shape)

# --------------------------------------
# Save
# --------------------------------------

os.makedirs("models", exist_ok=True)

torch.save(
    tensor,
    "models/lstm_sequences_normalized.pt"
)

torch.save(
    scaler,
    "models/lstm_scaler.pt"
)

print()
print("Saved:")
print("models/lstm_sequences_normalized.pt")
print("models/lstm_scaler.pt")

print("=" * 60)