import sys

result = ""

def V(i,j):
    return 'V%d_%d' % (i,j)
    
def domains(Vs):
    return [ q + ' in 1..9' for q in Vs ]
    
def all_different(Qs):
    return 'all_distinct([' + ', '.join(Qs) + '])'
    
def get_column(j):
    return [V(i,j) for i in range(9)] 
            
def get_raw(i):
    return [V(i,j) for j in range(9)] 

def get_square(i,j):
    return [V(i1,j1) for i1 in range(3*i,3*i+3) for j1 in range(3*j,3*j+3)]

                        
def horizontal():   
    return [ all_different(get_raw(i)) for i in range(9)]

def vertical():
    return [all_different(get_column(j)) for j in range(9)]

def square():
    return [all_different(get_square(i,j)) for i in range(3) for j in range(3)]

def print_constraints(Cs, indent, d):
    global result
    position = indent
    result += (indent - 1) * ' ' + "\n"
    for c in Cs:
        result += c + ',' + "\n"
        position += len(c)
        if position > d:
            position = indent
            result+="\n"
            result += (indent - 1) * ' ' + "\n"

      
def sudoku(assigments):
    global result
    variables = [ V(i,j) for i in range(9) for j in range(9)]
    
    result += ':- use_module(library(clpfd)).' + "\n"
    result += 'solve([' + ', '.join(variables) + ']) :- ' + "\n"
    
    
    cs = domains(variables) + vertical() + horizontal() + square() 
    for i,j,val in assigments:
        cs.append( '%s #= %d' % (V(i,j), val) )
    
    print_constraints(cs, 4, 70),
    result+="\n"
    result += '    labeling([ff], [' +  ', '.join(variables) + ']).'  + "\n"
    result += "\n"
    result += ':- solve(X), open("prolog_result.txt", write, Stream),write(Stream, X),close(Stream), nl.\n' 

if __name__ == "__main__":
    raw = 0
    triples = []
    with open("/home/michal/SI/lab3/zad_input.txt") as f:
        for x in f:
            x = x.strip()
            if len(x) == 9:
                for i in range(9):
                    if x[i] != '.':
                        triples.append( (raw,i,int(x[i])) ) 
                raw += 1          
    sudoku(triples)
    file = open("zad_output.txt", "w")
    file.write(result)
    file.close()
    
"""
89.356.1.
3...1.49.
....2985.
9.7.6432.
.........
.6389.1.4
.3298....
.78.4....
.5.637.48

53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79

3.......1
4..386...
.....1.4.
6.924..3.
..3......
......719
........6
2.7...3..
"""    
