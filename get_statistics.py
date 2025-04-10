import utils

def degree(hypergraph, node):
    neighbors = set()
    for hyperedge in hypergraph.nodes[node]['hyperedges']:
        neighbors.update(hyperedge - {node})  # Collect all nodes in the hyperedge except the current node
    return len(neighbors)

input_file = './datasets/real/congress/network.hyp'
hypergraph, E = utils.load_hypergraph(input_file)

print(f'Number of nodes: {len(hypergraph.nodes)}')
print(f'Number of edges: {len(E)}')

sum = 0
for e in E:
    sum = sum + len(e)

# average cardinality
print(f'Average Cardinality: {sum / len(E)}')

# average degree
sum = 0
for v in hypergraph.nodes:
    sum = sum + degree(hypergraph, v)

print(f'Average Degree: {sum / len(hypergraph.nodes)}')