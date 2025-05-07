import numpy as np
from queue import Queue

### python3 main.py --network ./datasets/real/congress/network.hyp --algorithm str --k 10 --s 2 --c 1 ###

def decay(x, c):
    return 1 / (x ** c)

def run(hypergraph, k, s, c):
    min = 1/(len(hypergraph.nodes) ** c + 1) # due to floating-point precision error
    deg = np.zeros(len(hypergraph.nodes) + 1)
    max = np.zeros(len(hypergraph.nodes) + 1)
    nbr = np.zeros(len(hypergraph.nodes) + 1)
    closeness = np.zeros((len(hypergraph.nodes) + 1, len(hypergraph.nodes) + 1))

    for u in hypergraph.nodes:
        nbr_set = set()
        for e in hypergraph.nodes[u]['hyperedges']:
            max[u] += 1 / (len(e) ** c)
            for v in e:
                if v != u:
                    nbr_set.add(v)
                if u < v:
                    closeness[u][v] += 1 / (len(e) ** c)
                    closeness[v][u] += 1 / (len(e) ** c)
        nbr[u] = len(nbr_set)
        for v in hypergraph.nodes:
            if u < v and closeness[u][v] >= s - min:
                deg[u] += 1
                deg[v] += 1

    V = set(hypergraph.nodes)
    Q = Queue()
    
    for u in V:
        if deg[u] < k:
            Q.put(u)

    
    while not Q.empty():
        u = Q.get()

        for e in hypergraph.nodes[u]['hyperedges']:
            for v in e:
                for w in e:
                    if v >= w:
                        continue
                    if closeness[v][w] > s - min:
                        closeness[v][w] -= 1 / (len(e) ** c)
                        closeness[w][v] -= 1 / (len(e) ** c)
                        if closeness[v][w] < s - min:
                            deg[v] -= 1
                            deg[w] -= 1
                    else:
                        closeness[v][w] -= 1 / (len(e) ** c)
                        closeness[w][v] -= 1 / (len(e) ** c)
                if deg[v] < k and v not in list(Q.queue) and v != u:
                    Q.put(v)
                if v != u:
                    hypergraph.nodes[v]['hyperedges'].remove(e)

        V.remove(u)

    return hypergraph.subgraph(V)