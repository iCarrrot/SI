from random import randint
from z4 import opt_dist
import time
start_time = time.time()

def printPic(table):
    for x in table:
        print("".join("x" if y else "." for y in x))
    print("\n\n\n")


def randTableGen(x, y):
    return [[randint(0, 1) for _ in range(x)] for _ in range(y)]


test = [
    ([7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7]),
    ([2, 2, 7, 7, 2, 2, 2], [2, 2, 7, 7, 2, 2, 2]),
    ([2, 2, 7, 7, 2, 2, 2], [4, 4, 2, 2, 2, 5, 5]),
    ([7, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7]),
    ([7, 5, 3, 1, 1, 1, 1], [1, 2, 3, 7, 3, 2, 1])
]
for (row, col) in test:

    table = []
    colState = {}
    rowState = {}
    colState[0] = 1
    rowState[0] = 1
    it = 0
    while sum(colState.values()) + sum(rowState.values()):
        it += 1
        table = randTableGen(len(col), len(row))
        for i in range(len(col)):
            _col = [x[i] for x in table]
            colState[i] = opt_dist(_col, col[i])[1]
        for i in range(len(row)):
            _row = table[i]
            rowState[i] = opt_dist(_row, row[i])[1]

        loop = 0
        loop2 = 0
        while sum(colState.values()):
            i = randint(0, len(col)-1)
            if loop >= 4*len(col) or loop2 > 4 * len(col):
                break
            if loop == 2*len(col):
                (_i, _j) = (randint(0, len(col)-1), randint(0, len(row)-1))
                table[_j][_i] ^= 1
                loop2 += 1

            if colState[i]:
                column = [x[i] for x in table]
                maxState = 0
                maxData = {'j': -1}
                for j in range(len(row)):
                    column[j] ^= 1
                    tempRow = table[j]
                    tempRow[i] ^= 1
                    newColState = opt_dist(column, col[i])[1]
                    newRowState = opt_dist(tempRow, row[j])[1]
                    state = colState[i] - newColState + \
                        rowState[j] - newRowState
                    if state > maxState:
                        maxState = state
                        maxData = {'j': j, "colS": newColState,
                                   "rowS": newRowState}
                    column[j] ^= 1
                    tempRow[i] ^= 1
                j = maxData['j']
                if j != -1:
                    table[j][i] ^= 1
                    colState[i] = maxData["colS"]
                    rowState[j] = maxData["rowS"]
                    loop = 0
                else:
                    loop += 1

    printPic(table)
# print("--- %s seconds ---" % (time.time() - start_time))
