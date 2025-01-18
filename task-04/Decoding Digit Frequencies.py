from collections import Counter

s = input()

d = Counter(s)

for i in range(10):
    print(d[str(i)], end = " ")
print()