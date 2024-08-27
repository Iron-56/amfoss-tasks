package main

import (
    "io"
    "os"
)

func main () {
    r, err := os.Open("input.txt")
    if err != nil {
        panic(err)
    }
    defer r.Close()

    w, err := os.Create("output.txt")
    if err != nil {
        panic(err)
    }
    defer w.Close()
    io.Copy(w, r)
}