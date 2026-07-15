import os
import pandas as pd

print("=" * 60)
print("Building Wallet Transaction Sequences")
print("=" * 60)

# ---------------------------------------
# Load transactions
# ---------------------------------------

transactions = pd.read_csv("data/raw/transactions.csv")

print("Transactions Loaded:", len(transactions))

# ---------------------------------------
# Convert Wei to ETH
# ---------------------------------------

transactions["value_eth"] = transactions["value_wei"] / 1e18

# ---------------------------------------
# Sort chronologically
# ---------------------------------------

transactions = transactions.sort_values("block_number")

# ---------------------------------------
# Build outgoing transaction sequences
# ---------------------------------------

wallet_sequences = {}

for wallet, group in transactions.groupby("from_address"):

    sequence = group[
        ["block_number", "value_eth", "gas", "gas_price"]
    ].values.tolist()

    wallet_sequences[wallet] = sequence

print("Unique Wallets:", len(wallet_sequences))

# ---------------------------------------
# Save sequences
# ---------------------------------------

os.makedirs("data/lstm", exist_ok=True)

sequence_df = pd.DataFrame({
    "wallet": list(wallet_sequences.keys()),
    "sequence": list(wallet_sequences.values())
})

sequence_df.to_csv(
    "data/lstm/wallet_sequences.csv",
    index=False
)

print()
print("Saved:")
print("data/lstm/wallet_sequences.csv")
print("=" * 60)