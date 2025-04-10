import os
import csv
import argparse
import utils

# Argument parser for command-line arguments
parser = argparse.ArgumentParser(description="Extract data from ks files and save to CSV")
parser.add_argument("--directory", help="Path to the directory containing files"
                    , default='./datasets/real/contact/')
parser.add_argument("--output", help="Output CSV file name", default='summary.csv')
args = parser.parse_args()

input_file = args.directory + 'network.hyp'
hypergraph, E = utils.load_hypergraph(input_file)
output_f = args.directory.split('/')[-2]+'_summary.csv'
# Define the output CSV file path
output_csv_path = os.path.join(args.directory, output_f)

# Prepare data dictionary for ks data
data = {}

# Loop through each file in the directory
for filename in os.listdir(args.directory):
    # Process only files starting with "EPA"
    if filename.startswith("ks"):
        file_path = os.path.join(args.directory, filename)

        # Extract algorithm, k, and s from the filename
        algorithm = "ks"
        k = int(filename.split("_")[1])
        s = float(filename.split("_")[2])
        c = int(filename.split("_")[3])

        # Read the file to get node count, runtime, and nodes
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Initialize variables
            num_of_nodes = None
            runtime = None
            nodes = []

            for line in lines:
                # Extract number of nodes
                if line.startswith("Num of nodes:"):
                    num_of_nodes = int(line.split(":")[1].strip())

                # Extract runtime
                elif line.startswith("Run Time:"):
                    runtime = float(line.split(":")[1].strip())

                # Extract nodes list
                elif line.startswith("Nodes:"):
                    nodes = line.split(":")[1].strip().split()
                    nodes = [int(node) for node in nodes]  # Convert nodes to integer list
            average_cardinality = 0
            average_degree = 0
            if num_of_nodes == 0 or runtime is None:
                continue


            average_cardinality = utils.edge_count(nodes,E)
            average_cardinality = average_cardinality / len(nodes)
            
            
            for v in nodes:
                average_degree += utils.hyperedges_count(hypergraph, v)
            average_degree = average_degree / len(nodes)


            # Store EPA data in a dictionary with (k, g) as the key
            data[(k, s, c)] = {
                "algorithm": algorithm,
                "k": k,
                "s": s,
                "c": c,
                "# of nodes": num_of_nodes,
                "runtime": runtime,
                "average_degree": average_degree,
                "average_cardinality": average_cardinality,  # Assuming average_cardinality is 0 as per original code
                "dataset": args.directory.split('/')[-2]
            }

data = list(data.values())

# Write the data to a CSV file
with open(output_csv_path, 'w', newline='') as csvfile:
    fieldnames = ["algorithm", "k", "s", "c", "# of nodes", "runtime", "average_degree", "average_cardinality", "dataset"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"Data successfully written to {output_csv_path}")