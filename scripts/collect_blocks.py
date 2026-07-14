from dotenv import load_dotenv
from web3 import Web3
import os
import csv
from tqdm import tqdm

# Load environment variables
load_dotenv()

alchemy_url = os.getenv("ALCHEMY_URL")
w3 = Web3(Web3.HTTPProvider(alchemy_url))

if not w3.is_connected():
    print("❌ Failed to connect to Ethereum")
    exit()

print("✅ Connected to Ethereum")

latest_block = w3.eth.block_number

print(f"Latest Block: {latest_block}")

NUMBER_OF_BLOCKS = 100

os.makedirs("data/raw", exist_ok=True)

csv_file = "data/raw/transactions.csv"

with open(csv_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "tx_hash",
        "block_number",
        "timestamp",
        "from_address",
        "to_address",
        "value_wei",
        "gas",
        "gas_price",
        "nonce"
    ])

    total_transactions = 0

    for block_number in tqdm(
            range(latest_block,
                  latest_block - NUMBER_OF_BLOCKS,
                  -1)):

        block = w3.eth.get_block(
            block_number,
            full_transactions=True
        )

        timestamp = block.timestamp

        for tx in block.transactions:

            writer.writerow([
                tx.hash.hex(),
                tx.blockNumber,
                timestamp,
                tx["from"],
                tx.to,
                tx.value,
                tx.gas,
                tx.gasPrice,
                tx.nonce
            ])

            total_transactions += 1

print("\nFinished!")
print(f"Blocks Downloaded : {NUMBER_OF_BLOCKS}")
print(f"Transactions Saved: {total_transactions}")
print(f"CSV File: {csv_file}")