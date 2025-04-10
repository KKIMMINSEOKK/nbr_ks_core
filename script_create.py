import os
dir = "./datasets/real/"

# read all the files in the directory
file  = os.listdir(dir)
# we need to remove .DS_Store and MAG file 
# file.remove('.DS_Store')
# file.remove('MAG')

file = ["contact"]

# write the output to a file
with open("run.sh", "w") as f:
    for file in file:
        for k in range(10,60,10):
            for s in range(0,10):
                print(f"python main.py --network {dir}{file}/network.hyp --algorithm ks --k {k} --s {round(s * 0.1, 1)} &&")
                f.write(f"python main.py --network {dir}{file}/network.hyp --algorithm ks --k {k} --s {round(s * 0.1, 1)} &&\n")
