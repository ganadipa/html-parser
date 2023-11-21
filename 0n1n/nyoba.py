with open("pda0n1n.txt", "r") as f:
    line = f.readline()
    while line != "":
        print(line[:-1])
        line = f.readline()
