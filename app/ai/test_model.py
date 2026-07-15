import torch

from graphsage import GraphSAGE

model = GraphSAGE(
    input_dim=14
)

print("="*50)
print("GraphSAGE Model")
print("="*50)

print(model)

total = sum(p.numel() for p in model.parameters())

print("\nTotal Parameters:", total)

dummy_x = torch.randn(10, 14)

edge_index = torch.tensor([
    [0,1,2,3,4,5,6,7,8],
    [1,2,3,4,5,6,7,8,9]
], dtype=torch.long)

output = model(dummy_x, edge_index)

print("\nOutput Shape:", output.shape)