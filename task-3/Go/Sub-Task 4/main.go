package main

import (
	"fmt"
	"strings"
	"io"
	"os"
    "bufio"
    "strconv"
)

func main() {
	fi, err := os.Open("input.txt")
    if err != nil {
        panic(err)
    }
    defer fi.Close()
    
    scanner := bufio.NewScanner(fi)
    scanner.Scan()

    if err := scanner.Err();
    err != nil {
        panic(err)
        return
    }

    n, err := strconv.Atoi(strings.TrimSpace(scanner.Text()))
    if err != nil {
        panic(err)
    }
		
	var counter int = n%2
	var seq string = ""

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
			
		seq += spaces+stars+spaces+"\n"
	}
	
	fo, err := os.Create("output.txt")
    if err != nil {
        panic(err)
    }
    defer fo.Close()
	
	_, err = io.WriteString(fo, seq)
    if err != nil {
        fmt.Println("Error writing to file:", err)
        return
    }
}