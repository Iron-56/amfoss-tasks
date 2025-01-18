from collections import Counter

n = int(input())
room = Counter(input().split())

for i in room:
    if room[i] == 1:
        print(i)
        break