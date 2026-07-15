import os
import pandas as pd

# -------------------------
# Load transaction data
# -------------------------
df = pd.read_csv("data/raw/transactions.csv")

# Convert Wei to ETH
df["value_eth"] = df["value_wei"] / 10**18

wallets = {}

for _, tx in df.iterrows():

    sender = tx["from_address"]
    receiver = tx["to_address"]
    value = tx["value_eth"]

    # -------------------------
    # Sender
    # -------------------------
    if sender not in wallets:
        wallets[sender] = {
            "wallet": sender,
            "sent_count": 0,
            "received_count": 0,
            "eth_sent": 0.0,
            "eth_received": 0.0,
            "neighbors": set()
        }

    wallets[sender]["sent_count"] += 1
    wallets[sender]["eth_sent"] += value

    if pd.notna(receiver):
        wallets[sender]["neighbors"].add(receiver)

    # -------------------------
    # Receiver
    # -------------------------
    if pd.notna(receiver):

        if receiver not in wallets:
            wallets[receiver] = {
                "wallet": receiver,
                "sent_count": 0,
                "received_count": 0,
                "eth_sent": 0.0,
                "eth_received": 0.0,
                "neighbors": set()
            }

        wallets[receiver]["received_count"] += 1
        wallets[receiver]["eth_received"] += value
        wallets[receiver]["neighbors"].add(sender)

# -------------------------
# Final Features
# -------------------------
rows = []

for wallet, data in wallets.items():

    total_tx = data["sent_count"] + data["received_count"]
    total_volume = data["eth_sent"] + data["eth_received"]

    avg_tx = (
        total_volume / total_tx
        if total_tx > 0 else 0
    )

    activity_score = (
        total_tx + len(data["neighbors"])
    )

    rows.append({
        "wallet": wallet,
        "sent_count": data["sent_count"],
        "received_count": data["received_count"],
        "total_transactions": total_tx,
        "eth_sent": data["eth_sent"],
        "eth_received": data["eth_received"],
        "total_volume": total_volume,
        "avg_tx_value": avg_tx,
        "unique_neighbors": len(data["neighbors"]),
        "activity_score": activity_score
    })

feature_df = pd.DataFrame(rows)

os.makedirs("data/graph", exist_ok=True)

feature_df.to_csv(
    "data/graph/graph_nodes.csv",
    index=False
)

print("===================================")
print("Node Feature Engineering Complete")
print("Wallets:", len(feature_df))
print("Saved:", "data/graph/graph_nodes.csv")
print("===================================")