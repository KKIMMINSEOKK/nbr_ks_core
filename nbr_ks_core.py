from queue import Queue

### python3 main.py --network ./datasets/real/congress/network.hyp --algorithm ks --k 10 --s 2 --c 1 ###

def getNbrMap(hypergraph, node, s, c, min):
    strengths = {}

    for hyperedge in hypergraph.nodes[node]['hyperedges']:
        for neighbor in hyperedge:
            if neighbor != node:
                strengths[neighbor] = strengths.get(neighbor,0) + (1 / (len(hyperedge) ** c))
    s_neighbors = {node: strength for node, strength in strengths.items() if strength >= s - min}
    return s_neighbors

def run(hypergraph, k, s, c):
    min = 1/(len(hypergraph.nodes) ** c + 1) # due to floating-point precision error

    H = set(hypergraph.nodes())
    S = {}
    VQ = Queue()
    VQ1 = set()
    # time_report = 0

    for v in H:
        # time2 = time.time()
        s_neighbors = getNbrMap(hypergraph, v, s, c, min)
        # time3 = time.time()
        # time_report += time3 - time2
        S[v] = len(s_neighbors)
        if S[v] < k:
            VQ.put(v)
            VQ1.add(v)
    while not VQ.empty():
        v = VQ.get()
        # time2 = time.time()
        s_neighbors = getNbrMap(hypergraph, v, s, c, min)
        # time3 = time.time()
        # time_report += time3 - time2
        H.remove(v)
        del S[v]
        for w in s_neighbors:
            if w not in VQ1:
                S[w] -= 1
                if S[w] < k:
                    VQ.put(w)
                    VQ1.add(w)

    # print(H)

    return hypergraph.subgraph(H)
    # return H, time_report
