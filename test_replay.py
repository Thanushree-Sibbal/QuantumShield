from app.services.replay_service import replay

for i in range(5):
    tx = replay.next_transaction()

    print()
    print("Transaction", i + 1)
    print(tx["from_address"])
    print("↓")
    print(tx["to_address"])
    print(tx["value_eth"], "ETH")