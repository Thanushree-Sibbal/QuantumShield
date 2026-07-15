import pandas as pd

nodes = pd.read_csv("data/graph/graph_nodes.csv")
edges = pd.read_csv("data/graph/graph_edges.csv")
labels = pd.read_csv("data/labels/exploit_labels.csv")

print("="*50)
print("DATASET SUMMARY")
print("="*50)

print(f"Nodes  : {len(nodes)}")
print(f"Edges  : {len(edges)}")
print(f"Labels : {len(labels)}")

print("\nNode Columns:")
print(nodes.columns.tolist())

print("\nEdge Columns:")
print(edges.columns.tolist())

print("\nLabel Columns:")
print(labels.columns.tolist())

print("="*50)