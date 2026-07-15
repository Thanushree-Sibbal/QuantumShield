import os
import pandas as pd
import networkx as nx

# ------------------------
# Load transactions
# ------------------------
transactions = pd.read_csv("data/raw/transactions.csv")

# Convert Wei → ETH
transactions["value_eth"] = transactions["value_wei"] / 10**18

# ------------------------
# Create Directed Graph
# ------------------------
G = nx.DiGraph()

for _, tx in transactions.iterrows():

    sender = tx["from_address"]
    receiver = tx["to_address"]

    # Ignore contract creation transactions
    if pd.isna(receiver):
        continue

    G.add_edge(
        sender,
        receiver,
        value=tx["value_eth"],
        block=tx["block_number"]
    )

# ------------------------
# Create graph folder
# ------------------------
os.makedirs("data/graph", exist_ok=True)

# ------------------------
# Save Nodes
# ------------------------
nodes = pd.DataFrame({
    "wallet": list(G.nodes())
})

nodes.to_csv(
    "data/graph/graph_nodes.csv",
    index=False
)

# ------------------------
# Save Edges
# ------------------------
edges = []

for u, v, data in G.edges(data=True):
    edges.append({
        "source": u,
        "target": v,
        "value_eth": data["value"],
        "block_number": data["block"]
    })

edges = pd.DataFrame(edges)

edges.to_csv(
    "data/graph/graph_edges.csv",
    index=False
)

print("================================")
print("Graph Created Successfully")
print("================================")
print("Nodes :", G.number_of_nodes())
print("Edges :", G.number_of_edges())
print("================================")