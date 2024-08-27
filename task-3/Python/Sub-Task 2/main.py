fs = open("input.txt")
lines = fs.readlines()

newfs = open("output.txt", "w")
newfs.writelines(lines)
newfs.flush()