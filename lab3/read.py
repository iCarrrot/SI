from sys import stdin, argv
file = open(str(argv[1])+"zad_input.txt", "w")
    
line = "new"
while line != "":
    line = stdin.readline()
    file.write(line)
file.close()