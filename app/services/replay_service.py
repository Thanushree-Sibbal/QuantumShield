import pandas as pd
from itertools import cycle

class TransactionReplay:

    def __init__(self):
        self.df = pd.read_csv("data/raw/transactions.csv")

        # Convert Wei → ETH
        self.df["value_eth"] = (
            self.df["value_wei"].astype(float) / 1e18
        ).round(6)

        # Infinite iterator
        self.transactions = cycle(
            self.df.to_dict(orient="records")
        )

    def next_transaction(self):
        return next(self.transactions)


# Global replay object
replay = TransactionReplay()