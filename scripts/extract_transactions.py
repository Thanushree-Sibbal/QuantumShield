from dotenv import load_dotenv
from web3 import Web3
import os
import csv

# Load environment variables
load_dotenv()

alchemy_url = os.getenv("ALCHEMY_URL")
w3 = Web3(Web3.HTTPProvider(alchemy_url))

if not w3.is_connected():
    print("Failed to connect to Ethereum")
    exit()

print("Connected to Ethereum!")

latest_block = w3.eth.block_number
print("Latest Block:", latest_block)

# Get full transaction objects
block = w3.eth.get_block(latest_block, full_transactions=True)

os.makedirs("data/raw", exist_ok=True)

csv_path = "data/raw/transactions.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "tx_hash",
        "block_number",
        "from_address",
        "to_address",
        "value_wei",
        "gas",
        "gas_price",
        "nonce"
    ])

    for tx in block.transactions:
        writer.writerow([
            tx.hash.hex(),
            tx.blockNumber,
            tx["from"],
            tx.to,
            tx.value,
            tx.gas,
            tx.gasPrice,
            tx.nonce
        ])

print(f"Saved {len(block.transactions)} transactions to {csv_path}")