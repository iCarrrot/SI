from random import randint
import time
start_time = time.time()
# from time import sleep


def opt_dist1(row, size):
    if(len(row) == size):
        return size - sum(row)
    if(len(row) < size):
        print("ERROR za duży kawałęk")
        print("ERROR+5")
        return len(row)+5
    suma = sum(row)
    change = len(row)
    for i in range(len(row)-size+1):
        wind = row[i:i+size]
        _change = size - 2*sum(wind) + suma
        if _change < change:
            change = _change

    return change


def opt_dist(row, numberList):
    if len(numberList) == 1:
        return opt_dist1(row, numberList[0])

    if len(numberList) == 0:
        print("ERROR+1")
        return len(row)+1

    change = len(row)
    minLen = -1
    for i in numberList:
        minLen += i+1
        if i == 0:
            numberList.remove(0)
        if i > len(row):
            print("ERROR+2")
            return len(row)+2

    if len(numberList) == 1:
        return opt_dist1(row, numberList[0])

    if len(numberList) == 0:
        print("ERROR+4")
        return len(row)+4

    if minLen > len(row):
        print("ERROR+3")
        return len(row)+3

    firstLen = numberList[0]

    if minLen == len(row):
        res = [1 if x < y else 0  for y in numberList  for x in range(y+1)][:-1]
        change = 0
        for i in range(len(row)):
            change += row[i] ^ res[i]
        return change

    for i in range(len(row) - minLen+1):
        # print(i)
        # głowa:
        tempChange2 = opt_dist1(row[i:firstLen+i], numberList[0])
        # print("r: ", row[i:firstLen+i], tempRes2, tempChange2)
        # ogon:
        tempChange= opt_dist(row[firstLen+i+1:], numberList[1:])
        # print(tempRes, tempChange)
        tempChange += row[i+firstLen] + tempChange2 +sum(row[:i])

        if tempChange < change:
            change = tempChange

            # print("after:", change , res)

    return change


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
            colState[i] = opt_dist(_col, col[i])
        for i in range(len(row)):
            _row = table[i]
            rowState[i] = opt_dist(_row, row[i])

        loop = 0
        loop2 = 0
        while sum(colState.values()):
            i = randint(0, len(col)-1)
            # printPic(table)
            # sleep(0.1)
            if loop >= 5*len(col) or loop2 > 100 *len(col):
                break
            if loop == 2*len(col):
                # printPic(table)
                (_i, _j) = (randint(0, len(col)-1), randint(0, len(row)-1))
                table[_j][_i] ^= 1
                colState[_i] = opt_dist([x[_i] for x in table], col[_i])
                rowState[_j] = opt_dist(table[_j], row[_j])
                loop2 += 1

            if colState[i]:
                column = [x[i] for x in table]
                maxState = 0
                maxData = {'j': -1}
                for j in range(len(row)):
                    column[j] ^= 1
                    tempRow = table[j]
                    tempRow[i] ^= 1
                    newColState = opt_dist(column, col[i])
                    newRowState = opt_dist(tempRow, row[j])
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


with open("/home/michal/SI/lab2/zad_input.txt") as f:
    i = 0
    col, row = [], []
    for line in f:
        if i == 0:
            rowSize, colSize = [int(x) for x in line.split()]
        elif i < rowSize+1:
            row += [[int(x) for x in line.split()]]
        elif i < rowSize+1+colSize:
            col += [[int(x) for x in line.split()]]
        else:
            break
        i += 1


printPicFile(makePicture(row, col))


# test = [
#     ([[7], [7], [7], [7], [7], [7], [7]], [[7], [7], [7], [7], [7], [7], [7]]),
#     ([[2], [2], [7], [7], [2], [2], [2]], [[2], [2], [7], [7], [2], [2], [2]]),
#     ([[2], [2], [7], [7], [2], [2], [2]], [[4], [4], [2], [2], [2], [5], [5]]),
#     ([[7], [6], [5], [4], [3], [2], [1]], [[1], [2], [3], [4], [5], [6], [7]]),
#     ([[7], [5], [3], [1], [1], [1], [1]], [[1], [2], [3], [7], [3], [2], [1]])
# ]



# # row = "10110"
# row = "1011000010101"

# row = [int(x) for x in row]
# print(row)
# if __name__ == "__main__":

#     # for x in range(len(row)+1):
#         print(opt_dist(row, [1,1,1,1,1,1,1]))


# for (row, col) in test:
#     printPic(makePicture(row, col))

# print("--- %s seconds ---" % (time.time() - start_time))
