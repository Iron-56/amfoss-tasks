import math

x = int(input())
n = int(input())

m = math.ceil(x**(1/n))-1
c = 0
powers = []
tmax = 0

for i in range(m):
    tmax += i+1
    powers.append((i+1)**n)

def count(terms, included, currentTerms=0, s=0):
    global c
    t = included**n+s
    if t==x and currentTerms == terms:
        c+=1
    if currentTerms < terms and t < x:
        for i in range(included, m+1):
            count(terms, i+1, currentTerms+1, t)
    
for t in range(tmax):
    for i in range(m+1):
        count(t, i+1)
print(c)