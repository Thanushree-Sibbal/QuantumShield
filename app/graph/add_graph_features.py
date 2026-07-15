import os
import pandas as pd
import networkx as nx

# -----------------------------
# Load datasets
# -----------------------------
nodes = pd.read_csv("data/graph/graph_nodes.csv")
edges = pd.read_csv("data/graph/graph_edges.csv")

print("Building graph...")

# Directed graph
G = nx.DiGraph()

# Add nodes
for wallet in nodes["wallet"]:
    G.add_node(wallet)

# Add edges
for _, row in edges.iterrows():
    G.add_edge(row["source"], row["target"])

print(f"Graph Built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# -----------------------------
# Compute graph features
# -----------------------------
print("Computing graph metrics...")

in_degree = dict(G.in_degree())
out_degree = dict(G.out_degree())
degree_centrality = nx.degree_centrality(G)
pagerank = nx.pagerank(G)
clustering = nx.clustering(G.to_undirected())

print("Metrics computed.")

# -----------------------------
# Add features to node dataset
# -----------------------------
nodes["in_degree"] = nodes["wallet"].map(in_degree).fillna(0)
nodes["out_degree"] = nodes["wallet"].map(out_degree).fillna(0)
nodes["degree_centrality"] = nodes["wallet"].map(degree_centrality).fillna(0)
nodes["pagerank"] = nodes["wallet"].map(pagerank).fillna(0)
nodes["clustering_coefficient"] = nodes["wallet"].map(clustering).fillna(0)

# -----------------------------
# Save updated dataset
# -----------------------------
nodes.to_csv("data/graph/graph_nodes.csv", index=False)

print("=" * 60)
print("Graph Feature Engineering Complete")
print("=" * 60)
print("Total Features :", len(nodes.columns) - 1)  # Excluding wallet column
print("Saved: data/graph/graph_nodes.csv")