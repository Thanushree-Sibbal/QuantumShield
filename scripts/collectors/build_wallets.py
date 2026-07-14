import pandas as pd
import os

# Load transactions
df = pd.read_csv("data/raw/transactions.csv")

# Convert Wei to ETH
df["value_eth"] = df["value_wei"] / 10**18

wallets = {}

for _, tx in df.iterrows():

    sender = tx["from_address"]
    receiver = tx["to_address"]
    value = tx["value_eth"]

    # Sender
    if sender not in wallets:
        wallets[sender] = {
            "wallet": sender,
            "sent_count": 0,
            "received_count": 0,
            "eth_sent": 0,
            "eth_received": 0
        }

    wallets[sender]["sent_count"] += 1
    wallets[sender]["eth_sent"] += value

    # Receiver
    if pd.notna(receiver):

        if receiver not in wallets:
            wallets[receiver] = {
                "wallet": receiver,
                "sent_count": 0,
                "received_count": 0,
                "eth_sent": 0,
                "eth_received": 0
            }

        wallets[receiver]["received_count"] += 1
        wallets[receiver]["eth_received"] += value

# Convert dictionary to DataFrame
wallet_df = pd.DataFrame(wallets.values())

os.makedirs("data/processed", exist_ok=True)

wallet_df.to_csv("data/processed/wallets.csv", index=False)

print("Wallets created:", len(wallet_df))
print("Saved to data/processed/wallets.csv")