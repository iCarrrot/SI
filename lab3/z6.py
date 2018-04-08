import sys


def V(i, j):
    return 'V%d_%d' % (i, j)


def domains(Vs):
    return [q + ' in 0..1' for q in Vs]


def all_different(Qs):
    return 'all_distinct([' + ', '.join(Qs) + '])'

def _sum(Qs, res):
    return ' + '.join(Qs) + ' #= '+str(res)

def in_square(Qs):
    return "{0} + {3} #= {1} + {2} #\\/ {1} + {2} +{3} + {0} #= 1".format(Qs[0],Qs[1],Qs[2],Qs[3])

def in_triple(Qs):
    return " #\\ {1} #\\/ {0} #\\/ {2}".format(Qs[0],Qs[1],Qs[2])

def get_column(j, k):
    return [V(i, j) for i in range(k)]


def get_row(i, k):
    return [V(i, j) for j in range(k)]


def get_square(i,j):
    return [V(i1,j1) for i1 in range(i,i+2) for j1 in range(j,j+2)]


def get_triple_vertical(i,j):
    return [V(i1,j) for i1 in range(i,i+3)]


def get_triple_horizontal(i,j):
    return [V(i,j1) for j1 in range(j,j+3)]


def squareSum(a,b):
    return [in_square(get_square(i,j)) for i in range(0,a-1) for j in range(0,b-1)] 

def stormsSum(rows, cols):
    return [_sum(get_column(i, len(rows)), cols[i]) for i in range(len(cols))] \
         + [_sum(get_row(j, len(cols)), rows[j]) for j in range(len(rows))]

def stormsTriple(a,b):
    return [in_triple(get_triple_vertical(i,j)) for i in range(0,a-2) for j in range(0,b)]+ \
           [in_triple(get_triple_horizontal(i,j)) for i in range(0,a) for j in range(0,b-2)]

def print_constraints(Cs, indent, d):
    position = indent
    print (indent - 1) * ' ',
    for c in Cs:
        print c + ',',
        position += len(c)
        if position > d:
            position = indent
            print
            print (indent - 1) * ' ',


def storms(rows, cols, triples):
    # print(rows, cols, triples)
    variables = [V(i, j) for i in range(len(cols)) for j in range(len(rows))]
    print ':- use_module(library(clpfd)).'
    print 'solve([' + ', '.join(variables) + ']) :- '

    cs = domains(variables) + stormsSum(rows, cols) + squareSum(len(rows), len(cols))+ stormsTriple(len(rows), len(cols))

    for i, j, val in triples:
        cs.append('%s #= %d' % (V(i, j), val))

    print_constraints(cs, 4, 70),
    print
    print '    labeling([ff], [' + ', '.join(variables) + ']).'
    print
    print ':- solve(X), write(X), nl.'


if __name__ == "__main__":
    raw = 0
    triples = []
    with open("/home/michal/SI/lab3/zad_input.txt") as f:
        i = 0
        col, row = [], []
        for line in f:
            if i == 0:
                rows = [int(x) for x in line.split()]
            elif i == 1:
                cols = [int(x) for x in line.split()]
            else:
                triples.append(tuple([int(x) for x in line.split()]))
            i += 1
        storms(rows, cols, triples)
