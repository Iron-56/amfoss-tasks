import math

n = int(input("Enter rows: "))
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
	
	print(spaces+stars+spaces)