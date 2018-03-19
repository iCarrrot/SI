from random import randint
# from z4 import opt_dist
import time
start_time = time.time()
from time import sleep


def opt_dist1(row, size):
    if(len(row) == size):
        return([1 for i in range(size)], size - sum(row))
    if(len(row) < size):
        print("ERROR za duży kawałęk")
        return ([], len(row)+5)
    suma = sum(row)
    change = len(row)
    index = -1
    for i in range(len(row)-size+1):
        wind = row[i:i+size]
        _change = size - 2*sum(wind) + suma
        if _change < change:
            index = i
            change = _change

    res = [0 for x in range(len(row))]
    res[index:index+size] = [1 for x in range(size)]
    return(res, change)


def opt_dist(row, numberList):
    if len(numberList) == 1:
        return opt_dist1(row, numberList[0])

    if len(numberList) == 0:
        return ([], len(row)+1)

    change = len(row)
    minLen = -1
    for i in numberList:
        minLen += i+1
        if i == 0:
            numberList.remove(0)
        if i > len(row):
            return ([], len(row)+5)

    if len(numberList) == 1:
        return opt_dist1(row, numberList[0])

    if len(numberList) == 0:
        return ([], len(row)+1)

    if minLen > len(row):
        return ([], len(row)+3)

    firstLen = numberList[0]

    if minLen == len(row):
        res = [0 for x in range(len(row))]
        j = 0
        for i in numberList:
            res[j:j+i] = [1 for x in range(i)]
            if j+i < len(row):
                res[j+i] = 0
            j += i+1
        change = 0
        for i in range(len(row)):
            change += row[i] ^ res[i]
        return (res, change)

    for i in range(len(row) - minLen+1):

        # print(i)

        # głowa:

        (tempRes2, tempChange2) = opt_dist1(row[i:firstLen+i], numberList[0])
        # print("r: ", row[i:firstLen+i], tempRes2, tempChange2)

        # ogon:
        (tempRes, tempChange) = opt_dist(row[firstLen+i+1:], numberList[1:])
        # print(tempRes, tempChange)

        tempChange += row[i+firstLen] + tempChange2+sum(row[:i])

        if tempChange < change:
            res = [0 for x in range(len(row))]
            change = tempChange
            res[firstLen+i+1:] = tempRes
            res[i:firstLen+i] = tempRes2
            res[i+firstLen] = 0

            # print("after:", change , res)

    return (res, change)


def printPic(table):
    for x in table:
        print("".join("x" if y else "." for y in x))
    print("\n\n\n")

def printPicFile(table):
    file = open("zad_output.txt","w") 
    for x in table:
        file.write("".join("#" if y else "." for y in x)+"\n")
    file.close() 


def randTableGen(x, y):
    return [[randint(0, 1) for _ in range(x)] for _ in range(y)]


def makePicture(row, col):
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
            # printPic(table)
            # sleep(0.1)
            if loop >= 4*len(col) or loop2 > 30 * len(col):
                # printPic(table)
                break
            if loop == 2*len(col):
                # printPic(table)
                (_i, _j) = (randint(0, len(col)-1), randint(0, len(row)-1))
                table[_j][_i] ^= 1
                colState[_i] = opt_dist([x[_i] for x in table], col[_i])[1]
                rowState[_j] = opt_dist(table[_j], row[_j])[1]
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

    return table


# with open("zad_input.txt") as f:
#     i = 0
#     col, row = [], []
#     for line in f:
#         if i == 0:
#             rowSize, colSize = [int(x) for x in line.split()]
#         elif i < rowSize+1:
#             row += [[int(x) for x in line.split()]]
#         elif i < rowSize+1+colSize:
#             col += [[int(x) for x in line.split()]]
#         else:
#             break
#         i += 1


# printPicFile(makePicture(row, col))


# test = [
#     ([[5], [1,1,1], [3], [2,2], [5]], [[2,2], [1,3], [3,1], [1,3], [2,2]])
#     # ([[1,1,1], [3], [2,2]], [[1,1], [2], [2], [2], [1,1]])
# ]


# row = "10110"
row = "11011"

row = [int(x) for x in row]
print(row)
if __name__ == "__main__":

    # for x in range(len(row)+1):
        x=[1,2]
        print(x, opt_dist(row, x))


# for (row, col) in test:
#     printPic(makePicture(row, col))

# print("--- %s seconds ---" % (time.time() - start_time))
