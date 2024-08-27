import math

fr = open("input.txt")
f = open("output.txt", "w")
n = int(fr.read())
fr.close()
counter = n%2

for i in range(n):
	if counter == 0:
		counter += 2
		continue

	stars = "*"*counter
	spaces = " "*math.floor((n-counter)/2)

	if i < math.floor(n/2):
		counter += 2
	else:
		counter -= 2
	
	f.write(spaces+stars+spaces+"\n")

f.close()