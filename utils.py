import networkx as nx

def load_hypergraph(file_path):
    hypergraph = nx.Graph()  # Create an empty hypergraph
    E = list()

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            # Use set to ignore duplicate values in each line and strip whitespace from node names
            if 'instacart' in file_path:
                nodes = {node.strip() for node in line.strip().split(' ')}
            else:
                nodes = {node.strip() for node in line.strip().split(',')}
            nodes = {int(x) for x in  nodes}
            hyperedge = set(nodes)  # Use frozenset to represent the hyperedge
            E.append(hyperedge)
            for node in nodes:
                if node not in hypergraph.nodes():
                    hypergraph.add_node(node, hyperedges=list(), max_s=0)  # Add a node for each node
                hypergraph.nodes[node]['hyperedges'].append(hyperedge)  # Add the hyperedge to the node's hyperedge set

    return hypergraph, E

def hyperedges_count(hypergraph, node): # count the number of hyperedges that contain the node = degree
    return len(hypergraph.nodes[node]['hyperedges'])

def edge_count(nodes,hyperedges): # Find a hyperedge that contains node
    edges = list()
    for hyperedge in hyperedges:

        if len(set(nodes) - hyperedge) == len(nodes) - len(hyperedge) :
            edges.append(hyperedge)
    return len(edges)