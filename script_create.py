import os
dir = "./datasets/real/"

# read all the files in the directory
files  = os.listdir(dir)
# we need to remove .DS_Store and MAG file 
# file.remove('.DS_Store')
# file.remove('MAG')

# files = ["contact", "congress"]


# write the output to a file
with open("run.sh", "w") as f:
    for file in files:
        for k in range(10,60,10):
            for s in range(1,10):
                for c in range(1, 4):
                    print(f"python3 main.py --network {dir}{file}/network.hyp --algorithm ks --k {k} --s {round(s * 0.5, 1)} --c {round(c * 0.5, 1)} &&")
                    f.write(f"python3 main.py --network {dir}{file}/network.hyp --algorithm ks --k {k} --s {round(s * 0.5, 1)} --c {round(c * 0.5, 1)} &&\n")

with open("run.sh", "rb+") as f:
    f.seek(-4, 2)
    f.truncate()