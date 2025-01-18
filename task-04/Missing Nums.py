_ = input()
a = list(map(int, input().split()))
_ = input()
b = list(map(int, input().split()))

skip = 0
j = 0

for _ in range(len(a)):
    if a[j] != b[j+skip]:
        print(b[j+skip], end = ' ')
        skip += 1
        j -= 1
    j += 1
print()