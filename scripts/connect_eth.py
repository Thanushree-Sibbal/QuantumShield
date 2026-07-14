from dotenv import load_dotenv
from web3 import Web3
import os

# Load environment variables
load_dotenv()

# Read the Alchemy URL
alchemy_url = os.getenv("ALCHEMY_URL")

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check connection
if w3.is_connected():
    print("Connected to Ethereum!")
else:
    print("Connection failed!")
    exit()

# Get latest block number
latest_block = w3.eth.block_number
print("Latest Block:", latest_block)