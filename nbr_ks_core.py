import numpy as np
from queue import Queue

### python main.py --network ./datasets/real/congress/network.hyp --algorithm ks --k 20 --s 0.5 ###

# complexity 재계산 => 어차피 e만큼 업데이트 됨

# def remove_incident_edges(hypergraph, u):
#     for edge in hypergraph.nodes[u]['hyperedges']:
#         for neighbour in edge:
#             if neighbour != u:
#                 if edge in hypergraph.nodes[neighbour]['hyperedges']:
#                     hypergraph.nodes[neighbour]['hyperedges'].remove(edge)
#     return hypergraph

def decay(x, c):
    return 1 / (x ** c)

def run(hypergraph, E, k, s):
    c = 1
    min = 1/(len(hypergraph.nodes) ** c + 1) # due to floating-point precision error
    deg = np.zeros(len(hypergraph.nodes) + 1)
    closeness = np.zeros((len(hypergraph.nodes) + 1, len(hypergraph.nodes) + 1))


    for u in hypergraph.nodes:
        for e in hypergraph.nodes[u]['hyperedges']:
            for v in e:
                if u < v:
                    closeness[u][v] += decay(len(e), c)
                    closeness[v][u] += decay(len(e), c)
        for v in hypergraph.nodes:
            if u < v and closeness[u][v] >= s - min:
                deg[u] += 1
                deg[v] += 1

    # for e in E:
    #     for u in e:
    #         for v in e:
    #             if u < v:
    #                 closeness[u][v] += decay(len(e), c)
                    # closeness[v][u] += decay(len(e), c)
    #         for v in hypergraph.nodes:
    #             if u < v and closeness[u][v] >= s - min:
    #                 deg[u] += 1
    #                 deg[v] += 1

    Q = Queue()
    for u in hypergraph.nodes:
        if deg[u] < k:
            Q.put(u)

    V = set(hypergraph.nodes)
    while not Q.empty():
        u = Q.get()

        for e in hypergraph.nodes[u]['hyperedges']:
            for v in e:
                for w in e:
                    if v >= w:
                        continue
                    if closeness[v][w] > s - min:
                        closeness[v][w] -= decay(len(e), c)
                        closeness[w][v] -= decay(len(e), c)
                        if closeness[v][w] < s - min:
                            deg[v] -= 1
                            deg[w] -= 1
                    else:
                        closeness[v][w] -= decay(len(e), c)
                        closeness[w][v] -= decay(len(e), c)
                if deg[v] < k and v not in list(Q.queue) and v != u:
                    Q.put(v)
                if v != u:
                    hypergraph.nodes[v]['hyperedges'].remove(e)

        V.remove(u)

    return hypergraph.subgraph(V)