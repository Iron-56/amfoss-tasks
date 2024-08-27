File.open("output.txt", "w") {
    |file| file.write(File.read("input.txt"))
}