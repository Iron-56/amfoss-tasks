package main

import (
	"fmt"
	"strings"
)

func main() {
	var n int
	fmt.Print("Enter rows: ")
	_, err := fmt.Scanf("%d", &n)
		
	if err != nil {
		panic(err)
	}
		
	var counter int = n%2

	for i := 0; i< n; i++{
		if counter == 0 {
			counter += 2
			continue
		}
		
		stars := strings.Repeat("*",counter)
		spaces := strings.Repeat(" ", int(((n-counter)/2)))
		
		if i < int(n/2) {
			counter += 2
		} else {
			counter -= 2
		}
			
		fmt.Println(spaces+stars+spaces)
	}
}