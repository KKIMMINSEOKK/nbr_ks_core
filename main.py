import argparse
import utils
import psutil
import os
import time

import nbr_ks_core

parser = argparse.ArgumentParser(description="Peeling Algorithm for Hypergraph nbr-(k,s)-core")
parser.add_argument("--algorithm", help="Algorithm to use", choices=["ks"], default="ks")
parser.add_argument("--network", help="Path to the network file"
                    ,default='./ex.hyp')
parser.add_argument("--k", type=int, help="Value of k",default=2)
parser.add_argument("--s", type=float, help="Value of s",default=0.5)
args = parser.parse_args()

process = psutil.Process(os.getpid())
memory_before = process.memory_info().rss / (1024 * 1024)  # Convert to MB
# Load hypergraph
hypergraph, E = utils.load_hypergraph(args.network)

if args.algorithm == "ks":
    start_time = time.time()
    G = nbr_ks_core.run(hypergraph, args.k, args.s)
    end_time = time.time()

memory_after = process.memory_info().rss / (1024 * 1024)  # Convert to MB
memory_usage = memory_after - memory_before  # Calculate memory used

# Write results to file
output_dir = os.path.dirname(args.network)

output_filename = f"{args.algorithm}_{args.k}_{args.s}_core.dat"
output_path = os.path.join(output_dir, output_filename)

with open(output_path, 'w') as output_file:
    # Write size of nodes
    output_file.write(f"Num of nodes: {str(len(G))}\n")
    # Write running time
    output_file.write(f"Run Time: {end_time - start_time}\n")
    # Write nodes    
    output_file.write("Nodes:")
    nodes = " ".join(str(node) for node in G)
    output_file.write(nodes + "\n")

    #write memory usage
    output_file.write("Memory Usage(MB): ")
    output_file.write(f"{memory_usage}\n")

print(f"Num of nodes: {str(len(G))}\n")
print(f"Run Time: {end_time - start_time}\n")
print(f"Memory Usage(MB): {memory_usage}\n")


print(f"Results written to {output_path}")