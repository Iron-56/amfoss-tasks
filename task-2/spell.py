#grep -rlE 'good.*holy|holy.*good'
s = "MoonbloomMistveil"
f = ""

for c in s:
	p = chr(ord(c)-1)
	if p.lower() not in "aeiou":
		f += p
print(f)