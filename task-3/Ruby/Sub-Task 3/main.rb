
puts  "Enter rows: "
n = gets.chomp.to_i
counter = n%2

for i in 0..(n-1)
	if counter == 0
		counter += 2
		next
	end

	stars = "*"*counter
	spaces = " "*(((n-counter)/2).floor())
	
	if i < (n/2).floor()
		counter += 2
	else
		counter -= 2
	end
	
	puts spaces+stars+spaces
end